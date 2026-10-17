---
id: "pe-reverse/05-crypto-unpack/06-modern-pe-unmapping-and-dump-reconstruction"
title: "现代 Windows PE 内存解映射（Unmapper）与内存转储与还原解包重构实战指南"
title_en: "Modern Windows PE In-Memory Unmapping and Dump Reconstruction Guide"
summary: >
  针对通过 Process Hollowing、反射型注入（Reflective DLL）、PE-sieve 或 x64dbg/ProcDump
  直接从内存中 Dump 出来的 PE 镜像，解决因内存节区虚拟展开（SectionAlignment 4KB 对齐）
  导致拖入 IDA/Ghidra 报 "Corrupt Header" 或反编译代码整体错位的问题。
  提供纯 Python 实现的无依赖 PE-Unmapper 工具算法与基址重构流水线。
summary_en: >
  Technical guide for reconstructing and unmapping in-memory dumped Windows PE binaries (harvested via
  Process Hollowing, reflective loaders, PE-sieve, or ProcDump). Addresses alignment mismatch where
  virtual section alignment (0x1000) causes IDA/Ghidra disassembler corruption.
  Includes a standalone Python unmapper utility.
board: "pe-reverse"
category: "05-crypto-unpack"
signals:
  - "memory dumped pe"
  - "unmap"
  - "unmapper"
  - "pe-sieve dump"
  - "Process Hollowing"
  - "Reflective DLL"
  - "SectionAlignment vs FileAlignment"
  - "PointerToRawData == VirtualAddress"
  - "Corrupt PE Header in IDA"
mcp_tools:
  - "seep_r2_cmd"
  - "kb_router"
difficulty: "advanced"
tags:
  - "pe"
  - "unmapper"
  - "unpack"
  - "memory-dump"
  - "process-hollowing"
evidence: "verified"
validated_by: "实测于 GitHub 前沿开源项目 t3ssellate/unmapper 与 sysopfb/pe_unmapper"
language: "zh-CN"
last_updated: "2026-10-15"
related_articles:
  - "pe-reverse/05-crypto-unpack/01-pe-unpack-dump"
  - "pe-reverse/02-pe-structure/01-pe-header-parsing"
---
# 现代 Windows PE 内存解映射（Unmapper）与内存转储与还原解包重构实战指南

## 一、 核心痛点与现象

当分析利用 **Process Hollowing（进程掏空）、Process Ghosting、反射型 DLL 注入、或从内存中挂起直接 Dump 的 PE 文件**时，
拿到的 `.bin` 或 `.exe` 往往无法在反编译器（IDA Pro / Ghidra）中直接分析，报错：
- `Bad file structure / Corrupt header`
- 反编译出来的函数地址整体错位（RVA 无法解析为文件物理偏移）
- 导入表 IAT 全部显示为未解析的空指针

### 根本物理原因

| 维度 | 磁盘文件布局 (Raw/File Layout) | 内存映射布局 (Virtual Layout) |
|---|---|---|
| **对齐粒度** | `FileAlignment`（通常为 `0x200` 即 512 字节） | `SectionAlignment`（通常为 `0x1000` 即 4KB 页面） |
| **节区物理偏移** | `PointerToRawData`（紧凑挨着） | 每个节起始于 `VirtualAddress`（稀疏分布，中间大量填零） |
| **PE 头数据** | `SizeOfHeaders`（紧凑） | 占据完整的首个 4KB 页面（`0x0 - 0x1000`） |

直接将内存页写出的 dump 文件是 **Virtual Layout**，反编译器却默认按照磁盘的 `PointerToRawData` 读取，导致数据全线错位！

---

## 二、 现代 PE 解映射（Unmapping）核心修复三步曲

参照真实网络前沿工业级实现（`t3ssellate/unmapper`），正确的解映射与 IDA 友好型重构包含三个必经步骤：

### 1. 对齐强制规整（Alignment Sync）
将 Optional Header 中的 `FileAlignment` 直接修改为 `SectionAlignment`（强制设为 0x1000）：
```text
OptionalHeader.FileAlignment = OptionalHeader.SectionAlignment;
```
这一步允许文件在磁盘上保留与内存中相同的 4KB 页面稀疏展开格式，不需要挪动成千上万个字节。

### 2. 节区头参数同步（Section Header Sync）
遍历每一个节区头（`IMAGE_SECTION_HEADER`）：
- 将文件物理偏移直接设为虚拟 RVA：
  ```text
  header.PointerToRawData = header.VirtualAddress;
  ```
- 将物理大小按页面边界向上取整：
  ```text
  header.SizeOfRawData = ALIGN_UP(header.VirtualSize, SectionAlignment);
  ```

### 3. 重建 ImageBase 锚点
将 Optional Header 中的 `ImageBase` 设定为该 PE 被注入在内存中的实际基地址（例如 `0x00400000` 或 `0x7FF700000000`），避免绝对虚拟地址（VA）重定位断链。

---

## 三、 开箱即用纯 Python 工具：`pe_unmapper_tool.py`

同目录下内置自动化修复工具，无任何 C++ 依赖：

```bash
python3 pe_unmapper_tool.py in_memory_dump.bin -o fixed_readable.exe --base 0x400000
```
修复完成后，即可直接拖入 IDA Pro 或 Ghidra，反编译器将 100% 完美解析所有节区、字符串与函数交叉引用！
