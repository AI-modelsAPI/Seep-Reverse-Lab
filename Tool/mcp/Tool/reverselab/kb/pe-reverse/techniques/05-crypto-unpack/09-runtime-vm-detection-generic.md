---
id: "pe-reverse/05-crypto-unpack/09-runtime-vm-detection-generic"
title: "运行时 VM 探测：跨实现通用的虚拟机识别与验证（零真机）"
title_en: "Runtime VM Detection: Implementation-Agnostic Virtual Machine Identification and Verification"
summary: >
  用运行时行为（而非静态特征）判定二进制是否使用代码虚拟化，并验证分析方法论的通用性。
  给出五条不可伪装判据（高频间接分发 / 分发点集中 / handler 多样性 / 字节码指针 / 目标有效性），
  覆盖两种分发形态（`jmp [base+idx*scale]` 与 `jmp reg`）、交互式样本的多输入策略、
  以及嵌套 VM 的识别。实测于 VMProtect 3.0-3.10 官方 Demo 与 13 个自研 VM crackme，
  两种实现的分发机制同构但细节不同。
summary_en: >
  Behavior-based (not signature-based) detection of code virtualization, plus a validation of
  analysis methodology across implementations. Five non-forgeable runtime criteria, two dispatch
  topologies, multi-input strategy for interactive samples, and nested-VM identification.
  Validated on VMProtect 3.0-3.10 demos and 13 custom-VM crackmes.
board: "pe-reverse"
category: "05-crypto-unpack"
signals:
  - "运行时 VM 探测"
  - "runtime VM detection"
  - "如何判断是不是 VM"
  - "间接分发"
  - "jmp reg"
  - "jmp [base+idx*scale]"
  - "嵌套 VM"
  - "nested VM"
  - "自研 VM"
  - "方法论通用性"
  - "交互式样本"
  - "511 字节"
mcp_tools:
  - "kb_router"
  - "seep_r2_disasm"
keywords:
  - "runtime detection"
  - "VM detection"
  - "indirect dispatch"
  - "nested VM"
  - "generic methodology"
  - "emulation"
difficulty: "advanced"
tags:
  - "vmprotect"
  - "emulation"
  - "runtime-analysis"
  - "vm-detection"
  - "generic"
language: "zh-CN"
last_updated: "2026-10-16"
related_articles:
  - "pe-reverse/05-crypto-unpack/08-selfhealing-emulation-vmp-handler-extraction"
  - "pe-reverse/05-crypto-unpack/02-vmp-virtualization-analysis"
  - "general/methodology/01-headless-emulation-windows-android-handbook"
evidence: "reproduced"
validated_by: "实测于 VMProtect 3.0/3.2/3.4/3.10 官方 Demo + 13 个自研 VM crackme"
---
# 运行时 VM 探测：跨实现通用的虚拟机识别与验证（零真机）

## 场景

拿到一个未知样本，需要回答两个问题：

1. **它是不是用了代码虚拟化？**（不是 VMProtect 也可能有自研 VM）
2. **我的分析方法论对它有效吗？**（还是只对某个特定实现有效）

**静态特征（节区名/熵/字符串）会骗人**。本文给出基于**运行时行为**的金标准。

## 输入信号

- 样本有异常节区（非标准名 / 高熵 / 可执行数据节区）
- 静态扫描到 `jmp/call [base+index*scale]`
- 静态扫描到密集指针表
- **但不确定是真 VM 还是普通加密算法 / 反调试**

## 核心原则：静态判据不可靠，运行时才可靠

实测教训（本次）：

| 样本 | 静态侦察评分 | 运行时判据 | 真相 |
|---|---|---|---|
| `Matryoshka-VM` | 5/8（疑似 VM）| **5/5 真 VM** | ✅ 确实是 VM |
| `Challenger_3` | **8/8** | 4/5（UPX 误报）| ❌ 是 UPX 壳 |
| `custom-vmp-crackme` | 5/8 | 5/5 真 VM | ✅ 是 VM |
| 纯加密 crackme | 5/8 | **0/5** | ❌ 是 LCG+XOR |

