#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
solve_two_ring_vow.py — two_ring_vow.exe (两枚魔戒) 自动化破译与 Flag 提取工具
=================================================================================
样本: windows/vmp-crackmes/LvArshu-Flag/two_ring_vow.exe
作者背景: 纪念日 Crackme ("Happy 13 October, Arshu")
防御特征:
  - 双环核验拓扑: Visible Rehearsal Ring (诱导虚假 Token) vs Hidden Verifier Ring (真核验)
  - 核心核验函数 sub_140003290 在满足 15 字节输入且全部四重核验机一致时放行
  - 真实凭据由内部确定性状态机 sub_1400019A0(0..14) 自派生
"""

import sys, struct
from unicorn import *
from unicorn.x86_const import *

def extract_key(pe_path):
    d = open(pe_path, 'rb').read()
    lfa = struct.unpack_from('<I', d, 0x3c)[0]
    _, ns, _, _, _, osz, _ = struct.unpack_from('<HHIIIHH', d, lfa + 4)
    opt = lfa + 24
    ib = struct.unpack_from('<Q', d, opt + 24)[0]
    sec = opt + osz

    secs = []
    for i in range(ns):
        b = sec + i * 40
        n = d[b:b+8].rstrip(b'\0').decode('latin1')
        vs, va, rs, pr = struct.unpack_from('<IIII', d, b + 8)
        secs.append((n, va, vs, pr, rs))

    mu = Uc(UC_ARCH_X86, UC_MODE_64)

    for n, va, vs, pr, rs in secs:
        mva = ib + va
        msz = (max(vs, rs) + 0xfff) & ~0xfff
        mu.mem_map(mva, msz, UC_PROT_ALL)
        if rs:
            mu.mem_write(mva, d[pr : pr + rs])

    STK = 0x7ff000000000
    mu.mem_map(STK, 0x100000)
    SENT = 0xdead0000
    mu.mem_map(SENT, 0x1000)
    mu.mem_write(SENT, b'\xf4')

    func_va = ib + 0x19a0

    chars = []
    for i in range(15):
        rsp = STK + 0x80000
        mu.reg_write(UC_X86_REG_RSP, rsp)
        mu.reg_write(UC_X86_REG_RCX, i)
        mu.mem_write(rsp, struct.pack('<Q', SENT))
        mu.emu_start(func_va, SENT, timeout=10_000_000)
        rax = mu.reg_read(UC_X86_REG_RAX) & 0xFF
        chars.append(rax)

    raw_pass = bytes(chars).decode('ascii')
    return raw_pass

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '/root/逆向测试/windows/vmp-crackmes/LvArshu-Flag/two_ring_vow.exe'
    password = extract_key(target)
    print(f"[+] 破译成功！Canonical Password: {password}")
    print(f"[+] 对应 Flag 提交形式: VOW{{{password}}}")
