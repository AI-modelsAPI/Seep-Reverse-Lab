---
id: "pe-reverse/05-crypto-unpack/04-twinbasic-compressed-resource-recovery"
title: "TwinBasic/VB6 程序压缩资源还原与自复制样本分析"
title_en: "TwinBasic/VB6 Compressed Resource Recovery and Self-Replicating Sample Analysis"
summary: >
  针对 twinBASIC / VB6 编译的 Windows PE，识别 .data 段高熵区实为 raw-DEFLATE 压缩块（非加密），
  从 PE 描述符结构 [size0][size1][deflate](@ 0x4b20a8) 直接解压还原内嵌 Form 序列化数据与图片资源；
  并覆盖 "自我复制 + 逐字节变异" 型反分析样本的处置方法（文件名序号驱动、DOS 头自破坏）。
summary_en: >
  For twinBASIC/VB6-compiled Windows PEs, identify high-entropy .data regions that are actually
  raw-DEFLATE blocks (not encrypted), decompress via descriptor struct [size0][size1][deflate],
  and recover embedded Form serialization + image resources. Also covers remediation for
  self-replicating, one-byte-per-generation anti-analysis samples (filename-driven, DOS-header self-corruption).
board: "pe-reverse"
category: "05-crypto-unpack"
signals:
  - "高位熵 .data 段 (>7.9) 但非加密"
  - "twinBASIC"
  - "TWINBASIC.ICO"
  - "ThunderRT6FormDC"
  - "VB.Timer / VB.TextBox"
  - "DOS 头非 MZ (0x15 0x5A / 0x00 0x00)"
  - "UnholyDragon-N.exe 文件名序号"
  - "raw deflate 78 5E 头"
  - "Failed to deserialize form"
  - "OleLoadPictureEx"
keywords:
  - "twinBASIC"
  - "VB6"
  - "raw deflate"
  - "inflate"
  - "DOS header"
  - "self-replication"
  - "form deserialization"
  - "Wine oleaut32"
  - "PNG IDAT"
mcp_tools:
  - "seep_r2_info"
  - "seep_r2_decompile"
  - "seep_r2_cmd"
  - "kb_router"
difficulty: "advanced"
tags:
  - "pe"
  - "twinbasic"
  - "vb6"
  - "deflate"
  - "unpack"
  - "anti-analysis"
language: "zh-CN"
last_updated: "2026-10-15"
related_articles:
  - "pe-reverse/05-crypto-unpack/01-pe-unpack-dump"
  - "pe-reverse/02-pe-structure/01-pe-header-parsing"
  - "pe-reverse/04-dynamic-analysis/08-procmon-patterns"
evidence: "reproduced"
validated_by: "含可复现代码/命令"
---
# TwinBasic/VB6 程序压缩资源还原与自复制样本分析

> 适用：Windows PE，`.data` 段出现 1MB+ 极高熵区，导入表含 `OLEAUT32` 的
> `VarAdd/VarIdiv/VarRound/SafeArrayGetVartype/LoadTypeLib`，或 `file` 报 `data`（头部异常）。

## 1. 入口信号（30 秒判型）

| 现象 | 结论 |
|---|---|
| `file` 报 `data`；首 2 字节非 `4D 5A` | **DOS 头被人为破坏**，先修复（见 §2） |
| 导入表有 `OLEAUT32` Variant/SafeArray 大批函数 | **VB6 / twinBASIC 编译产物** |
| 二进制内出现 `ThunderRT6FormDC` / `VB.Timer` / `VB.TextBox` | VB6 运行时控件类名 |
| 出现 `twinBASIC` / `TWINBASIC.ICO` / `RootWindowElement` | twinBASIC（VB6 语法现代编译器） |
| `.data` 有 ~1.8MB 连续熵 `7.9+` 区 | **不是加密，80% 是 raw DEFLATE 压缩块** |

```text
# 快速熵扫描（定位高熵连续段）
python3 - <<'PY'
import math
from collections import Counter
d = open("sample.exe","rb").read()
def ent(b):
    if not b: return 0
    c = Counter(b); n = len(b)
    return -sum((v/n)*math.log2(v/n) for v in c.values())
W = 4096
seg = None
for off in range(0, len(d)-W, W):
    if ent(d[off:off+W]) > 7.5:
        if seg is None: seg = [off, off+W]
        else: seg[1] = off+W
    elif seg:
        print(f"高熵段 0x{seg[0]:x}-0x{seg[1]:x} ({seg[1]-seg[0]} bytes)")
        seg = None
if seg: print(f"高熵段 0x{seg[0]:x}-0x{seg[1]:x}")
PY
```

