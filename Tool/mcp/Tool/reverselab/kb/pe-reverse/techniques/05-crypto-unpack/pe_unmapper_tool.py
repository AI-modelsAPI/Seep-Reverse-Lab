#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pe_unmapper_tool.py — 内存 Dump PE 镜像解映射与对齐修复工具
=============================================================
作用：一键将内存中按页面对齐 (Virtual Layout) 展开的 PE Dump 文件，
      修复为可被 IDA Pro / Ghidra / x64dbg 正常反编译与加载的合规 PE 文件。

核心实现：
1. FileAlignment = SectionAlignment (0x1000 对齐规整)
2. PointerToRawData = VirtualAddress (节区头偏移同步)
3. 自动计算补全 SizeOfRawData 页面对齐
4. 修正实际内存 ImageBase 锚点
"""

import sys, os, struct, argparse

def unmap_and_fix_pe(input_path, output_path, new_image_base=None):
    data = bytearray(open(input_path, "rb").read())
    if len(data) < 64:
        raise ValueError("[-] 文件过小，不是有效 PE 文件")

    # 1. 解析 DOS Header
    e_magic = data[:2]
    if e_magic != b"MZ":
        print(f"[!] 警告: 首字节非 MZ ({e_magic.hex()})，尝试自动修正 DOS 魔数...")
        data[0] = 0x4D; data[1] = 0x5A

    e_lfanew = struct.unpack_from("<I", data, 0x3c)[0]
    if e_lfanew + 4 > len(data) or data[e_lfanew:e_lfanew+4] != b"PE\x00\x00":
        raise ValueError(f"[-] 在偏移 0x{e_lfanew:x} 处未找到 PE 签名")

    # 2. 解析 File Header
    file_hdr_off = e_lfanew + 4
    machine, num_sections, _, _, _, opt_hdr_size, _ = struct.unpack_from("<HHIIIHH", data, file_hdr_off)
    print(f"[+] 识别有效 PE: Machine=0x{machine:x}, 节区总数={num_sections}, 可选头大小=0x{opt_hdr_size:x}")

    # 3. 解析 Optional Header
    opt_hdr_off = file_hdr_off + 20
    magic = struct.unpack_from("<H", data, opt_hdr_off)[0]
    is_64bit = (magic == 0x20B)
    print(f"[+] 位数判定: {'64-bit (PE32+)' if is_64bit else '32-bit (PE32)'}")

    section_alignment = struct.unpack_from("<I", data, opt_hdr_off + 32)[0]
    file_alignment_off = opt_hdr_off + 36
    old_file_alignment = struct.unpack_from("<I", data, file_alignment_off)[0]

    print(f"[+] 修改 FileAlignment: 0x{old_file_alignment:x} -> 0x{section_alignment:x} (与 SectionAlignment 同步)")
    struct.pack_into("<I", data, file_alignment_off, section_alignment)

    if new_image_base is not None:
        if is_64bit:
            struct.pack_into("<Q", data, opt_hdr_off + 24, new_image_base)
            print(f"[+] 重建 ImageBase (64-bit): -> 0x{new_image_base:016x}")
        else:
            struct.pack_into("<I", data, opt_hdr_off + 28, new_image_base & 0xFFFFFFFF)
            print(f"[+] 重建 ImageBase (32-bit): -> 0x{new_image_base:08x}")

    # 4. 遍历并修复所有 Section Headers
    sec_hdr_start = opt_hdr_off + opt_hdr_size
    print(f"[+] 遍历并修复 {num_sections} 个节区头...")
    for i in range(num_sections):
        sec_off = sec_hdr_start + (i * 40)
        name = data[sec_off:sec_off+8].rstrip(b'\x00').decode('latin1', errors='ignore')
        vsize, vaddr, rawsize, rawptr = struct.unpack_from("<IIII", data, sec_off + 8)

        # 核心算法: 内存展开的节区，其物理文件偏移直接对等为虚拟内存地址 (VirtualAddress)
        new_rawptr = vaddr
        # 将原始大小对齐到页面边界向上取整
        align = section_alignment if section_alignment > 0 else 0x1000
        new_rawsize = rawsize
        if new_rawsize % align != 0:
            new_rawsize = align * (1 + new_rawsize // align)
        if new_rawsize == 0 and vsize > 0:
            new_rawsize = align * (1 + vsize // align)

        print(f"    - 节区 #{i} [{name:8s}]: PointerToRawData (0x{rawptr:x} -> 0x{new_rawptr:x}), SizeOfRawData (0x{rawsize:x} -> 0x{new_rawsize:x})")
        struct.pack_into("<II", data, sec_off + 16, new_rawsize, new_rawptr)

    # 5. 校验并写出修复后文件
    open(output_path, "wb").write(data)
    print(f"[🎉] 修复完成！已生成可供反编译器解析的完整 PE: {output_path} (大小: {len(data)} 字节)")

def main():
    p = argparse.ArgumentParser(description="内存 Dump PE 镜像解映射与对齐修复工具")
    p.add_argument("input", help="输入的内存 Dump PE 二进制文件 (.bin / .exe)")
    p.add_argument("-o", "--output", required=True, help="输出修复后的 PE 文件路径")
    p.add_argument("--base", type=lambda x: int(x, 16), help="可选指定的实际内存加载基址 (十六进制，如 0x400000)")
    args = p.parse_args()

    unmap_and_fix_pe(args.input, args.output, args.base)

if __name__ == "__main__":
    main()