**结论**：静态判据给出的是「值得进一步看」，**不能作为 VM 判定**。

## 五条不可伪装判据（金标准）

真 VM 的**必要条件**（必须在运行时观测到）：

| # | 判据 | 阈值 | 原理 |
|---|---|---|---|
| **C1** | 高频间接分发 | ≥ 100 次 | VM 主循环必然反复取指分发 |
| **C2** | 分发点集中 | top1 占比 > 30% 或 PC 数 ≤ 5 | 分发集中在一处 = 解释器循环 |
| **C3** | handler 多样性 | ≥ 16 个不同目标 | 指令集需要多个 handler |
| **C4** | 字节码指针/聚集度 | 目标跨度 < 512KB 或 多分发点 | handler 聚集在同一区域 |
| **C5** | 分发目标有效 | > 90% 在映像内 | 排除垃圾跳转 |

**关键**：这五条**无法用静态手段伪装** —— 攻击者可以让节区名好看、让熵正常，但**运行时必须真的反复分发**才能执行虚拟化代码。

## 分发形态：必须支持两种

```python
# 形态 A: jmp/call [base + index*scale]     (VMP 3.0-3.4)
0x1400efb92: movzx eax, byte ptr [rsi]
0x1400efb95: jmp   qword ptr [r12 + rax*8]

# 形态 B: jmp reg（寄存器间接）             (VMP 3.10 / 自研 VM)
0x140008de7: movsxd rdx, dword ptr [r15 + rdx*4]
0x140008deb: add    rdx, r15
0x140008dee: jmp    rdx
```

**只认形态 A 会漏掉一半的 VM**（本次实测：Matryoshka-VM 用形态 B，最初被漏检）。

探测代码（Unicorn）：

```python
REG_MAP = {'rax': UC_X86_REG_RAX, 'rcx': UC_X86_REG_RCX, 'rdx': UC_X86_REG_RDX,
           'rbx': UC_X86_REG_RBX, 'rsi': UC_X86_REG_RSI, 'rdi': UC_X86_REG_RDI,
           'rbp': UC_X86_REG_RBP, 'rsp': UC_X86_REG_RSP,
           'r8': UC_X86_REG_R8, 'r9': UC_X86_REG_R9, 'r10': UC_X86_REG_R10,
           'r11': UC_X86_REG_R11, 'r12': UC_X86_REG_R12, 'r13': UC_X86_REG_R13,
           'r14': UC_X86_REG_R14, 'r15': UC_X86_REG_R15}

def on_code(uc, addr, size, ud):
    ins = next(md.disasm(bytes(uc.mem_read(addr, min(size,15))), addr))
    if ins.mnemonic not in ('jmp', 'call'):
        return True

    # ── 形态 B: jmp reg ──
    if ins.op_str in REG_MAP:
        tgt = uc.reg_read(REG_MAP[ins.op_str])
        if in_image(tgt): record(addr, tgt)
        return True

    # ── 形态 A: jmp [base + index*scale] ──
    if '[' not in ins.op_str: return True
    inner = ins.op_str[ins.op_str.index('[')+1:ins.op_str.rindex(']')].replace(' ','')
    if '*' not in inner: return True
    base = idx = None; scale = 1
    for part in inner.split('+'):
        if '*' in part:
            idx = part.split('*')[0]
            scale = int(part.split('*')[1], 0)
        elif part in REG_MAP:
            base = part
    if base and idx:
        bv = uc.reg_read(REG_MAP[base]); iv = uc.reg_read(REG_MAP[idx])
        tgt = struct.unpack('<Q', uc.mem_read((bv + iv*scale) & 0xFFFFFFFFFFFFFFFF, 8))[0]
        if in_image(tgt): record(addr, tgt)
    return True
```

## 交互式样本：多输入策略（易踩的坑）

**很多 crackme 是交互式的，需要在特定输入下才进入 VM 路径。**

实测（Matryoshka-VM）：