## 2. 修复被人为破坏的 DOS 头

很多样本把 `MZ`（`4D 5A`）改成别的值（如 `15 5A`），使加载器拒绝执行，
**只有程序自身（自我复制到下一代）才会写出正确头**。静态分析前先修好：

```python
d = bytearray(open("sample.exe","rb").read())
# 标准 DOS stub 头关键字节
for i, v in [(0,0x4D),(1,0x5A),(2,0x90),(3,0x00),(4,0x03),(5,0x00),
             (10,0x00),(11,0x00),(26,0x00),(27,0x00)]:
    d[i] = v
open("fixed.exe","wb").write(bytes(d))
```

> **判断技巧**：先看 `e_lfanew`（偏移 `0x3C`）处的 `PE\0\0` 是否完好。
> 若 PE 签名正确、仅 DOS stub 前几十字节异常 → 是**故意破坏头**，修复即可，PE 结构未动。

## 3. 定位压缩块描述符（核心）

twinBASIC/VB6 运行时把主数据块以 **raw DEFLATE** 存放，并在前面放一个描述符结构。

**描述符定位法**：入口点附近会有一条 `lea` + `shl` 指令指向元数据（如 `lea eax,[0x4b09a8]; shl dword [eax],2`），
该地址上下就是块描述符区；再在附近找形如 `[size0:4][size1:4][deflate data]` 的结构。

```python
import struct
# 例：描述符 VA 0x4b20a8，.data 段 VA 0x4aa000 / raw 0xa9200
desc_va  = 0x4b20a8
sec_va, sec_raw = 0x4aa000, 0xa9200
desc_off = sec_raw + (desc_va - sec_va)

d = open("fixed.exe","rb").read()
size0, size1 = struct.unpack_from("<II", d, desc_off)   # 两个相近的大小字段
print(f"size0={size0} size1={size1}")

# 关键：raw deflate = 跳过 2 字节 zlib 头，wbits = -15
import zlib
comp    = d[desc_off+8 : desc_off+8+size1]
payload = zlib.decompressobj(-15).decompress(comp)
assert len(payload) == size1        # 解压长度 == size1 即验证成功
print(f"[+] 解出 {len(payload)} bytes")
```

> **三种 zlib 模式辨析**（踩坑点）：
> - `78 5E / 78 01 / 78 9C / 78 DA` 开头 = **zlib（带 2 字节头）** → `wbits=15`（或 `-15` 跳过 2 字节）
> - 直接 `wbits=-15`（raw）用于**已跳过 2 字节**或裸 deflate
> - `wbits=31` 用于 gzip
> - **若报 `incorrect data check`**：说明 Adler32 尾被改，但**数据本身正确** → 用
>   `decompressobj(-15)` 或 `decompressobj(); out=...decompress(...)` 忽略校验仍能拿到数据。

## 4. 解析解压结果（twinBASIC Form 序列化）

解压产物典型结构：

```
[ver:4][len1:4][field2:4][payloadSize:4]     ← 头部（如 01 00 00 00 0e 00 00 00 ...）
[GUID:16]                                     ← 项目 GUID
"Form1\0" "Segoe UI\0" ...                    ← 元数据字符串（[len][text] 格式）
[PNG magic 89 50 4E 47] ... [IEND] ...        ← 内嵌图片资源（Image1）
[控件属性表: 浮点常量 05 + double8]            ← Left/Top/Width/Height 等
```

**提取内嵌 PNG**：

```python
p  = payload.find(b'\x89PNG\r\n\x1a\n', 0x200)   # 跳过头部
ie = payload.find(b'IEND', p) + 8
png = payload[p:ie]
open("Image1.png","wb").write(png)
```

**PNG 结构可能被"分块 + 假长度"处理**（Windows IStream 存储特征）：
`IDAT` 块每 `0x10000` 字节边界切分，**块长度字段可能对不上**，
需按"每块到下一个 IDAT 之前"的方式拼接，再 raw inflate：

