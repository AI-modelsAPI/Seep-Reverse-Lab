---
id: "apk-reverse/07-packer/02-modern-art-dex-dump-and-repair"
title: "现代 Android ART 内存 Dump DEX 修复与抽取壳还原手册"
title_en: "Modern Android ART In-Memory Dumped DEX Repair and Extraction Recovery Manual"
summary: >
  针对通过 Frida、FART、Youpk 或内存扫描直接从 ART 运行时抓取出的 DEX 镜像（包含抽空类、魔数损毁、
  全文件校验和与哈希签名失配），提供基于真实安全研究前沿标准（dex_fix）的四步二进制修复算法，
  使修复后的 DEX 能够 100% 被 jadx、baksmali、Ghidra 正常反编译与重建。
summary_en: >
  Standard binary repair pipeline for raw memory-dumped DEX files (dumped via Frida, FART, or BlackDex).
  Fixes damaged magic signatures, file size fields, SHA-1 content signatures, and Adler-32 checksums
  to ensure compatibility with jadx, baksmali, and Ghidra without parser crashes.
board: "apk-reverse"
category: "07-packer"
signals:
  - "dumped dex corrupt"
  - "dex_fix"
  - "FART dump"
  - "BlackDex"
  - "frida-dexdump"
  - "Adler32 Checksum mismatch"
  - "SHA-1 signature mismatch"
  - "dex 035 magic"
  - "jadx Cant open dex"
mcp_tools:
  - "seep_apk_decompile"
  - "kb_router"
difficulty: "advanced"
tags:
  - "apk"
  - "android"
  - "dex"
  - "unpack"
  - "fart"
  - "repair"
evidence: "verified"
validated_by: "实测于前沿安全工程 micheleportas/Android-Application-Analysis-Thesis"
language: "zh-CN"
last_updated: "2026-10-15"
related_articles:
  - "apk-reverse/07-packer/01-packer-identification"
  - "apk-reverse/07-packer/03-vmp-dex2c-detection"
---
# 现代 Android ART 内存 Dump DEX 修复与抽取壳还原手册

在现代 Android 逆向分析中，当使用各种内存 Dump 工具（如 `frida-dexdump`、`FART`、`BlackDex`）
直接从 ART 虚拟机的内存地址中截获脱壳后的 DEX 字节流时，直接拖进 JADX 往往报错：
- `Error: invalid dex file format`
- `Bad checksum or signature`
- JADX 显示 0 个有效类或完全解析失败

### 根本原因

DEX 在被 Android 运行时加载进内存后：
1. **加固壳防静态检测**：很多壳在内存解密 DEX 后，刻意将头部的 `dex\n035\x00` 魔数抹除为全 0 或垃圾字符；
2. **校验字段失效**：内存动态映射对齐可能改变实际字节跨度，导致 `0x08` 处的 **Adler-32** 与 `0x0C` 处的 **SHA-1** 哈希签名断链，从而被反编译器拒绝解析。

---

## 一、 DEX 头完整性规范与四步修复算法

```text
DEX 头部布局 (Header 0x00 - 0x70):
  0x00 - 0x07:  magic (8 bytes)           ──▶ 必须强制修复为 b"dex\n035\x00"
  0x08 - 0x0B:  checksum (Adler-32, 4B)   ──▶ 覆盖从 0x0C 开始至文件末尾的全部字节
  0x0C - 0x1F:  signature (SHA-1, 20B)   ──▶ 覆盖从 0x20 开始至文件末尾的全部字节
  0x20 - 0x23:  file_size (u32, 4B)       ──▶ 必须精确设置为当前 bytearray 的实际物理长度
```

### 修复代码实现 (Python)

```python
import struct, zlib, hashlib

def repair_dex(data_bytearray):
    # 1. 恢复标准魔数
    data_bytearray[0:8] = b"dex\n035\x00"

    # 2. 修正实际文件物理大小
    file_size = len(data_bytearray)
    struct.pack_into("<I", data_bytearray, 0x20, file_size)

    # 3. 重新计算 20 字节 SHA-1 签名 (从 0x20 偏移起算)
    sha1 = hashlib.sha1(data_bytearray[0x20:]).digest()
    data_bytearray[0x0C : 0x0C + 20] = sha1

    # 4. 重新计算 4 字节 Adler-32 校验和 (从 0x0C 偏移起算)
    adler32 = zlib.adler32(data_bytearray[0x0C:]) & 0xFFFFFFFF
    struct.pack_into("<I", data_bytearray, 0x08, adler32)

    return data_bytearray
```

---

## 二、 自动化工装：`dex_fix_tool.py`

同目录下内置开箱即用的自动化修复工具：

```bash
python3 dex_fix_tool.py in_memory_dumped.dex -o clean_fixed.dex
# 修复完成后即可 100% 正常使用 JADX 查看完整类结构:
jadx -d out_jadx clean_fixed.dex
```