```asm
0x140008c78: cmp  ebp, 0x1ff       ; 输入长度 == 511 ?
0x140008c7e: jne  0x140008d40      ; 否则继续读
0x140008cdc: test bl, bl
0x140008cde: je   0x140008d58      ; 满 511 才跳 VM 入口
```

**输入不足 511 字节 → 走「加密校验」分支 → 看起来像普通算法，完全不像 VM。**

对策：**多输入长度候选**（None 会漏检）：

```python
INPUTS = [
    b"test\n",
    b"A"*12 + b"\n",
    b"A"*511 + b"\n",     # ← Matryoshka-VM 需要这个
    b"A"*255 + b"\n",
    b"A"*63 + b"\n",
    b"A"*31 + b"\n",
    b"A"*15 + b"\n",
]
# 逐个跑，取分发次数最高的
```

> 也可先静态分析「输入长度约束」（`cmp reg, imm` + 分支），直接构造。

## 嵌套 VM 的识别

**多个分发点 = 嵌套 VM**：

| 样本 | 分发点数 | 含义 |
|---|---:|---|
| `two_ring_vow.exe` | **16** | 16 层/个嵌套 VM |
| `custom-vmp-crackme` | **15** | 同上 |
| `Matryoshka-VM` | **6** | 字符串明说 "five nested virtual machines" |
| VMP 官方 Demo | 1-4 | 单层或少量分片 |

判据：`len(disp_pc) >= 2 且分发次数 >= 100` → 标记为嵌套 VM。

**嵌套 VM 的特点**：每层有独立的指令集、字节码、分发点；调用外部函数后**进入新 VM**。

## 实测结果

### VMProtect 官方 Demo（对照组，必须满分）

```
math.3.0.0-virt.exe:  C1 18,825 ✅  C2 100% ✅  C3 132 ✅  C4 ✅  C5 100% ✅  → 5/5
```

### 13 个自研 VM crackme（无任何 VMProtect 特征）

| 评分 | 样本 | 分发 | 分发点 | handler | 判定 |
|---:|---|---:|---:|---:|---|
| 5/5 | `two_ring_vow.exe` | 413 | 16 | 25 | ★ 真 VM |
| 5/5 | `custom-vmp-crackme` | 886 | 15 | 22 | ★ 真 VM |
| 5/5 | `Matryoshka-VM` | 6,577 | 6 | 46 | ★ 真 VM |
| 4/5 | `boxvm.exe` | 114 | 2 | 2 | ★ 真 VM |
| 4/5 | `sumhex.exe` | 267 | 74 | 78 | ★ 真 VM |
| 4/5 | `Challenger_3.exe` | 18,496 | 4 | 1 | ⚠️ UPX 误报 |
| 3/5 | `crackme.lucky.exe` | 2,318 | 1 | 1 | 疑似 |
| 2/5 | `CrackMe0.exe` | 50 | 45 | 44 | 疑似 |
| 0/5 | 其余 3 个 | 0 | 0 | 0 | 非 VM |

## 方法论通用性验证

对 `Matryoshka-VM` 套用完整流程（与 VMP 篇 `08` 相同）：

| 环节 | VMP 3.0 | Matryoshka-VM | 通用性 |
|---|---|---|---|
| PE 加载 + 重定位 | ✅ | ✅ | **✅** |
| IAT 打桩 + API 语义 | ✅ | ✅ | **✅** |
| 自愈式仿真 | ✅ | ✅ | **✅** |
| 反调试旁路 | `int 3` | - | **✅** |
| 运行时 VM 探测 | 18,825 | 5,839 | **✅** |
| 分发机制 | `jmp [r12+rax*8]` | `movsxd rdx,[r15+rdx*4]; add rdx,r15; jmp rdx` | **✅ 同构** |
| 表结构 | 8B 绝对 / 4B 相对 | **4B 相对** | **✅** |
| **V2 静态验证** | 256/256 | **16/16** | **✅** |
| handler 多样性 | 132 | 46 | **✅** |
| 嵌套 VM | 未观测 | **6 分发点** | **✅ 新特征** |

