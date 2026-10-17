#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_310_final.py — VMP 3.10.x 计算型分发 handler 表提取（T-B 定稿）
========================================================================
破译的分发机制 (仿真实证, 28551/28551 公式匹配):
    movzx  r10d, byte ptr [rsi]            ; opcode = vm_ip[0]
    add    rsi, 1                          ; vm_ip++
    movsxd rdx, dword ptr [r11 + r10*4]    ; 32位有符号相对偏移
    add    rdx, r11                        ; 目标 = 表基址 + 偏移
    jmp    rdx                             ; 寄存器分发

对比: 3.0-3.4 用 jmp qword [r12+rax*8] (64位绝对表, 静态可扫)
      3.10   用 jmp rdx               (32位相对表, 必须运行时)
"""
import sys, os, struct, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vmp_selfheal_run import SelfHealingEmu
from unicorn import *
from unicorn.x86_const import *
from capstone import *

md = Cs(CS_ARCH_X86, CS_MODE_64)

REG_MAP = {
    'rax': UC_X86_REG_RAX, 'rcx': UC_X86_REG_RCX, 'rdx': UC_X86_REG_RDX,
    'rbx': UC_X86_REG_RBX, 'rsi': UC_X86_REG_RSI, 'rdi': UC_X86_REG_RDI,
    'rbp': UC_X86_REG_RBP, 'rsp': UC_X86_REG_RSP,
    'r8': UC_X86_REG_R8, 'r9': UC_X86_REG_R9, 'r10': UC_X86_REG_R10,
    'r11': UC_X86_REG_R11, 'r12': UC_X86_REG_R12, 'r13': UC_X86_REG_R13,
    'r14': UC_X86_REG_R14, 'r15': UC_X86_REG_R15,
}


def extract(sample, max_insn=800_000, outdir='out'):
    name = os.path.basename(sample)
    print("=" * 88)
    print(f"T-B 定稿: VMP 3.10 计算型分发提取 — {name}")
    print("=" * 88)

    e = SelfHealingEmu(sample, max_insn=max_insn)
    mu, base = e.mu, e.ld.load_base
    mu.hook_add(UC_HOOK_INTR, lambda uc, i, ud: True)

    events = []
    found = [None]

    def on_code(uc, addr, size, ud):
        try:
            code = bytes(uc.mem_read(addr, min(size, 15)))
            ins = next(md.disasm(code, addr))
        except Exception:
            return True
        if ins.mnemonic == 'jmp' and ins.op_str in REG_MAP:
            if found[0] is None:
                found[0] = (addr, ins.op_str)
            if ins.op_str == found[0][1]:
                try:
                    r10 = uc.reg_read(UC_X86_REG_R10)
                    r11 = uc.reg_read(UC_X86_REG_R11)
                    tgt = uc.reg_read(REG_MAP[ins.op_str])
                    events.append(dict(op=r10 & 0xFF, rva=int(tgt) - base,
                                       r11=r11, tgt=int(tgt)))
                except Exception:
                    pass
        return True
    mu.hook_add(UC_HOOK_CODE, on_code)
    e.run()

    if not events:
        print("  ❌ 未捕获分发事件")
        return None

    d_rva, d_reg = found[0][0] - base, found[0][1]
    r11 = events[0]['r11']
    print(f"  执行指令   : {len(e.trace):,}")
    print(f"  分发点     : RVA 0x{d_rva:x}  (jmp {d_reg})")
    print(f"  分发事件   : {len(events):,}")
    print(f"  表基址 r11 : 0x{r11:x}  (RVA 0x{r11-base:x})")

    # 公式验证
    ok = 0
    for x in events:
        try:
            off = struct.unpack('<i', mu.mem_read(x['r11'] + x['op'] * 4, 4))[0]
            if (x['r11'] + off) & 0xFFFFFFFFFFFFFFFF == x['tgt']:
                ok += 1
        except UcError:
            pass
    pct = ok / len(events) * 100
    print(f"  公式验证   : {ok}/{len(events)}  ({pct:.1f}%)  "
          f"{'✅ 完全匹配' if ok == len(events) else ''}")

    # 提取表
    table = []
    for i in range(256):
        try:
            off = struct.unpack('<i', mu.mem_read(r11 + i * 4, 4))[0]
            table.append((r11 + off) & 0xFFFFFFFFFFFFFFFF)
        except UcError:
            table.append(0)
    inimg = sum(1 for v in table if base <= v < base + 0x3000000)
    print(f"  表         : 256 项 x 4 字节, 指向映像内 {inimg}")

    # 语义
    spec, kinds = {}, collections.Counter()
    PATTERNS = [('imul', 'vm_mul'), ('cpuid', 'vm_cpuid'), ('rdtsc', 'vm_rdtsc'),
                ('popfq', 'vm_flags'), ('pushfq', 'vm_flags'),
                ('shld', 'vm_shxd'), ('shrd', 'vm_shxd'),
                ('shl ', 'vm_shift'), ('shr ', 'vm_shift'), ('sar ', 'vm_shift'),
                ('rol ', 'vm_rotate'), ('ror ', 'vm_rotate'),
                ('rcl ', 'vm_rotate'), ('rcr ', 'vm_rotate'),
                ('xor', 'vm_xor'), ('and ', 'vm_and'), ('or ', 'vm_or'),
                ('not ', 'vm_not'), ('neg ', 'vm_neg'),
                ('adc', 'vm_adc'), ('sbb', 'vm_sbb'),
                ('add', 'vm_add'), ('sub', 'vm_sub'),
                ('cmp', 'vm_cmp'), ('test', 'vm_test'), ('mov', 'vm_mov')]
    for i, v in enumerate(table):
        if not (base <= v < base + 0x3000000):
            continue
        try:
            b = bytes(mu.mem_read(v, 48))
            seq = []
            for ins in md.disasm(b, v):
                seq.append(f"{ins.mnemonic} {ins.op_str}")
                if ins.mnemonic in ('jmp', 'call', 'ret') or len(seq) >= 10:
                    break
            t = ' '.join(seq)
            k = 'unknown'
            for pat, kk in PATTERNS:
                if pat in t:
                    k = kk
                    break
            spec[i] = dict(rva=v - base, kind=k, seq=seq)
            kinds[k] += 1
        except Exception:
            pass

    executed = set(x['op'] for x in events)
    print(f"  执行 opcode: {len(executed)} 种")
    print(f"  建模 handler: {len(spec)}")
    print(f"\n  语义分类:")
    for k, c in kinds.most_common(12):
        print(f"    {k:14s} {c:4d}")

    by_kind = collections.defaultdict(list)
    for op, info in spec.items():
        by_kind[info['kind']].append(op)
    print(f"\n  handler 轮换 (多变体):")
    for k, ops in sorted(by_kind.items(), key=lambda x: -len(x[1]))[:8]:
        print(f"    {k:14s} {len(ops):3d} 变体")

    print(f"\n  handler 样例:")
    for i in sorted(executed)[:8]:
        if i in spec:
            print(f"    op=0x{i:02x} RVA=0x{spec[i]['rva']:06x} "
                  f"[{spec[i]['kind']:12s}] {' ; '.join(spec[i]['seq'][:2])}")

    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, name + '.handler_map_310.json')
    json.dump(dict(sample=sample,
                   mechanism='movzx r10d,[rsi]; add rsi,1; movsxd rdx,[r11+r10*4]; add rdx,r11; jmp rdx',
                   dispatch_rva=hex(d_rva), jmp_reg=d_reg,
                   table_base=hex(r11), table_rva=hex(r11 - base),
                   formula_match=f'{ok}/{len(events)}',
                   handlers=spec, kinds=dict(kinds),
                   variants={k: sorted(v) for k, v in by_kind.items()},
                   executed_opcodes=sorted(executed),
                   table_entries=[hex(v) for v in table],
                   dispatch_count=len(events)),
              open(out, 'w'), indent=2)
    print(f"\n  [+] {out}")
    return spec


if __name__ == '__main__':
    extract(sys.argv[1] if len(sys.argv) > 1 else
            '/root/逆向测试/windows/vmp-samples/3.10.0/math.3.10.0-virt.exe')
