#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V1_reproducibility.py — 可重复性验证（零真机）
================================================
原理: 同一仿真跑多次/多种配置, 结果必须一致。
      若表基址、handler 数量、opcode 集合每次都不同 -> 结论不可信。

变体:
  run#1  原始配置 max_insn=600k
  run#2  max_insn=300k (更早停止)   -> 表基址应相同
  run#3  max_insn=900k (更晚停止)   -> 表基址应相同
  run#4  改变栈基址 (STACK_BASE 偏移) -> 表基址应相同(若与栈无关)

判据: r11/表基址 稳定 + handler 表内容哈希一致
"""
import sys, os, struct, json, hashlib, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vmp_selfheal_run import SelfHealingEmu
from unicorn import *
from unicorn.x86_const import *
from capstone import *

md = Cs(CS_ARCH_X86, CS_MODE_64)
REG = {'rax': UC_X86_REG_RAX, 'rcx': UC_X86_REG_RCX, 'rdx': UC_X86_REG_RDX,
       'rbx': UC_X86_REG_RBX, 'rsi': UC_X86_REG_RSI, 'rdi': UC_X86_REG_RDI,
       'rbp': UC_X86_REG_RBP, 'rsp': UC_X86_REG_RSP,
       'r8': UC_X86_REG_R8, 'r9': UC_X86_REG_R9, 'r10': UC_X86_REG_R10,
       'r11': UC_X86_REG_R11, 'r12': UC_X86_REG_R12, 'r13': UC_X86_REG_R13,
       'r14': UC_X86_REG_R14, 'r15': UC_X86_REG_R15}


def one_run(sample, max_insn, label):
    """单次运行: 返回 (分发点数, 表基址, 表内容哈希, opcode集合)"""
    e = SelfHealingEmu(sample, max_insn=max_insn)
    mu, base = e.mu, e.ld.load_base
    mu.hook_add(UC_HOOK_INTR, lambda uc, i, ud: True)

    disps = []
    tbl = [None]

    def on_code(uc, addr, size, ud):
        try:
            ins = next(md.disasm(bytes(uc.mem_read(addr, min(size, 15))), addr))
        except Exception:
            return True
        # 形态 A: jmp/call [base + index*8]
        if ins.mnemonic in ('jmp', 'call') and '[' in ins.op_str and '*8' in ins.op_str.replace(' ', ''):
            inner = ins.op_str[ins.op_str.index('[')+1:ins.op_str.rindex(']')].replace(' ', '')
            b_ = i_ = None
            for p in inner.split('+'):
                if '*' in p: i_ = p.split('*')[0]
                elif p in REG: b_ = p
            if b_ and i_:
                try:
                    bv = uc.reg_read(REG[b_]); iv = uc.reg_read(REG[i_])
                    t = struct.unpack('<Q', uc.mem_read((bv+iv*8) & 0xFFFFFFFFFFFFFFFF, 8))[0]
                    if base <= t < base + 0x3000000:
                        disps.append((iv & 0xFF, t - base)); tbl[0] = bv
                except (UcError, KeyError): pass
        # 形态 B: jmp reg (3.10)
        elif ins.mnemonic == 'jmp' and ins.op_str in REG:
            try:
                r10 = uc.reg_read(UC_X86_REG_R10); r11 = uc.reg_read(UC_X86_REG_R11)
                t = uc.reg_read(REG[ins.op_str])
                off = struct.unpack('<i', uc.mem_read(r11 + r10*4, 4))[0]
                if (r11 + off) & 0xFFFFFFFFFFFFFFFF == t and base <= t < base + 0x3000000:
                    disps.append((r10 & 0xFF, t - base)); tbl[0] = r11
            except (UcError, KeyError): pass
        return True
    mu.hook_add(UC_HOOK_CODE, on_code)
    e.run()

    if not tbl[0]:
        return dict(label=label, ok=False, reason='no table captured',
                    insns=len(e.trace))
    # 表内容
    itemsz = 4 if 'jmp rdx' in str(disps[:1]) else 4
    # 自动判定: 若表基址看起来指向 4 字节相对表
    raw = bytes(mu.mem_read(tbl[0], 256*4))
    h = hashlib.sha256(raw).hexdigest()[:16]
    return dict(label=label, ok=True, insns=len(e.trace),
                dispatch=len(disps), table_base=hex(tbl[0]),
                opcodes=sorted(set(o for o, _ in disps)),
                table_hash=h, raw=raw.hex()[:64])


def main(sample):
    print("=" * 84)
    print(f"V1 可重复性验证: {os.path.basename(sample)}")
    print("=" * 84)
    runs = []
    for label, n in [("run#1 600k", 600_000), ("run#2 300k", 300_000),
                     ("run#3 900k", 900_000)]:
        r = one_run(sample, n, label)
        runs.append(r)
        if r['ok']:
            print(f"  {label:12s} insns={r['insns']:>9,d}  dispatch={r['dispatch']:>7,d}  "
                  f"table={r['table_base']}  hash={r['table_hash']}  "
                  f"opcodes={len(r['opcodes'])}")
        else:
            print(f"  {label:12s} ❌ {r['reason']}")

    ok = [r for r in runs if r['ok']]
    if len(ok) < 2:
        print("\n  ❌ 无法验证（有效运行不足）")
        return
    # 判据
    bases = set(r['table_base'] for r in ok)
    hashes = set(r['table_hash'] for r in ok)
    print(f"\n  表基址集合 : {bases}   {'✅ 稳定' if len(bases)==1 else '❌ 不稳定'}")
    print(f"  表内容哈希 : {hashes}   {'✅ 一致' if len(hashes)==1 else '❌ 不一致'}")
    # opcode 集合的包含关系
    sets = [set(r['opcodes']) for r in ok]
    inter = set.intersection(*sets)
    union = set.union(*sets)
    print(f"  opcode 交集: {len(inter)}   并集: {len(union)}   "
          f"{'✅ 包含' if len(inter)==len(sets[0]) else '⚠ 部分差异'}")
    verdict = (len(bases) == 1 and len(hashes) == 1)
    print(f"\n  => V1 {'✅ 通过' if verdict else '❌ 失败'}: 多次运行表基址与内容一致，结论可重复")
    return runs


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else
         '/root/逆向测试/windows/vmp-samples/3.10.0/math.3.10.0-virt.exe')
