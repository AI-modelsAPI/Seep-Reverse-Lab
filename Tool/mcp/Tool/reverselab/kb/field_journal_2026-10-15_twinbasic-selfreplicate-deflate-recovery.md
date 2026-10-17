---
id: "field_journal_2026-10-15_twinbasic-selfreplicate-deflate-recovery"
title: "2026-10-15 TwinBasic 自复制样本：压缩资源还原 + 图内 flag 提取"
evidence: "verified"
validated_by: "实战记录（含样本与实践过程）"
---
# 2026-10-15 TwinBasic 自复制样本：压缩资源还原 + 图内 flag 提取

## 场景分类

Windows PE 逆向 / twinBASIC(VB6 语法) / 高熵区误判为加密 / 自我复制反分析 / 图内文字识别

## 目标概述

对 FLARE-On 12 Challenge 4（`UnholyDragon-150.exe`，2.7MB，twinBASIC 编译）
做只读白盒分析：修复被破坏的 DOS 头、识别 `.data` 高熵区为 raw DEFLATE 非加密、
解出内嵌 Form 序列化数据与 1024×1024 图片资源、在 Wine 下恢复 GUI 显示、
从第 148 代实例解出的图中提取 flag 文本。
全程不修改原始样本（仅副本操作），凭据类数据未记录。

## 完整执行链路

1. `file` 报 `data`，读头部发现首 2 字节 `15 5A`（非 `MZ`）→ 判为**人为破坏 DOS 头**。
   校验 `e_lfanew(0x3C)` 处 `PE\0\0` 完好，PE 结构与段表正常。
2. 读导入表：`OLEAUT32` 的 `VarAdd/VarIdiv/VarRound/SafeArrayGetVartype/LoadTypeLib`
   + `ThunderRT6FormDC`/`VB.Timer` 字符串 → 判定 **VB6/twinBASIC 原生 PE**（非 .NET）。
3. 用 4KB 窗口熵扫描定位 `.data` 内 **1.8MB 连续熵 7.97 区**。
   搜索单/双字节 XOR、AES-ECB 块重复 → 全部无效 → **放弃"加密"假设**。
4. 反编译入口 `0x402587`：`lea eax,[0x4b09a8]; shl dword [eax],2` + 后续初始化；
   在入口附近发现 `push 0x4b20a8; call 0x46fe5c`，`0x46fe5c` 内含
   `call 0x46fca3`（Huffman 码表初始化）+ `0x46fabc`（inflate 位读取器）
   → **确认是 DEFLATE 解压器**。
5. 解析描述符 `0x4b20a8`：`[size0=1838690][size1=1839781][deflate data]`。
   用 `zlib.decompressobj(-15)` 从 `+8` 解压 → **得 1,839,781 字节**（== size1，验证成功）。
6. 解析解压产物：`[ver][len][field][payloadSize]` + GUID + `Form1`/`Segoe UI` 字符串
   + **PNG magic `89 50 4E 47`**（`Image1`，1024×1024 RGBA）+ 控件属性表（`05`+double 常量）。
7. 提取 PNG：发现 29 个 `IDAT` 块按 `0x10000` 边界切分，**首块长度字段 65445 是假的**；
   改为"每块到下一个 IDAT 之前"拼接 + raw inflate + `LOAD_TRUNCATED_IMAGES` 成功解码。
8. 静态线暂停（Form 空白）；转动态：装 Wine32 + 原生 `oleaut32`，
   `oleaut32=native` + `ole32=builtin`，`winedbg` 反复 `pass` 忽略异常。
9. 观察自我复制：程序读**自身文件名** `UnholyDragon-N.exe` → 复制为 `N+1` 并启动，
   **每代只改 1 字节**；变异 **#150 破坏 DOS 头首字节**（自锁）。
10. 程序稳定跑到**第 148 代**并创建 24 个 `Form1`（1172×766）。解第 148 代实例：
    其变异改变了压缩块 → **解出图像与原始样本不同（差 165 万字节）**，
    该图中**含 flag 文字**。
11. 识别文字：逐列投影切出 34 个字符段 → 二值化/反色/放大 → 多 PSM OCR；
    对摇摆字符用**字形签名匹配**（未知段与已知 `d3ntal` 的 `t` 逐行宽度轮廓完全一致）
    → 确定为 `t`。
12. 交付：解密脚本、解出图像、字形签名验证报告、flag 明文。

## 踩坑记录

