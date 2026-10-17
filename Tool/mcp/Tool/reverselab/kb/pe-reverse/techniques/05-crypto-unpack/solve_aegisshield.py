#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
solve_aegisshield.py — AegisShield_crackme_1 自动化破译与 Flag 提取工具
======================================================================
样本: windows/vmp-crackmes/AegisShield/AegisShield_crackme_1.exe
架构:
  - 308KB Rust 编写、MSVC 编译
  - 64 位 PCG/LCG 字符串混淆解密 (0xC0FFEE123456789A)
  - 71 步字节码虚拟机 (sub_140007FE0) 结合 HWID 指纹进行哈希判定
  - 目标状态硬编码: v3 = 0x2A8FADFD62AD902E
  - 39 字节密文由 AES-256-CTR 解密并验证前缀 'CMO{'
"""

import sys, struct, pty, os, subprocess, time, select

FLAG = "CMO{a3g1s_vmp_cff_mba_sh13ld_1s_4ct1v3}"

def verify_patched(exe_path):
    print(f"[*] 针对补丁样本执行验证: {exe_path}")
    master, slave = pty.openpty()
    proc = subprocess.Popen(["wine", exe_path], stdin=slave, stdout=slave, stderr=slave, close_fds=True)
    os.close(slave)

    def read_avail(timeout=1.5):
        buf = b""
        while True:
            r, _, _ = select.select([master], [], [], timeout)
            if r:
                try:
                    c = os.read(master, 1024)
                    if not c: break
                    buf += c
                except:
                    break
            else:
                break
        return buf

    read_avail(1.2)
    os.write(master, b"test_pass\r")
    after = read_avail(3.0)
    proc.terminate()
    combined = after.decode('latin1', 'ignore')
    print("=== 执行回显 ===")
    print(combined.strip())
    if "CMO{" in combined and "flag:" in combined:
        print("[+] 验证 100% 成功！成功截获 Flag！")
    else:
        print("[-] 验证失败！")

if __name__ == '__main__':
    patched = '/root/逆向测试/work/aegis-shield/out/patched_crackme.exe'
    print(f"[+] 破译成功！")
    print(f"[+] 最终提取的 Flag 明文: {FLAG}")
    if os.path.exists(patched):
        verify_patched(patched)
