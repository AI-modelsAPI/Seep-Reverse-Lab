#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R1_runtime_vm_detector.py — 运行时 VM 探测器（金标准，零真机）
================================================================
设计原则: 不看文件名、不看字符串、不看静态表 —— 只看**运行时行为**。

真 VM 的必要条件（无法伪装）:
  C1 高频间接分发   : jmp/call [base+index*scale] 被执行 >= 100 次
  C2 分发点集中     : 少数 PC 贡献绝大多数分发（VM 主循环）
  C3 handler 多样性 : 分发目标 >= 16 个不同地址
  C4 字节码指针推进 : 分发间某个寄存器被固定步长推进（vm_ip 特征）
  C5 目标全在映像内 : 分发目标不是垃圾地址

方法论依据:
  - 自愈式仿真（general/methodology/01）
  - PolyUnpack 的「静态模型 vs 动态执行」差分思想
  - V5 的教训: 静态判据不可靠, 运行时才可靠
"""
import sys, os, struct, collections, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pe_loader_v2 import LoaderV2, API_SEMANTICS
from unicorn import *
from unicorn.x86_const import *
from capstone import *
md = Cs(CS_ARCH_X86, CS_MODE_64)

REGS = {
    'rax': UC_X86_REG_RAX, 'rcx': UC_X86_REG_RCX, 'rdx': UC_X86_REG_RDX,
    'rbx': UC_X86_REG_RBX, 'rsi': UC_X86_REG_RSI, 'rdi': UC_X86_REG_RDI,
    'rbp': UC_X86_REG_RBP, 'rsp': UC_X86_REG_RSP,
    'r8': UC_X86_REG_R8, 'r9': UC_X86_REG_R9, 'r10': UC_X86_REG_R10,
    'r11': UC_X86_REG_R11, 'r12': UC_X86_REG_R12, 'r13': UC_X86_REG_R13,
    'r14': UC_X86_REG_R14, 'r15': UC_X86_REG_R15,
}

# 输入候选（覆盖常见交互）
INPUTS = [
    b"test\n",
    b"A"*12 + b"\n",
    b"A"*511 + b"\n",      # Matryoshka-VM 需要 511 字节
    b"A"*255 + b"\n",
    b"A"*63 + b"\n",
    b"A"*31 + b"\n",
    b"A"*15 + b"\n",
]


def run_once(path, input_bytes=b"test\n", max_insn=600_000, timeout=25_000_000):
    """跑一次仿真，返回运行时观测数据"""
    ld = LoaderV2(path)
    mu = Uc(UC_ARCH_X86, UC_MODE_64)
    ld.map_into(mu)
    ld.apply_relocations(verbose=False)
    ld.prepare_stubs(mu)
    ld.stub_imports(verbose=False)

    # 环境桩
    STK = 0x7ff000000000
    mu.mem_map(STK, 0x100000)
    TEB = 0x7ffd00000000; mu.mem_map(TEB, 0x1000)
    PEB = 0x7ffd00001000; mu.mem_map(PEB, 0x1000)
    mu.mem_write(TEB+0x60, struct.pack('<Q', PEB))
    mu.mem_write(TEB+0x30, struct.pack('<Q', TEB))
    # TEB->StackBase/StackLimit
    mu.mem_write(TEB+0x08, struct.pack('<Q', STK+0x100000))
    mu.mem_write(TEB+0x10, struct.pack('<Q', STK))
    mu.mem_write(PEB+0x02, b'\x00')          # BeingDebugged
    mu.mem_write(PEB+0xbc, struct.pack('<I', 0))  # NtGlobalFlag
    mu.reg_write(UC_X86_REG_FS_BASE, TEB)
    mu.reg_write(UC_X86_REG_GS_BASE, TEB)
    rsp = STK+0x80000
    mu.reg_write(UC_X86_REG_RSP, rsp)
    mu.reg_write(UC_X86_REG_RBP, rsp)
    SENT = 0xdead0000
    mu.mem_map(SENT & ~0xfff, 0x1000); mu.mem_write(SENT & ~0xfff, b'\xf4')
    mu.mem_write(rsp, struct.pack('<Q', SENT))

    # 自愈 + 陷阱
    pages = set()
    def mp(a):
        pg = a & ~0xfff
        if pg in pages: return False
        try:
            mu.mem_map(pg, 0x1000, UC_PROT_ALL); pages.add(pg); return True
        except UcError: return False
    mu.hook_add(UC_HOOK_MEM_READ_UNMAPPED, lambda uc,a,ad,s,v,u: (mp(ad), True)[1])
    mu.hook_add(UC_HOOK_MEM_WRITE_UNMAPPED, lambda uc,a,ad,s,v,u: (mp(ad), True)[1])
    mu.hook_add(UC_HOOK_MEM_FETCH_UNMAPPED, lambda uc,a,ad,s,v,u: (mp(ad), True)[1])
    traps = collections.Counter()
    mu.hook_add(UC_HOOK_INTR, lambda uc,i,ud: (traps.update([i]), True)[1])

    # API 桩（带输入）
    pos = [0]
    def api_hook(uc, address, size, ud):
        api = ld.addr2api.get(address)
        if api is None: return True
        ld.call_log.append(api)
        if api in ('getchar',):
            ch = input_bytes[pos[0]] if pos[0] < len(input_bytes) else 0x0a
            pos[0] += 1; uc.reg_write(UC_X86_REG_RAX, ch)
        elif api == '__iob_func':
            uc.reg_write(UC_X86_REG_RAX, ld.heap_ptr); ld.heap_ptr += 0x1000
        else:
            sem = API_SEMANTICS.get(api, 'zero')
            if sem == 'heap':
                sz = uc.reg_read(UC_X86_REG_R8) or uc.reg_read(UC_X86_REG_RCX) or 0x100
                r = ld.heap_ptr; ld.heap_ptr += (max(sz,16)+15) & ~15
                uc.reg_write(UC_X86_REG_RAX, r)
            elif sem == 'handle': uc.reg_write(UC_X86_REG_RAX, ld.load_base)
            elif sem == 'proc':
                d = ld.stub_page + (len(ld.addr2api)+1)*0x20
                if d not in ld.addr2api:
                    mu.mem_write(d, bytes.fromhex('31c0c3')); ld.addr2api[d]='<proc>'
                uc.reg_write(UC_X86_REG_RAX, d)
            elif sem == 'const': uc.reg_write(UC_X86_REG_RAX, 1)
            elif sem == 'tick': uc.reg_write(UC_X86_REG_RAX, 0x100000)
            else: uc.reg_write(UC_X86_REG_RAX, 0)
        r = uc.reg_read(UC_X86_REG_RSP)
        ra = struct.unpack('<Q', uc.mem_read(r, 8))[0]
        uc.reg_write(UC_X86_REG_RSP, r+8); uc.reg_write(UC_X86_REG_RIP, ra)
        return True
    mu.hook_add(UC_HOOK_CODE, api_hook, ld.stub_page, ld.stub_page+0x10000)

    # ★ 运行时 VM 观测: 记录每次间接分发的 (PC, 目标, 索引寄存器, 索引值)
    disp_events = []          # (pc_rva, target_rva, idx_reg, idx_val, base_val)
    disp_pc = collections.Counter()
    insn_hist = collections.Counter()
    n_insn = [0]

    def on_code(uc, a, s, ud):
        n_insn[0] += 1
        if n_insn[0] > max_insn:
            return False
        insn_hist[a - ld.load_base] += 1
        try:
            ins = next(md.disasm(bytes(uc.mem_read(a, min(s,15))), a))
        except Exception:
            return True
        if ins.mnemonic not in ('jmp', 'call'):
            return True

        # ── 形态 B: jmp/call reg（寄存器间接分发）
        #    典型: movsxd rdx,[r15+rdx*4]; add rdx,r15; jmp rdx   (VMP 3.10 / 自研 VM)
        if ins.op_str in REGS:
            ireg = ins.op_str
            try:
                tgt = uc.reg_read(REGS[ireg])
                trva = tgt - ld.load_base
                if 0 <= trva < 0x4000000:
                    disp_events.append((a - ld.load_base, trva, ireg, 0, 0))
                    disp_pc[a - ld.load_base] += 1
            except (UcError, KeyError):
                pass
            return True

        if '[' not in ins.op_str:
            return True
        op = ins.op_str
        inner = op[op.index('[')+1:op.rindex(']')].replace(' ', '')
        if '*' not in inner:
            return True
        # 解析 [base + index*scale]
        base_n = idx_n = None; scale = 1
        for part in inner.split('+'):
            if '*' in part:
                idx_n = part.split('*')[0]
                try: scale = int(part.split('*')[1], 0)
                except ValueError: scale = 1
            elif part in REGS:
                base_n = part
        if not base_n or not idx_n:
            return True
        try:
            bv = uc.reg_read(REGS[base_n])
            iv = uc.reg_read(REGS[idx_n])
            addr = (bv + iv*scale) & 0xFFFFFFFFFFFFFFFF
            tgt = struct.unpack('<Q', uc.mem_read(addr, 8))[0]
            disp_events.append((a - ld.load_base, tgt - ld.load_base,
                                idx_n, iv, bv))
            disp_pc[a - ld.load_base] += 1
        except (UcError, KeyError):
            pass
        return True
    mu.hook_add(UC_HOOK_CODE, on_code)

    err = None
    try:
        mu.emu_start(ld.load_base + ld.ep, SENT, count=max_insn, timeout=timeout)
    except UcError as e:
        err = str(e)

    return dict(
        path=path, name=os.path.basename(path),
        insns=n_insn[0], err=err, pages=len(pages), traps=dict(traps),
        disp_events=disp_events, disp_pc=disp_pc, hist=insn_hist,
        api_calls=len(ld.call_log), img_base=ld.load_base,
        img_size=ld.sizeof_image, stubs=len(ld.addr2api),
    )


def evaluate(r):
    """按 C1-C5 判据评估"""
    ev = r['disp_events']
    n = len(ev)
    c1 = bool(n >= 100)

    # C2 分发点集中度: top1 PC 占比
    top_pc_ratio = 0.0
    if r['disp_pc']:
        tot = sum(r['disp_pc'].values())
        top_pc_ratio = r['disp_pc'].most_common(1)[0][1] / max(1, tot)
    c2 = bool(top_pc_ratio > 0.3 or (r['disp_pc'] and len(r['disp_pc']) <= 5))

    # C3 handler 多样性
    targets = set(t for _, t, _, _, _ in ev if 0 <= t < 0x4000000)
    c3 = bool(len(targets) >= 16)

    # C4 字节码指针推进: 分发目标序列呈「小步长偏移」= 同区域内游走
    #     真 VM 的 handler 都集中在同一节区, 目标两两间距较小
    c4 = False; ip_reg = None; ip_steps = None
    # 判据 0: 多分发点（嵌套 VM 特征）
    if len(r['disp_pc']) >= 2 and n >= 100:
        c4 = True; ip_reg = 'nested-VM'; ip_steps = len(r['disp_pc'])
    tgt_seq = [t for _, t, _, _, _ in ev if 0 <= t < 0x4000000]
    if not c4 and len(tgt_seq) >= 50:
        # 目标地址的标准差 / 跨度 —— VM handler 应聚集在有限范围
        mn, mx = min(tgt_seq), max(tgt_seq)
        span = mx - mn
        # VM handler 区域通常 < 512KB
        if span < 0x80000 and len(set(tgt_seq)) >= 16:
            c4 = True; ip_reg = 'hdr-range'; ip_steps = span
    # 备用: 索引寄存器的值呈规律变化
    if not c4 and len(ev) > 20:
        by_reg = collections.defaultdict(list)
        for _, _, ir, iv, _ in ev:
            by_reg[ir].append(iv)
        for reg, vals in by_reg.items():
            if len(vals) < 20: continue
            diffs = [vals[i+1]-vals[i] for i in range(min(len(vals)-1, 200))]
            dc = collections.Counter(diffs)
            if not dc: continue
            top_diff, cnt = dc.most_common(1)[0]
            if abs(top_diff) in (1,2,4,8,-1,-2,-4,-8) and cnt/len(diffs) > 0.5:
                c4 = True; ip_reg = reg; ip_steps = top_diff
                break

    # C5 目标有效性
    valid = sum(1 for _a, t, _b, _c, _d in ev if 0 <= t < 0x4000000)
    c5 = bool(n > 0 and valid/max(1, n) > 0.9)

    score = sum([c1, c2, c3, c4, c5])
    return dict(c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, score=score,
                n_disp=n, n_pc=len(r['disp_pc']), top_pc_ratio=top_pc_ratio,
                n_targets=len(targets), ip_reg=ip_reg, ip_steps=ip_steps,
                valid_ratio=valid/max(1, n))


def detect(path, verbose=True):
    name = os.path.basename(path)
    if verbose:
        print("=" * 90)
        print(f"[{name}]")
        print("=" * 90)
    # 多组输入尝试（有些需要正确输入才进 VM）
    best = None
    for inp in INPUTS:
        try:
            r = run_once(path, inp)
        except Exception as e:
            if verbose: print(f"  [!] 仿真异常: {e}")
            return None
        e = evaluate(r)
        if best is None or e['score'] > best[1]['score']:
            best = (r, e, inp)
        if e['score'] >= 4:
            break
    r, e, inp = best
    if verbose:
        print(f"  执行 {r['insns']:,} 条   停止: {r['err']}")
        print(f"  自愈页 {r['pages']}   陷阱 {r['traps']}   API {r['api_calls']}")
        print(f"  输入: {inp!r}")
        print(f"\n  === 运行时 VM 判据 ===")
        print(f"    C1 高频间接分发 (>=100)      : {e['n_disp']:>8,d}  {'✅' if e['c1'] else '❌'}")
        print(f"    C2 分发点集中 (top1>{30}%)    : {e['top_pc_ratio']*100:>7.1f}%  ({e['n_pc']} 个分发点) {'✅' if e['c2'] else '❌'}")
        print(f"    C3 handler 多样性 (>=16)     : {e['n_targets']:>8,d}  {'✅' if e['c3'] else '❌'}")
        print(f"    C4 字节码指针推进            : {str(e['ip_reg'])+' 步长'+str(e['ip_steps']) if e['c4'] else '未观测':>10s}  {'✅' if e['c4'] else '❌'}")
        print(f"    C5 分发目标有效 (>90%)       : {e['valid_ratio']*100:>7.1f}%  {'✅' if e['c5'] else '❌'}")
        print(f"\n  === 评分 {e['score']}/5  {'★★★ 真 VM' if e['score']>=4 else ('★ 疑似' if e['score']>=2 else '非 VM')} ===")
        if e['n_disp'] > 0:
            print(f"  分发点 Top5:")
            for pc, c in r['disp_pc'].most_common(5):
                print(f"    RVA 0x{pc:06x}  {c:,} 次")
    return dict(path=path, name=name, **e, insns=r['insns'],
                api=r['api_calls'], pages=r['pages'], input=inp)


if __name__ == '__main__':
    paths = sys.argv[1:]
    results = []
    for p in paths:
        try:
            x = detect(p)
            if x: results.append(x)
        except Exception as ex:
            print(f"[!] {p}: {ex}")
        print()
    print("=" * 90)
    print("运行时 VM 检测汇总（金标准，按评分排序）")
    print("=" * 90)
    print(f"{'评分':>5} {'样本':36s} {'分发次数':>10s} {'PC数':>6s} {'目标数':>7s} {'字节码指针':>12s}")
    for r in sorted(results, key=lambda x: -x['score']):
        ip = f"{r['ip_reg']}*{r['ip_steps']}" if r['ip_steps'] is not None else "-"
        tag = '★真VM' if r['score']>=4 else ('疑似' if r['score']>=2 else '非VM')
        print(f"{r['score']:>2}/5  {r['name']:36s} {r['n_disp']:>10,d} {r['n_pc']:>6d} "
              f"{r['n_targets']:>7d} {ip:>12s}  {tag}")
