---
id: "pe-reverse/05-crypto-unpack/05-high-entropy-compression-vs-crypto-routing"
title: "高熵数据鉴别与无头解压/解密自动化路由手册"
title_en: "High-Entropy Data Identification and Headless Decompression/Decryption Routing"
summary: >
  针对二进制逆向中遇到的高熵（>7.5）未知数据块，提供 5 步精确判定决策树（区分压缩 vs 对称加密 vs 伪随机数 vs 多媒体），
  包含 raw-deflate、zlib、gzip、lz4、zstd、snappy、brotli 的无头试探法，以及常见 S-Box 与魔改算法特征识别，
  彻底解决将压缩流误判为加密导致的逆向陷入死循环问题。
summary_en: >
  Decision tree and automated carving pipeline to distinguish compression streams from symmetric encryption
  in high-entropy binary regions (>7.5). Covers headless probing for raw-deflate, zlib, gzip, lz4, zstd,
  snappy, brotli, and crypto S-box/T-table detection to prevent anti-analysis false routes.
board: "pe-reverse"
category: "05-crypto-unpack"
signals:
  - "高熵数据块 (>7.5)"
  - "未知加密流"
  - "raw deflate"
  - "zlib 78 9c 78 01 78 5e"
  - "lz4 magic 04 22 4d 18"
  - "zstd magic 28 b5 2f fd"
  - "AES SBox / Te0"
  - "T-Table"
  - "ChaCha20 expand 32-byte k"
mcp_tools:
  - "seep_r2_cmd"
  - "seep_r2_disasm"
  - "kb_router"
difficulty: "advanced"
tags:
  - "pe"
  - "entropy"
  - "crypto"
  - "compression"
  - "deflate"
  - "carving"
evidence: "verified"
validated_by: "实测于 FLARE-On 12 UnholyDragon 与典型混淆样本"
language: "zh-CN"
last_updated: "2026-10-15"
related_articles:
  - "pe-reverse/05-crypto-unpack/01-pe-unpack-dump"
  - "pe-reverse/05-crypto-unpack/04-twinbasic-compressed-resource-recovery"
---
# 高熵数据鉴别与无头解压/解密自动化路由手册

## 1. 痛点与核心定性模型

在二进制安全分析中，遇到未命名的连续大块数据（几十 KB 到数 MB，信息熵在 7.5~7.99 之间），**绝不能凭直觉假定为加密（AES/RC4/ChaCha20）**。
现实中 70% 的高熵区实际上是**内嵌资源压缩（raw DEFLATE / LZ4 / ZSTD / 序列化表单）**。如果按密码学去找 S 盒、密钥、XOR 循环，会彻底陷入逻辑泥潭。

### 5 步判定决策树

```text
高熵数据块 (Entropy > 7.5)
  │
  ├─ 1. 局部自相关与字节频率检测 (Chi-Square & Autocorrelation)
  │     ├─ 极度均匀，无频次倾斜 (Chi-Square p > 0.05) ──▶ 大概率为现代对称加密或真随机流
  │     └─ 存在局部偏斜 (存在频次 > 均值 3 倍的字节，或局部相邻差值规律) ──▶ 大概率为压缩流/多媒体
  │
  ├─ 2. 压缩魔数探测 (Magic Header Probing)
  │     ├─ 0x1F 0x8B ──────▶ Gzip
  │     ├─ 0x78 0x01/5E/9C/DA ▶ Zlib Stream
  │     ├─ 0x04 0x22 0x4D 0x18 ▶ LZ4 Frame
  │     ├─ 0x28 0xB5 0x2F 0xFD ▶ ZSTD Frame
  │     └─ 0x42 0x5A 0x68 ──▶ Bzip2 ("BZh")
  │
  ├─ 3. 无头流启发式试探 (Headless Stream Probing - 关键突破点)
  │     └─ 当没有标准魔数时，按滑动窗口测试 raw DEFLATE (wbits = -15)、Snappy、Brotli
  │
  ├─ 4. 加密算法特征签名交叉检验 (Crypto S-Box / Constants)
  │     └─ 扫描全局内存/节区是否存在密码学结构（AES Te 表、SHA-256 IV、RC4 初始化）
  │
  └─ 5. 解码验证与证据化落地
```

---

## 2. 压缩格式“无头（Headless）”解压探测标准

当外部封装格式（如 TwinBasic、自定义打包器）剥离了压缩格式的标准文件头，直接存储原始压缩流时，必须使用**无头解压模式**。

### 核心 Python 试探套件

```python
import zlib

def probe_headless_deflate(data, max_probe_len=65536):
    """
    针对无 78 9C 等魔数的 raw DEFLATE 进行滑动试探。
    wbits=-15 告诉底层 zlib 跳过 header 与 adler32 校验。
    """
    for offset in range(min(len(data), 128)):
        chunk = data[offset:offset + max_probe_len]
        try:
            decompressor = zlib.decompressobj(-15)
            decompressed = decompressor.decompress(chunk)
            if len(decompressed) > 1024:
                return {
                    "format": "raw-deflate",
                    "offset": offset,
                    "decompressed_size": len(decompressed),
                    "unused_bytes": len(decompressor.unused_data)
                }
        except Exception:
            continue
    return None
```

---

## 3. 常见密码学特征常量与 S 盒速查表

如果在二进制的只读数据节（`.rdata`, `.rodata`）或代码立即数中命中以下常量，则判定存在加密调用：

| 算法 | 经典特征常量 / S 盒起始字节 (Hex) | 内存模式 |
|---|---|---|
| **AES S-Box** | `63 7C 77 7B F2 6B 6F C5 30 01 67 2B FE D7 AB 76` | 连续 256 字节只读查找表 |
| **AES Inv S-Box** | `52 09 6A D5 30 36 A5 38 BF 40 A3 9E 81 F3 D7 FB` | 连续 256 字节逆表 |
| **AES Te0 (T-Table)** | `C6 63 63 A5 F8 7C 7C 84 EE 77 77 99 F6 7B 7B 8D` | 1024 字节优化查表加速结构 |
| **MD5 Init State** | `01 23 45 67 89 AB CD EF FE DC BA 98 76 54 32 10` | 4 个 32-bit 寄存器初始向量 |
| **SHA-256 K 常量** | `42 8A 2F 98 71 37 44 91 B5 C0 FB CF E9 B5 DB A5` | 64 个立方根小数部分的 32-bit 常量表 |
| **SM4 S-Box** | `D6 90 E9 FE CC E1 3D B7 16 B6 14 C2 28 FB 2C 05` | 国密 SM4 8位非线性置换表 |
| **ChaCha20 Constant** | `"expand 32-byte k"` (`65 78 70 61 6E 64 20 33 32 2D 62 79 74 65 20 6B`) | 16 字节固定矩阵初始化字串 |

---

## 4. 配套自动化提取工装：`entropy_carver_tool.py`

同目录下自带自动化分析工具，一键执行：
1. 熵曲线分析与分块报告；
2. 8 种主流解压算法自动切片试探；
3. 密码学常量与结构扫描。

```bash
python3 entropy_carver_tool.py sample.bin --outdir extracted_streams/
```