```python
import re, struct, zlib
idats = [m.start() for m in re.finditer(b'IDAT', png_data)]
idat_all = b''
for j, p_ in enumerate(idats):
    if j+1 < len(idats):
        idat_all += png_data[p_+4 : idats[j+1]-4]
    else:
        ie = png_data.find(b'IEND', p_)
        idat_all += png_data[p_+4 : ie-4]
raw = zlib.decompressobj(-15).decompress(idat_all[2:])   # 跳过 78 5E
```

**容错解码图片**（当标准解析报 `unrecognized data stream`）：

```python
from PIL import ImageFile, Image
ImageFile.LOAD_TRUNCATED_IMAGES = True     # ← 关键，允许损坏/截断的 PNG
im = Image.open("Image1.png"); im.load()
im.convert("RGB").save("view.png")
```

## 5. 动态运行：Wine 下 VB6/twinBASIC 的 COM 修复

**症状**：Wine 下程序启动即崩，弹 `twinBASIC Internal Error: Failed to deserialize form`，
error log 显示 `fixme:olepicture:OLEPictureImpl_QueryInterface() unsupported interface {7fd52380-...}`。

**根因**：Wine 内置 `oleaut32` 的 `OleLoadPictureEx` **只部分实现**，`IPicture/IPictureDisp` 查询失败
→ 图片对象为 NULL → 反序列化失败。

**修复**：安装**微软原生 oleaut32**，并让 ole32 用 builtin（原生 ole32 依赖链复杂）：

```bash
export WINEPREFIX=/tmp/wp WINEARCH=win32
winetricks -q oleaut32                  # 从 Win7 SP1 包提取原生 oleaut32.dll
wine reg add "HKCU\\Software\\Wine\\DllOverrides" /v oleaut32 /t REG_SZ /d native  /f
wine reg add "HKCU\\Software\\Wine\\DllOverrides" /v ole32     /t REG_SZ /d builtin /f
wine reg add "HKCU\\Software\\Wine\\DllOverrides" /v comctl32  /t REG_SZ /d builtin /f
```

> ⚠️ **常见误判**：只设 `ole32=native` 会因缺少原生 ole32 依赖而全线 `import_dll ... not found`。
> **正确组合 = oleaut32:native + ole32:builtin**。

**用 winedbg 自动忽略可恢复异常**（VB6 用异常做控制流时必需）：

```bash
yes pass | head -5000 > cmds.txt
winedbg prog.exe < cmds.txt        # 反复 pass = 忽略异常继续执行
```

**X11 无头环境**：`Xvfb :99 -screen 0 1280x1024x24 -ac -noreset &`，
用 `xwininfo -root -tree` 枚举窗口，`xwd -id <WID>` + `convert` 截图，`xdotool` 操作窗口，
`xprop -id <WID> _NET_WM_PID` 关联窗口到进程。

## 6. 自我复制 + 逐字节变异型样本处置

**特征**：
- 程序读**自身文件名**解析序号 N（如 `UnholyDragon-N.exe`），复制为 `N+1` 并启动；
- 每代相对上一代**只改 1 个字节**（累积变异链）；
- **最后一处变异破坏 DOS 头首字节** → 形成**自锁**（第 N 代永不可运行）。

**分析方法**：

```python
# 1. 收集所有代实例，求累积变异链
import glob, re
files = {int(re.search(r'-(\d+)\.exe',f).group(1)): f
         for f in glob.glob("UnholyDragon-*.exe")}
base = open("fixed.exe","rb").read()
chain, prev = [], set()
for n in sorted(files):
    d = open(files[n],"rb").read()
    cur = set(i for i in range(len(d)) if d[i] != base[i])
    for pos in cur - prev:
        chain.append((n, pos, base[pos], d[pos]))   # (代, 偏移, 原值, 新值)
    prev = cur
# 2. 观察规律：位置分布、是否避开压缩块、是否改代码/头
```

**关键结论（通用）**：
- 这类"自我复制"**常是反分析噪声**——真正的载荷不在变异里；
- 但**变异会改变压缩块**，导致**每一代解出的资源不同** → **要试多代**（如本例第 148 代的图片才含 flag）；
- **实例靠文件名判序号**，把某代改名可让它以为自己是别的代（验证机制时有用）。

## 7. 常见误判清单