| 问题 | 原因 | 解决方案 | 耗时 |
|---|---|---|---|
| `file` 报 `data`，pefile 报 `DOS Header magic not found` | DOS 头被改成 `15 5A` | 手工修 10 个字节即可，PE 结构未动 | 低 |
| 高熵 1.8MB 区各种 XOR/AES 都解不开 | **误当作加密，其实是 raw DEFLATE** | 反编译入口找到 inflate 调用，改用 `wbits=-15` | **高** |
| 标准 `zlib.decompress` 报 `incorrect data check` | Adler32 尾被改 | 用 `decompressobj(-15)` 忽略校验 | 中 |
| PNG 报 `unrecognized data stream` | 29 个 IDAT 块长度字段被改，块边界错位 | 按"到下一个 IDAT 前"拼接 + `LOAD_TRUNCATED_IMAGES` | 高 |
| Wine 下弹 `twinBASIC Internal Error: Failed to deserialize form` | Wine 内置 `oleaut32` 的 `OleLoadPictureEx` 不支持 `IPicture` | `winetricks -q oleaut32` 装原生 | 中 |
| 设 `ole32=native` 后全线 `import_dll not found` | 原生 ole32 依赖链复杂，缺失 DLL | **改为 ole32=builtin**（只 oleaut32 用 native） | 中 |
| 程序反复在同地址崩溃，进程秒退 | VB6 用异常做控制流，Wine 当致命错误 | `winedbg` + `yes pass` 反复忽略 | 中 |
| X 报 `Maximum number of clients reached` | 大量测试实例占满 X 客户端 | 重启 Xvfb，清理僵尸进程 | 低 |
| 静态反复在运行时噪声函数里打转 | twinBASIC 用户代码与运行时混编 | 转向"**解资源**"而非"读代码" | 高 |
| OCR 对 `s3ru?ce` 反复给出 `t`/`i`/`l` | 自绘艺术字体，OCR 不稳 | **字形签名匹配**数学确定 | 中 |

## 工具链发现

- **熵高 ≠ 加密**：raw DEFLATE 的熵就是 7.9+。**先试 `wbits=-15`**，再考虑加密。
- **DOS 头破坏**是廉价的"让工具打不开"手法；`PE\0\0` 完好即可放心修复。
- **twinBASIC** 区块描述符形如 `[size0][size1][deflate]`，入口附近有 inflate 调用链可定位。
- **Wine 跑 VB6/twinBASIC**：`oleaut32=native` + `ole32=builtin` 是关键组合；
  异常驱动控制流必须用 `winedbg` 的 `pass`。
- **`LOAD_TRUNCATED_IMAGES=True`** 能救"CRC 被改但数据完好"的 PNG。
- **字形签名匹配**（逐行宽度轮廓）是 OCR 摇摆时的确定性仲裁手段。
- 自我复制 + 逐字节变异**大多是反分析噪声**；真正载荷在资源里，
  且**变异会改变解出的资源**，需**试多代**。

## 关键代码/命令

```python
# 1) 定位并解压 twinBASIC raw-DEFLATE 块
import struct, zlib
desc_off = 0xa9200 + (0x4b20a8 - 0x4aa000)     # .data 段 raw + (desc_va - sec_va)
size0, size1 = struct.unpack_from("<II", pe, desc_off)
payload = zlib.decompressobj(-15).decompress(pe[desc_off+8 : desc_off+8+size1])
assert len(payload) == size1

# 2) 提取内嵌 PNG（容错）
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
p  = payload.find(b'\x89PNG\r\n\x1a\n', 0x200)
ie = payload.find(b'IEND', p) + 8
open("Image1.png","wb").write(payload[p:ie])
im = Image.open("Image1.png"); im.load()

# 3) 字形签名匹配（仲裁 OCR 摇摆）
import numpy as np
def signature(mask, s, e):
    ch = mask[:, s:e+1]; ys,_ = np.nonzero(ch)
    ch = ch[ys.min():ys.max()+1, :]
    return tuple(int(np.where(ch[r])[0].max()-np.where(ch[r])[0].min()+1)
                 if ch[r].any() else 0 for r in range(ch.shape[0]))
# 已知 't'(段9) 与 未知段 签名相同 → 未知段 = 't'
```

```bash
# Wine 修复 VB6/twinBASIC COM
winetricks -q oleaut32
wine reg add "HKCU\\Software\\Wine\\DllOverrides" /v oleaut32 /t REG_SZ /d native  /f
wine reg add "HKCU\\Software\\Wine\\DllOverrides" /v ole32     /t REG_SZ /d builtin /f

# 忽略异常继续执行
yes pass | head -5000 > cmds.txt && winedbg prog.exe < cmds.txt

# 无头窗口取证
DISPLAY=:99 xwininfo -root -tree
DISPLAY=:99 xwd -id 0x<WID> -out w.xwd && convert w.xwd w.png
```

## 产出与指标

- 样本：`UnholyDragon-150.exe`（sha256 `4c22f5e4...`），DOS 头 `15 5A`（破坏）。
- 解压块：`size1=1839781`，解出同长；内嵌 `Image1` = 1838852 字节 PNG。
- 自复制链：1 → 148 代可用；第 150 代自锁（头被破坏）。
- flag：`dr4g0n_d3ntal_of_s3rutce@flare-on.com`
- 关键：**第 148 代解出的图才含 flag**（原始样本不含）——变异改变了解压结果。

## 沉淀

- 通用技术 → `kb/pe-reverse/techniques/05-crypto-unpack/04-twinbasic-compressed-resource-recovery.md`
  （含：DOS 头修复、描述符定位、raw DEFLATE 辨析、PNG 分块拼接、
  Wine oleaut32 修复、自复制样本处置、字形签名识别、误判清单）
