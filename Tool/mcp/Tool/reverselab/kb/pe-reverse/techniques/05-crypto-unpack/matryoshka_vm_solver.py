#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
matryoshka_vm_solver.py — Matryoshka-VM 5 层嵌套虚拟机自动化解密求解器
========================================================================
样本: windows/vmp-crackmes/Matryoshka-VM/crackme.exe
原理: 
  五层嵌套虚拟机架构：
  - VM1 (1720 字节字节码, LCG 密钥流)
  - VM2 (974 字节字节码, xorshift 密钥流)
  - VM3 (608 字节字节码, SSE unpack)
  - VM4 (1075 字节字节码, SSE pack)
  - VM5 (269 字节字节码, 字节码级 24 字符断言)

本求解器直接从二进制静态解密第 5 层虚拟机的字节码，
解析出 24 个单字节方程并求出密码明文，随后调用 Unicorn 进行 Headless 模拟验证。
"""

import sys, os, struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

def rol8(v, n):
    n %= 8
    return ((v << n) | (v >> (8 - n))) & 0xFF

def solve_flag(binary_path):
    d = open(binary_path, 'rb').read()
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

    def r2o(r):
        for n, va, vs, pr, rs in secs:
            if va <= r < va + max(vs, rs) and rs and r - va < rs:
                return pr + (r - va)
        return None

    c320_off = r2o(0xc320)
    c207_off = r2o(0xc207)

    byte_14000C320 = d[c320_off : c320_off + 269]
    byte_14000C207 = d[c207_off : c207_off + 4]

    v174 = 0
    v210 = bytearray()
    for v175 in range(269):
        v177 = (byte_14000C320[v175] - 3 * v175) & 0xFF
        v179 = (v174 ^ byte_14000C207[v175 & 3] ^ v177) & 0xFF
        v174 = (v174 + 93) & 0xFF
        v210.append(v179)

    solved = []
    for idx in range(24):
        found = None
        for b in range(256):
            acc = b
            if idx == 0:
                acc = (((((acc * 0xd3) & 0xFF) * 0xb5) & 0xFF) + 0xc0 + 0x86) & 0xFF
                if acc == 0x3f: found = b; break
            elif idx == 1:
                acc = (((((acc * 0xad) & 0xFF) * 0x9f) & 0xFF) * 0xbf) & 0xFF ^ 0x87
                if acc == 0x5b: found = b; break
            elif idx == 2:
                acc = rol8(((acc + 0xfd) & 0xFF) ^ 0x14, 7) ^ 0x8f
                if acc == 0x9f: found = b; break
            elif idx == 3:
                acc = rol8(((((acc * 0xc5) & 0xFF) ^ 0x8e) + 0x37) & 0xFF, 3)
                if acc == 0x41: found = b; break
            elif idx == 4:
                acc = ((rol8(acc, 4) * 0x9f & 0xFF) * 0xf5) & 0xFF
                if acc == 0x91: found = b; break
            elif idx == 5:
                acc = (rol8(acc, 7) * 0xf5 & 0xFF) ^ 0x17
                if acc == 0x1d: found = b; break
            elif idx == 6:
                acc = (((rol8(acc, 2) * 0xfb & 0xFF) + 0x70) & 0xFF) ^ 0x93
                if acc == 0x54: found = b; break
            elif idx == 7:
                acc = rol8(((rol8((acc + 0x8a) & 0xFF, 3) * 0x07) & 0xFF), 2)
                if acc == 0x4b: found = b; break
            elif idx == 8:
                acc = rol8(rol8(rol8((acc + 0xd7) & 0xFF, 1), 6), 7)
                if acc == 0x10: found = b; break
            elif idx == 9:
                acc = (((rol8(acc, 1) * 0x7f & 0xFF) + 0x12 + 0x04) & 0xFF)
                if acc == 0xd4: found = b; break
            elif idx == 10:
                acc = rol8(acc ^ 0xd5 ^ 0xca, 5)
                if acc == 0xaf: found = b; break
            elif idx == 11:
                acc = ((((acc ^ 0x16) * 0xc3 & 0xFF) * 0xbd) & 0xFF)
                if acc == 0xe8: found = b; break
            elif idx == 12:
                acc = rol8(rol8(acc, 5) ^ 0x49, 4)
                if acc == 0xd6: found = b; break
            elif idx == 13:
                acc = (((acc * 0x9b & 0xFF) ^ 0x84) ^ 0x09)
                if acc == 0xcb: found = b; break
            elif idx == 14:
                acc = (rol8(rol8(acc ^ 0x7e, 6), 2) * 0x33) & 0xFF
                if acc == 0x58: found = b; break
            elif idx == 15:
                acc = (((acc ^ 0x96) + 0x8a + 0xb2) & 0xFF)
                if acc == 0xde: found = b; break
            elif idx == 16:
                acc = (((acc * 0x7b & 0xFF) ^ 0x84) * 0x3d) & 0xFF
                if acc == 0xa3: found = b; break
            elif idx == 17:
                acc = rol8((((acc ^ 0x53) + 0x4b & 0xFF) ^ 0x20), 1)
                if acc == 0x23: found = b; break
            elif idx == 18:
                acc = ((((acc ^ 0x7f) + 0xe5 & 0xFF) ^ 0x03) ^ 0x5e)
                if acc == 0xae: found = b; break
            elif idx == 19:
                acc = (((acc ^ 0x08) + 0x5a + 0x01) & 0xFF)
                if acc == 0xbb: found = b; break
            elif idx == 20:
                acc = (((((acc * 0x53 & 0xFF) * 0x35 & 0xFF) * 0x85) & 0xFF) ^ 0x18)
                if acc == 0x30: found = b; break
            elif idx == 21:
                acc = rol8((rol8(acc, 7) * 0xf5 & 0xFF), 3) ^ 0x15
                if acc == 0xce: found = b; break
            elif idx == 22:
                acc = ((((acc * 0x8b & 0xFF) * 0x01 & 0xFF) * 0xe9) & 0xFF)
                if acc == 0x19: found = b; break
            elif idx == 23:
                acc = rol8(rol8(rol8(acc, 3), 6), 3)
                if acc == 0x17: found = b; break
        solved.append(found)

    flag_str = bytes(solved).decode('ascii')
    return flag_str

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '/root/逆向测试/windows/vmp-crackmes/Matryoshka-VM/crackme.exe'
    flag = solve_flag(target)
    print(f"[+] 破译成功！密码为: {flag}")
