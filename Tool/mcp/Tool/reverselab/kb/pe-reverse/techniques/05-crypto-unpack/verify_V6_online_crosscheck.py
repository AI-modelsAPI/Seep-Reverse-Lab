#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V6_online_crosscheck.py — 联网检索后的补充验证
================================================
根据网上检索到的权威分析（mzakocs VMP3 分析、VMPLift、vmp-reverse-skill），
补充验证三项此前未检查的内容:

  V6-A 滚动密钥检查    : handler 内的密钥寄存器是否随执行变化
  V6-B handler 合并检查: 是否「1 opcode = 1 handler」
  V6-C 架构代际定位    : 我的样本属于哪一代 VMP 架构
"""
import sys, os, struct, collections, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vmp_selfheal_run import SelfHealingEmu
from unicorn import *
from unicorn.x86_const import *
from capstone import *
md = Cs(CS_ARCH_X86, CS_MODE_64)

R = {
    'rax': UC_X86_REG_RAX, 'rcx': UC_X86_REG_RCX, 'rdx': UC_X86_REG_RDX,
    'rbx': UC_X86_REG_RBX, 'rsi': UC_X86_REG_RSI, 'rdi': UC_X86_REG_RDI,
    'r8': UC_X86_REG_R8, 'r9': UC_X86_REG_R9, 'r10': UC_X86_REG_R10,
    'r11': UC_X86_REG_R11, 'r12': UC_X86_REG_R12, 'r13': UC_X86_REG_R13,
    'r14': UC_X86_REG_R14, 'r15': UC_X86_REG_R15,
}


def check(sample, max_insn=400000):
    name = os.path.basename(sample)
    print("=" * 86)
    print(f"V6 联网检索后的补充验证: {name}")
    print("=" * 86)
    e = SelfHealingEmu(sample, max_insn=max_insn)
    mu, base = e.mu, e.ld.load_base
    mu.hook_add(UC_HOOK_INTR, lambda uc, i, ud: True)

    # 定位 dispatcher: 记录所有 jmp/call [base+idx*W] 或 jmp reg
    disp_addr = [None]
    segs = []              # (opcode, insn_count)
    reg_samples = []       # handler 内的寄存器采样
    cur = [0]; pend = [None]
    cnt = [0]

    def on_code(uc, addr, size, ud):
        try:
            ins = next(md.disasm(bytes(uc.mem_read(addr, min(size, 15))), addr))
        except Exception:
            return True
        isdisp = False
        if ins.mnemonic in ('jmp', 'call'):
            if '[' in ins.op_str and ('*8' in ins.op_str.replace(' ', '') or '*4' in ins.op_str.replace(' ', '')):
                isdisp = True
            elif ins.op_str in R:
                isdisp = True
        if isdisp:
            if disp_addr[0] is None:
                disp_addr[0] = addr
            if addr == disp_addr[0]:
                # 记录 opcode + 寄存器采样
                if pend[0] is not None:
                    segs.append((pend[0], cnt[0]))
                op = uc.reg_read(UC_X86_REG_RAX) & 0xFF
                pend[0] = op; cnt[0] = 0
                rva = addr - base
                if 0xee000 <= rva < 0xf3000 or 0x100000 <= rva < 0x140000:
                    reg_samples.append(dict(
                        r9=uc.reg_read(UC_X86_REG_R9),
                        rbx=uc.reg_read(UC_X86_REG_RBX),
                        r13=uc.reg_read(UC_X86_REG_R13),
                        r14=uc.reg_read(UC_X86_REG_R14),
                        r15=uc.reg_read(UC_X86_REG_R15)))
        else:
            if pend[0] is not None:
                cnt[0] += 1
        return True
    mu.hook_add(UC_HOOK_CODE, on_code)
    e.run()

    if not disp_addr[0]:
        print("  ❌ 未找到 dispatcher"); return
    print(f"  dispatcher RVA: 0x{disp_addr[0]-base:x}")
    print(f"  采样 dispatch : {len(segs):,}")

    # ── V6-A 滚动密钥 ──
    print(f"\n  === V6-A 滚动密钥检查 ===")
    print(f"    （若某寄存器几乎每次都变 = 滚动密钥候选）")
    rolling = []
    for reg in ('r9', 'rbx', 'r13', 'r14', 'r15'):
        vals = [x[reg] for x in reg_samples]
        if not vals: continue
        u = len(set(vals))
        ratio = u / len(vals)
        tag = '⚠ 滚动密钥候选' if ratio > 0.5 else '稳定常量'
        print(f"      {reg:4s}: 唯一值 {u:>6,d} / {len(vals):,} = {ratio*100:6.2f}%  {tag}")
        if ratio > 0.5: rolling.append(reg)
    print(f"    => {'⚠ 检测到滚动密钥: ' + ','.join(rolling) if rolling else '✅ 无滚动密钥（早期明文架构）'}")

    # ── V6-B handler 合并 ──
    print(f"\n  === V6-B handler 合并检查 ===")
    byop = collections.defaultdict(list)
    for op, n in segs:
        byop[op].append(n)
    tot = len(byop)
    const1 = sum(1 for o in byop if len(set(byop[o])) == 1)
    print(f"    opcode 种类: {tot}")
    print(f"    长度恒定的: {const1} ({const1/max(1,tot)*100:.1f}%)")
    multi = {o: sorted(set(byop[o])) for o in byop if len(set(byop[o])) > 1}
    if multi:
        print(f"    长度可变的: {len(multi)} 个，例:")
        for o, ls in list(multi.items())[:5]:
            print(f"      0x{o:02x}: {ls[:6]}")
    verdict = const1 / max(1, tot) > 0.9
    print(f"    => {'✅ 1 opcode = 1 handler（无合并）' if verdict else '⚠ 可能有 handler 合并'}")

    # ── V6-C 架构代际 ──
    print(f"\n  === V6-C 架构代际定位 ===")
    # 从 dispatcher 形态判断
    try:
        ins = next(md.disasm(bytes(mu.mem_read(disp_addr[0], 15)), disp_addr[0]))
        form = f"{ins.mnemonic} {ins.op_str}"
    except Exception:
        form = '?'
    print(f"    dispatcher 形态: {form}")
    if '*' in form:
        gen, mech = 'Gen-1 (3.0-3.4)', '固定跳表 jmp [r12+rax*8]，表项=明文绝对地址'
    else:
        gen, mech = 'Gen-3 (FDJ)', '当前handler+解码偏移，无表'
    print(f"    判定代际       : {gen}")
    print(f"    分发机制       : {mech}")
    print(f"    滚动密钥       : {'有' if rolling else '无'}")
    print(f"    opcode 概念    : {'有' if tot > 0 else '无'}")
    print(f"\n    【对照 mzakocs 的 VMP 3.5 分析】")
    print(f"      3.5: 无 opcode、无表、有滚动密钥、FDJ 分发")
    print(f"      本样本: {'与 3.5 一致' if rolling else '与 3.5 不同 —— 属更早的 Gen-1 架构'}")

    return dict(rolling=rolling, dispatcher=form, gen=gen,
                const_ratio=const1/max(1,tot), opcodes=tot)


if __name__ == '__main__':
    for p in sys.argv[1:] or ['/root/逆向测试/windows/vmp-samples/3.0.0/math.3.0.0-virt.exe']:
        check(p); print()