| 误判 | 实际 |
|---|---|
| 高熵 .data = 加密 | **多为 raw DEFLATE**，先试 `wbits=-15` 再谈加密 |
| `file` 报 `data` = 损坏/加密壳 | **DOS 头被故意改**，修 10 个字节就能用 |
| `zlib` 报 `incorrect data check` = 数据坏 | **只是 Adler32 尾被改**，忽略校验仍可解 |
| 图片打不开 = 数据坏 | 用 `LOAD_TRUNCATED_IMAGES` + 手工拼 IDAT |
| Wine 崩 = 反调试 | **常是 oleaut32 的 IPicture 不支持**，装原生 DLL |
| 自我复制 = 核心机制 | **通常是干扰**，真正 flag 在资源/逻辑里 |
| OCR 单次结果即可信 | **必须多 PSM + 字形签名匹配**双重确认（见 §8） |

## 8. 图内文字可靠识别（避免 OCR 摇摆）

当 flag 在图片里、OCR 对某字符反复摇摆（如 `t`/`i`/`l`）：

**方法：字形签名匹配（数学确定，不依赖 OCR）**

同一字体下"**相同字形 = 相同字符**"。提取每个字符的**逐行宽度轮廓**做签名：

```python
import numpy as np
def signature(mask, s, e):
    ch = mask[:, s:e+1]
    ys, _ = np.nonzero(ch)
    ch = ch[ys.min():ys.max()+1, :]
    widths = tuple(int(np.where(ch[r])[0].max()-np.where(ch[r])[0].min()+1)
                   if ch[r].any() else 0 for r in range(ch.shape[0]))
    return (ch.shape[1], ch.shape[0], widths)
```

**步骤**：
1. 逐列投影切出每个字符段（列间 gap > 阈值 = 分隔）；
2. 对每个段算签名；
3. **找已知字符的段**（如 `d3ntal` 里的 `t`），用其签名去匹配**未知段**；
4. 签名相同 → **必是同一字符**（同字体同字号）。

本例中，`s3ru?ce` 的未知字符签名与 `d3ntal` 的 `t` **逐行宽度完全一致**
→ 数学确定是 `t`，排除了 OCR 给出的 `i`/`l` 摇摆。

> **配套技巧**：二值化（`(a<阈值)*255`）+ 反色（黑底白字）+ 4~8 倍放大，
> 再跑 `tesseract --psm 6/7/8/13` 多模式投票；**最终以字形签名为准**。

## 9. 工具命令速查

```bash
# 熵扫描定位压缩块
python3 -c "..."                      # 见 §1

# raw deflate 解压（关键）
python3 -c "import zlib;print(len(zlib.decompressobj(-15).decompress(open('blob.bin','rb').read())))"

# Wine 环境
winetricks -q oleaut32
wine reg add "HKCU\\Software\\Wine\\DllOverrides" /v oleaut32 /t REG_SZ /d native /f
winedbg prog.exe < cmds.txt

# 窗口取证
Xvfb :99 -screen 0 1280x1024x24 -ac &
DISPLAY=:99 xwininfo -root -tree
DISPLAY=:99 xwd -id 0x<WID> -out w.xwd && convert w.xwd w.png
DISPLAY=:99 xprop -id 0x<WID> _NET_WM_PID

# 图内文字
tesseract img.png stdout --psm 8 -c tessedit_char_whitelist='abcdefghijklmnopqrstuvwxyz0123456789_@.-'
```

## 10. 配套自动化工具

同目录 `twinbasic_unpack_tool.py` 一键完成：DOS 头修复 → 熵扫描 → 智能定位 raw-DEFLATE 描述符 → 解压 → 提取内嵌 PNG。
已用 FLARE-On 12 UnholyDragon 样本端到端验证（自动定位 `@0xb12a8`，解出 1839781 字节 + PNG）。

```bash
python3 twinbasic_unpack_tool.py sample.exe outdir/
# [*] 高熵区 (>7.5):  0xb1000 - 0x272000
# [+] 描述符 @0xb12a8: size0=1838690 size1=1839781 (解出 1839781)
# [+] 内嵌 PNG: outdir/resource.png (1838852 bytes)
```

## 11. 输出位置

- 解密脚本 → `notes/` 或 `tools/`
- 解出资源（图片/配置）→ `exports/`
- 修复后的 PE → `patches/`
- 分析报告 → `reports/`
- **通用技巧** → 本篇（`kb/pe-reverse/techniques/05-crypto-unpack/`）
