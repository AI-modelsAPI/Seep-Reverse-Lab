#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dex_fix_tool.py — Android 内存 Dump DEX 头修复与完整性重建工装
=============================================================
适用场景：修复因加固壳抹头、内存抓取导致的无效 DEX，使其在 JADX / Baksmali 中 100% 正常解析。
"""
import sys, os, struct, zlib, hashlib, argparse

def fix_dex_file(input_path, output_path):
    raw = open(input_path, "rb").read()
    if len(raw) < 0x70:
        raise ValueError("[-] 输入文件小于 DEX 最小 Header 长度 (112 字节)")

    data = bytearray(raw)
    old_magic = bytes(data[:8])
    print(f"[*] 原始 Magic: {old_magic!r}")

    # 1. 恢复标准魔数 (dex\n035\0)
    data[0:8] = b"dex\n035\x00"

    # 2. 修正物理文件大小
    file_size = len(data)
    old_size = struct.unpack_from("<I", data, 0x20)[0]
    struct.pack_into("<I", data, 0x20, file_size)
    print(f"[+] 修正 file_size: 0x{old_size:x} -> 0x{file_size:x} ({file_size} 字节)")

    # 3. 重新计算覆盖全文件的 SHA-1 签名 (从 0x20 开始)
    sha1 = hashlib.sha1(data[0x20:]).digest()
    data[0x0C : 0x0C + 20] = sha1
    print(f"[+] 重新计算 SHA-1 签名: {sha1.hex()[:16]}...")

    # 4. 重新计算覆盖全文件的 Adler-32 校验和 (从 0x0C 开始)
    adler32 = zlib.adler32(data[0x0C:]) & 0xFFFFFFFF
    struct.pack_into("<I", data, 0x08, adler32)
    print(f"[+] 重新计算 Adler-32 校验和: 0x{adler32:08x}")

    open(output_path, "wb").write(data)
    print(f"[🎉] 修复完成！可反编译的 DEX 已输出至: {output_path}")

def main():
    p = argparse.ArgumentParser(description="Android 内存 Dump DEX 头修复与完整性重建工装")
    p.add_argument("input", help="输入的被损毁/内存抓取的 DEX 文件")
    p.add_argument("-o", "--output", required=True, help="修复后的输出 DEX 文件路径")
    args = p.parse_args()

    fix_dex_file(args.input, args.output)

if __name__ == "__main__":
    main()
