#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
solve_inside.py — Inside-the-Machine 自定义虚拟机自动化破译与 Password 提取工具
================================================================================
样本: windows/vmp-crackmes/Inside-the-Machine/crackme.exe
架构:
  - 24KB 极简自定义虚拟机 (8 个 32 位虚拟寄存器, 14 种字节码算子)
  - 动态滚动密钥 Opcode 置换: v8 = byte_140005520[(v3 ^ raw) & 0xff], v3 = v8 + 33*v3 + 7
  - 26 组单字符代数约束方程 + 全局 Rolling Hash 终检
"""

import sys, struct, subprocess

def rol32(v, n):
    n %= 32
    return ((v << n) | (v >> (32 - n))) & 0xFFFFFFFF

def solve_password():
    solved = []
    for idx in range(26):
        found = None
        for b in range(256):
            r1 = b
            if idx == 0:
                r1 = (r1 * 0x0e93b22d) & 0xFFFFFFFF
                r1 = rol32(r1, 19)
                r1 ^= 0xaca59a4b
                r1 = (r1 * 0xdd4a3bff) & 0xFFFFFFFF
                if (r1 ^ 0x2b2df55b) == 0: found = b; break
            elif idx == 1:
                r1 = (r1 + 0x038afe1b) & 0xFFFFFFFF
                r1 = rol32(r1, 28)
                if (r1 ^ 0xc038afe4) == 0: found = b; break
            elif idx == 2:
                r1 ^= 0x13eb0d9f
                r1 = rol32(r1, 24)
                if (r1 ^ 0xed13eb0d) == 0: found = b; break
            elif idx == 3:
                r1 = (r1 * 0x11312afb) & 0xFFFFFFFF
                r1 = (r1 + 0x7a982591) & 0xFFFFFFFF
                r1 = rol32(r1, 11)
                r1 ^= 0x5ade3969
                r1 = rol32(r1, 24)
                if (r1 ^ 0x4fa62453) == 0: found = b; break
            elif idx == 4:
                r1 = rol32(r1, 2)
                r1 = (r1 * 0x4fdd4eeb) & 0xFFFFFFFF
                r1 = (r1 * 0xc287ecd3) & 0xFFFFFFFF
                r1 = rol32(r1, 16)
                if (r1 ^ 0x2f9417a5) == 0: found = b; break
            elif idx == 5:
                r1 = (r1 + 0xfbc74806) & 0xFFFFFFFF
                r1 = rol32(r1, 28)
                r1 ^= 0xf540a17e
                r1 ^= 0x1842824d
                r1 = rol32(r1, 14)
                if (r1 ^ 0x95ec10af) == 0: found = b; break
            elif idx == 6:
                r1 = (r1 + 0xba010a2a) & 0xFFFFFFFF
                r1 = rol32(r1, 18)
                r1 = rol32(r1, 13)
                if (r1 ^ 0x5d00854b) == 0: found = b; break
            elif idx == 7:
                r1 = (r1 + 0x3b0cdb36) & 0xFFFFFFFF
                r1 ^= 0x8a89413f
                r1 ^= 0xb169dce2
                r1 = (r1 + 0xd0f50734) & 0xFFFFFFFF
                if (r1 ^ 0xd1e14d92) == 0: found = b; break
            elif idx == 8:
                r1 ^= 0x2a781277
                r1 ^= 0x891af2a9
                r1 = (r1 + 0x6fb17ba4) & 0xFFFFFFFF
                r1 ^= 0x46bdf7af
                if (r1 ^ 0x55a9ab21) == 0: found = b; break
            elif idx == 9:
                r1 = rol32(r1, 22)
                r1 = rol32(r1, 22)
                r1 = rol32(r1, 6)
                if (r1 ^ 0x018c0000) == 0: found = b; break
            elif idx == 10:
                r1 = (r1 * 0x24ba4587) & 0xFFFFFFFF
                r1 ^= 0x8f37d80b
                r1 = (r1 + 0x129fcaa0) & 0xFFFFFFFF
                r1 ^= 0x312f4df3
                r1 = rol32(r1, 11)
                if (r1 ^ 0xa7e40230) == 0: found = b; break
            elif idx == 11:
                r1 = rol32(r1, 3)
                r1 = (r1 + 0x64a3435c) & 0xFFFFFFFF
                r1 ^= 0x553f0fee
                r1 = (r1 + 0x37de1876) & 0xFFFFFFFF
                if (r1 ^ 0x697a6380) == 0: found = b; break
            elif idx == 12:
                r1 = rol32(r1, 25)
                r1 = (r1 + 0xf9c62b0e) & 0xFFFFFFFF
                if (r1 ^ 0xd5c62b0e) == 0: found = b; break
            elif idx == 13:
                r1 ^= 0xeb14d585
                r1 ^= 0xdf5b1af7
                r1 ^= 0x4f534a12
                r1 ^= 0xb13a7380
                r1 = rol32(r1, 21)
                if (r1 ^ 0xda7944de) == 0: found = b; break
            elif idx == 14:
                r1 = (r1 + 0x2b7fe8cf) & 0xFFFFFFFF
                r1 = (r1 + 0xbefdc56f) & 0xFFFFFFFF
                r1 = rol32(r1, 23)
                r1 ^= 0x27e06efd
                r1 = rol32(r1, 26)
                if (r1 ^ 0xa9a45540) == 0: found = b; break
            elif idx == 15:
                r1 = rol32(r1, 27)
                r1 = rol32(r1, 21)
                r1 ^= 0x12de73b9
                r1 = (r1 * 0x9d414f6d) & 0xFFFFFFFF
                if (r1 ^ 0xcba35cc5) == 0: found = b; break
            elif idx == 16:
                r1 ^= 0x623a401f
                r1 ^= 0xc0f904ea
                r1 = rol32(r1, 4)
                r1 = (r1 + 0xddceb5cb) & 0xFFFFFFFF
                if (r1 ^ 0x0a02ff85) == 0: found = b; break
            elif idx == 17:
                r1 = rol32(r1, 25)
                r1 ^= 0xb9d82b10
                if (r1 ^ 0x5fd82b10) == 0: found = b; break
            elif idx == 18:
                r1 = (r1 + 0x13f36bec) & 0xFFFFFFFF
                r1 = rol32(r1, 15)
                r1 = (r1 * 0x29c560af) & 0xFFFFFFFF
                r1 = (r1 + 0x87b99c69) & 0xFFFFFFFF
                if (r1 ^ 0x8e0acda0) == 0: found = b; break
            elif idx == 19:
                r1 = (r1 + 0x1dbd4a3e) & 0xFFFFFFFF
                r1 = rol32(r1, 1)
                r1 = (r1 * 0x7f1a59e3) & 0xFFFFFFFF
                r1 = (r1 + 0x8ff178dc) & 0xFFFFFFFF
                r1 ^= 0x8c9100ca
                if (r1 ^ 0x32ee7d2e) == 0: found = b; break
            elif idx == 20:
                r1 = (r1 * 0x6814f013) & 0xFFFFFFFF
                r1 = (r1 + 0xeb51fde8) & 0xFFFFFFFF
                r1 ^= 0x9eb5ab16
                if (r1 ^ 0x39c87aa7) == 0: found = b; break
            elif idx == 21:
                r1 = rol32(r1, 1)
                r1 = (r1 * 0xd410d1a9) & 0xFFFFFFFF
                r1 ^= 0x48dacd89
                r1 = (r1 + 0xa57f5339) & 0xFFFFFFFF
                if (r1 ^ 0xd220aa20) == 0: found = b; break
            elif idx == 22:
                r1 = (r1 * 0xe9f8a65f) & 0xFFFFFFFF
                r1 ^= 0x8aeb6071
                r1 ^= 0xbc0fea1b
                if (r1 ^ 0x8474f4e4) == 0: found = b; break
            elif idx == 23:
                r1 ^= 0x05e4ccdd
                r1 = rol32(r1, 22)
                if (r1 ^ 0x3b417933) == 0: found = b; break
            elif idx == 24:
                r1 = (r1 + 0x7d62268a) & 0xFFFFFFFF
                r1 = (r1 * 0x80b9c88b) & 0xFFFFFFFF
                r1 ^= 0x06b4c251
                r1 = (r1 + 0xf3eabc51) & 0xFFFFFFFF
                r1 = (r1 + 0x86fda061) & 0xFFFFFFFF
                if (r1 ^ 0x41c586f7) == 0: found = b; break
            elif idx == 25:
                r1 = (r1 + 0x0c3acf15) & 0xFFFFFFFF
                r1 = (r1 + 0xb24ce875) & 0xFFFFFFFF
                r1 = (r1 + 0xf8b22965) & 0xFFFFFFFF
                if (r1 ^ 0xb739e125) == 0: found = b; break
        solved.append(found)

    pwd = bytes(solved).decode('ascii')
    return pwd

def verify(exe_path, pwd):
    print(f"[*] 针对样本执行验证: {exe_path}")
    print(f"[*] 输入 Password: {pwd}")
    cmd = ["wine", exe_path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate(input=pwd + "\n")
    combined = out + err
    print("=== 执行回显 ===")
    print(combined.strip())
    print(f"[*] 进程退出码: {p.returncode}")
    if p.returncode == 0 and "accepted" in combined:
        print("[+] 验证 100% 成功！")
    else:
        print("[-] 验证失败！")

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '/root/逆向测试/windows/vmp-crackmes/Inside-the-Machine/crackme.exe'
    pwd = solve_password()
    print(f"[+] 破译成功！Password: {pwd}")
    verify(target, pwd)