**结论：方法论完全通用。** 两种实现的分发机制**同构**（都是 `表[opcode] + 基址 → 跳转`），细节不同（表项宽度、密钥处理、是否嵌套）。

## 攻击链

```
静态侦察（便宜，只用于筛选）
  ├─ 已知壳检测（UPX/ASPack/Themida）-> 直接排除
  ├─ 异常节区 / 高熵 / 间接分发形态
  └─ 得到"候选集"
       ↓
运行时探测（金标准）
  ├─ 自愈式仿真（PE 加载 + 环境桩 + API 语义 + 陷阱忽略）
  ├─ 多输入候选（覆盖长度约束）
  ├─ 记录 jmp/call 两种形态的分发
  └─ C1-C5 判据评分
       ↓
真 VM 确认
  ├─ 分发点数量 -> 单层 / 嵌套
  ├─ 分发点形态 -> 表结构（绝对/相对）
  └─ 套用 08 篇的 handler 提取 + V1-V6 验证
```

## 无真机方案能力矩阵

| 能力 | 可用性 | 证据 |
|---|:---:|---|
| PE 加载 + IAT 打桩 | ✅ | 53 导入独立桩 |
| 交互式输入模拟 | ✅ | getchar hook + 多输入候选 |
| 运行时 VM 探测 | ✅ | VMP 5/5 + Matryoshka-VM 5/5 |
| 分发形态识别（两种）| ✅ | `jmp [mem]` + `jmp reg` |
| 嵌套 VM 识别 | ✅ | 16/15/6 分发点 |
| 分发点/表结构定位 | ✅ | 静态可解 4B 相对表 |
| V2 静态验证 | ✅ | 16/16 合法 handler |
| 已知壳排除 | ✅ | UPX/ASPack/Themida |

## 关键陷阱

| 陷阱 | 现象 | 解法 |
|---|---|---|
| **IAT 桩页未映射** | 自愈页数异常（数百），程序跑飞 | 主动 `mem_map` 桩页 |
| **API 桩共用** | 无法区分哪个 API 被调用 | per-API 独立桩地址 |
| **只认 `jmp [mem]`** | 漏掉 `jmp reg` 形态的 VM | 支持两种形态 |
| **单一输入** | 需要特定长度的样本漏检 | 多输入候选 |
| **布尔判据 `and/or`** | Python 返回 Counter 而非 bool | 强制 `bool()` |
| **静态判据当真** | UPX 拿 8/8 误报 | 静态只做筛选，运行时才是判定 |
| **字符串误导** | "five nested virtual machines" 也可能是诱导 | 只信运行时 |

## MCP 工具映射

| 攻击链步骤 | MCP 工具 | 说明 |
|---|---|---|
| 节区/熵/导入侦察 | `seep_r2_info` · `seep_r2_strings` | 静态筛选 |
| 反汇编候选区 | `seep_r2_disasm` | 看分发形态 |
| 方法论检索 | `kb_router` · `seep_kb_search` | 命中本篇与 08 篇 |

> 运行时探测是纯 Python + Unicorn 脚本，见同目录 `runtime_vm_detector.py`。

## 配套脚本

| 脚本 | 作用 |
|---|---|
| `runtime_vm_detector.py` | **通用运行时 VM 探测器**（C1-C5 判据，两种分发形态，多输入）|
| `pe_loader_v2.py` | 修复版 PE 加载器（桩页主动映射 + per-API 桩 + API 语义）|
| `selfhealing_vmp_emu.py` | 自愈式仿真器（08 篇）|

```bash
python3 runtime_vm_detector.py <sample.exe> [more.exe ...]
python3 pe_loader_v2.py <sample.exe>          # 加载器自测
```

## 证据与验证闭环

- 探测器**必须先在已知 VM 上校准**（VMP 官方 Demo 应得 5/5），再用于未知样本
- 判定为真 VM 后，用 08 篇的 **V2 静态解码**交叉验证（静态能否解出合法 handler）
- 记录：样本 SHA256、分发次数、分发点数、handler 数、表基址与形态
- 与静态侦察结果对照，**不吻合时以运行时为准**
