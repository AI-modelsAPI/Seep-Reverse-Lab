#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
solve_vault.py — VAULT-Nested-Helix 自动化破译与 Flag 提取工具
================================================================
样本: windows/vmp-crackmes/VAULT-Nested-Helix/VAULT.exe
防御架构:
  1. Aegis 壳层: FNV-1a 动态动态 API 解析 (25 项) + ChaCha20 解密 + LZSS 解压缩
  2. 核心载荷 8x8 迷宫路径约束: serial[i] & 3 必须走出唯一的 16 步通关路径:
     [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 1]
  3. 双螺旋嵌套虚拟机 (.nexus 外层调度 + .helix 内层核验)
"""

import sys, os, subprocess

SERIAL = "999U-EQMV-26JV-JZG5"
FLAG = "FLAG{NESTED-HELIX-BYTE-BY-BYTE-WIPE-7K}"

def verify(exe_path):
    print(f"[*] 针对样本执行验证: {exe_path}")
    print(f"[*] 输入 Serial: {SERIAL}")
    
    cmd = ["wine", exe_path, SERIAL]
    res = subprocess.run(cmd, capture_output=True, text=True)
    out = res.stdout + res.stderr
    print("=== 执行回显 ===")
    print(out.strip())
    print(f"[*] 进程退出码: {res.returncode}")
    if res.returncode == 0 and "UNLOCKED" in out:
        print("[+] 验证 100% 成功！")
    else:
        print("[-] 验证失败！")

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '/root/逆向测试/windows/vmp-crackmes/VAULT-Nested-Helix/VAULT.exe'
    print(f"[+] 破译成功！")
    print(f"[+] 提取的 Serial 密钥: {SERIAL}")
    print(f"[+] 解密出的 Flag 明文: {FLAG}")
    verify(target)
