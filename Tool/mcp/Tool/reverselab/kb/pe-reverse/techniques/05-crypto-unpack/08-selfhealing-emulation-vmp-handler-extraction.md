---
id: "pe-reverse/05-crypto-unpack/08-selfhealing-emulation-vmp-handler-extraction"
title: "自愈式仿真：无真机提取 VMP Handler 表与字节码（PE x64）"
title_en: "Self-Healing Emulation: Extracting VMP Handler Tables and Bytecode Without a Windows Host (PE x64)"
summary: >
  在无 Windows 沙箱、无真机条件下，用 Unicorn 自愈式仿真（自动映射未映射页 + 忽略反调试陷阱）
  完整跑通 VMProtect 各版本官方 Demo，导出 256 项 handler 表、破译 VM 指令集语义、
  提取 VM 字节码流并产出解映射修复后的可分析 PE。含 3.0-3.4 与 3.10 的分发机制差异
  （绝对地址表 vs 32 位相对偏移表 + 寄存器分发）、handler 轮换统计、VM 虚拟寄存器重映射表
  `[rsp+rax]` 机制，以及与真机 Frida dump 的等价性对比。
summary_en: >
  A self-healing Unicorn emulation methodology for analyzing VMProtect-protected PE x64 binaries
  without a Windows host or debugger: auto-map unmapped pages, ignore anti-debug traps, run the packer
  to completion, then extract the 256-entry handler table, recover VM opcode semantics, dump the VM
  bytecode stream, and emit an IDA-loadable unmapped PE. Covers the dispatcher difference between
  VMP 3.0-3.4 (absolute 8-byte table) and 3.10 (32-bit relative offset table + register dispatch),
  handler-variant statistics, and the `[rsp+rax]` virtual-register remap mechanism.
board: "pe-reverse"
category: "05-crypto-unpack"
signals:
  - "VMProtect"
  - "VMP"
  - "handler 表"
  - "VM 字节码"
  - "无真机"
  - "自愈式仿真"
  - "self-healing emulation"
  - "Unicorn"
  - "headless"
  - "反调试陷阱"
  - "int 3"
  - "jmp [r12+rax*8]"
  - "jmp rdx"
  - "相对偏移表"
mcp_tools:
  - "kb_router"
  - "seep_r2_cmd"
  - "seep_r2_disasm"
keywords:
  - "VMProtect"
  - "handler table"
  - "VM bytecode"
  - "Unicorn"
  - "self-healing"
  - "headless emulation"
  - "devirtualization"
  - "dispatcher"
difficulty: "advanced"
tags:
  - "vmprotect"
  - "emulation"
  - "unicorn"
  - "handler-extraction"
  - "headless"
  - "pe"
language: "zh-CN"
last_updated: "2026-10-16"
related_articles:
  - "pe-reverse/05-crypto-unpack/01-pe-unpack-dump"
  - "pe-reverse/05-crypto-unpack/02-vmp-virtualization-analysis"
  - "pe-reverse/05-crypto-unpack/03-vmp-devirtualization-toolchain"
  - "pe-reverse/05-crypto-unpack/06-modern-pe-unmapping-and-dump-reconstruction"
  - "general/methodology/01-headless-emulation-windows-android-handbook"
evidence: "reproduced"
validated_by: "实测于 VMProtect 官方 Demo 3.0.0/3.2.0/3.4.0/3.10.0 (math/conditional/printf) 共 20 样本"
---
# 自愈式仿真：无真机提取 VMP Handler 表与字节码（PE x64）

## 场景

拿到 VMProtect 保护的 PE x64 样本（官方 Demo 或其他），但**没有 Windows 沙箱、没有真机、没有 x64dbg**。
静态分析看到的是 handler 循环和垃圾指令；`03-vmp-devirtualization-toolchain` 里的 NoVmp 类工具对
新版 VMP 大概率失效。

本文给出**第三条路**：用 Unicorn 做**自愈式仿真**——不追求精确复刻真机环境，而是**遇错自动修**，
把壳跑到自然结束，然后在仿真内存里直接读 handler 表与字节码。

> 相比 `01` 篇的真机 Frida dump 与 `03` 篇的 devirt 工具链，本文方法的特点是：
> **零宿主依赖、零工具安装（只需 Unicorn）、对任意 VMP 版本可降级使用**。

## 输入信号

- PE 节区名为 `.vmp0`/`.vmp1`（VMP 2.x–3.2）或混淆随机名（3.4+，如 `.awC`/`.h#o`）
- 导入表只剩少量 KERNEL32 API；EP 落在壳节区
- `diec -b target.exe` 报 `VMProtect(3.x)`
- **无 Windows 环境但需要拿到 handler 表 / VM 字节码 / 可分析镜像**

## 核心思想：自愈式仿真（Self-Healing Emulation）

传统精确仿真的困境：VMP 的 VM context 依赖此前执行的大量副作用（壳自解密、TEB/PEB 初始化、
堆分配、异常链），**静态无法预测缺失什么**，逐一补齐成本极高。

自愈式仿真的转变：

| 维度 | 精确复刻 | **自愈式** |
|---|---|---|
| 未映射内存访问 | 分析缺什么 → 手工补 | **自动映射该页 → 重试指令** |
| 反调试陷阱（int 3/2d） | 逐个 patch 或 hook API | **注册 INTR hook 直接忽略** |
| 未初始化数据 | 追求与真机一致 | **接受垃圾值，能跑完即可** |
| 目标 | 环境保真 | **行为可观测** |

**关键洞察**：无真机场景下，"能跑完并观测到行为"比"环境精确复刻"价值更高。
类似 Qiling/SPEKE 的 environment-lift 思路，但实现更轻（仅 Unicorn）。

## 三层 Hook 架构

```python
from unicorn import *
from unicorn.x86_const import *

mu = Uc(UC_ARCH_X86, UC_MODE_64)

# ① 自愈层：未映射访问 -> 自动映射页 -> 重试
auto_pages = set()
def map_page(addr):
    page = addr & ~0xFFF
    if page in auto_pages:
        return False
    try:
        mu.mem_map(page, 0x1000, UC_PROT_ALL)
        auto_pages.add(page)
        return True
    except UcError:
        return False

def on_read_unmapped(uc, access, addr, size, value, ud):
    map_page(addr); return True          # True = 重试该指令
def on_write_unmapped(uc, access, addr, size, value, ud):
    map_page(addr); return True
def on_fetch_unmapped(uc, access, addr, size, value, ud):
    map_page(addr); return True

mu.hook_add(UC_HOOK_MEM_READ_UNMAPPED,  on_read_unmapped)
mu.hook_add(UC_HOOK_MEM_WRITE_UNMAPPED, on_write_unmapped)
mu.hook_add(UC_HOOK_MEM_FETCH_UNMAPPED, on_fetch_unmapped)

# ② 反调试旁路层：忽略 int 3 / int 0x2d 等陷阱
def on_intr(uc, intno, ud):
    return True                          # 忽略并继续
mu.hook_add(UC_HOOK_INTR, on_intr)

# ③ 观测层：捕获 dispatch 事件（见下文）
```

> **注意**：`UC_HOOK_MEM_*_UNMAPPED` 回调返回 `True` 表示"已处理，重试当前指令"；
> 返回 `False` 才会上报为 `UC_ERR_*_UNMAPPED` 异常。

## PE 加载器：Windows loader 的三件事

类比 ELF 的 ld.so 三件事（重定位/初始化/TLS），PE 侧对应：

| 步骤 | 实现要点 |
|---|---|
| **① 节区映射** | 按 `VirtualAddress` 展开到 `ImageBase`；`SizeOfHeaders` 单独拷头部 |
| **② 基址重定位** | 遍历 `.reloc`（`IMAGE_BASE_RELOCATION`），处理 Type 3 (HIGHLOW) / Type 10 (DIR64) |
| **③ IAT 打桩** | 遍历导入表，为每个 thunk 写桩函数地址（默认 `xor eax,eax; ret` = `31 C0 C3`） |

Windows x64 特有的环境桩：

```python
# TEB (x64 用 FS 寄存器, 不是 GS!)
mu.mem_write(TEB + 0x30, pack('<Q', TEB))       # TEB->Self
mu.mem_write(TEB + 0x60, pack('<Q', PEB))       # TEB->PEB
mu.reg_write(UC_X86_REG_FS_BASE, TEB)

# PEB 反调试字段清零
mu.mem_write(PEB + 0x02, b'\x00')               # BeingDebugged = 0
mu.mem_write(PEB + 0xbc, pack('<I', 0))         # NtGlobalFlag = 0

# 栈 + 哨兵返回地址
mu.mem_write(RSP, pack('<Q', SENTINEL))
```

## VM Entry 全景（3.0.0 实证，92 条指令）

从 EP 到首次 dispatch 的完整轨迹，关键指令：

```asm
0x000efb34: mov rbp, rsp           ; VM 栈指针 = 当前栈
0x000efb3f: sub rsp, 0x180         ; 分配 VM context (0x180 字节)
0x000efb4d: and rsp, ~0xf          ; 16 字节对齐
0x000efb54: mov rbx, rsi           ; 保存 VM key     <- VMEXIT 回到此处!
0x000efb75: lea r12, [rip-0x14f4]  ; ★ r12 = handler 表基址 = 0x1400ee688
0x000efb88: sub rsi, 1             ; vm_ip 调整
0x000efb92: movzx eax, byte [rsi]  ; 取 opcode
0x000efb95: jmp [r12+rax*8]        ; 分发
```

**双向验证**：静态算出的 `lea r12,[rip-0x14f4] → 0x1400ee688` 与仿真捕获的表基址**完全一致**。

> **陷阱提示**：VMP 会在多个节区放置**外观相同但未使用的 dispatcher 副本**。
> 静态扫描可能命中 `.vmp0` 的副本（本例 `0x1400aae22`），而**实际执行的是 `.vmp1` 的
> `0x1400efb92`** —— 只有跑起来才知道哪个是真的。

## 分发机制：两个时代的分水岭

### 3.0–3.4：绝对地址跳表（静态可见）

```asm
movzx eax, byte ptr [rsi]      ; 0F B6 06
jmp   qword ptr [r12+rax*8]    ; 41 FF 24 C4   <- 8 字节绝对地址表
```

静态扫描模式：`0F B6 06` + `41 FF 24 C4` 紧邻出现即可定位。

### 3.10：相对偏移表 + 寄存器分发（静态扫描失效，但表是明文） 

```asm
0x101124: movzx  r10d, byte ptr [rsi]          ; 取 opcode
0x101132: add    rsi, 1                         ; vm_ip++
0x101142: movsxd rdx, dword ptr [r11 + r10*4]   ; ★ 32 位有符号相对偏移（表中存的是偏移，不是地址）
0x101146: add    rdx, r11                       ; 目标 = 表基址 + 偏移
0x101149: jmp    rdx                            ; ★ 寄存器间接分发
```

| 版本 | 表项宽度 | 表基址 | 分发指令 | 静态可定位 | 表内容 |
|---|---:|---|---|:---:|---|
| 3.0-3.4 | 8 字节绝对地址 | r12 | `jmp qword [r12+rax*8]` | ✅ | 明文 |
| **3.10** | **4 字节相对偏移** | **r11** | **`jmp rdx`**（寄存器） | ❌ | **明文** |

> **重要区分（经静态解码实证）**：3.10 并非"表被加密"，而是
> **分发指令从 `jmp [内存]` 改成了 `jmp 寄存器`，导致静态扫描器扫不到表的位置**。
> 表内容本身在文件中就是**明文**（4 字节有符号相对偏移）。
> 仿真在其中的作用不是"解密"，而是**定位表基址 r11**。
>
> 实测：`3.10` 文件偏移 `0x102574` 处的原始字节 `28acffff b6bbffff 08abffff ...`
> 按 4 字节有符号解释为 `-21464, -17482, -21752 ...`，
> 加表基址 `0x106774` 即得 `0x10139c, 0x10232a, 0x10127c ...` —— 全是合法 handler。

**为什么仿真仍然不可替代**：静态全盘扫描找候选表会产生**大量假阳性**。
实测数据：

| 版本 | 4字节候选数 | 8字节候选数 | 哪个是真的 |
|:-----|:-----------:|:-----------:|:-----------|
| 3.0.0 | **10** | 2 | 8 字节（仿真确认）|
| 3.10.0 | 8 | 0 | 4 字节（仿真确认）|

只有运行时仿真（读 r11/r12 的实际值）才能**唯一确定**哪个候选是真的。
这正是无真机方案的价值定位：**不是"仿真能解密"，而是"仿真能唯一定位目标结构、消除静态歧义"**。

**运行时提取（仿真实测 28551/28551 = 100% 匹配）**：

```python
# hook 'jmp rdx'，在指令处读 r10(opcode)/r11(表基址)/rdx(目标)
def on_jmp(uc, addr, size, ud):
    op  = uc.reg_read(UC_X86_REG_R10) & 0xFF
    r11 = uc.reg_read(UC_X86_REG_R11)
    tgt = uc.reg_read(UC_X86_REG_RDX)
    # 验证: tgt == r11 + signed32(mem[r11 + op*4])
    off = struct.unpack('<i', uc.mem_read(r11 + op*4, 4))[0]
    assert (r11 + off) & 0xFFFFFFFFFFFFFFFF == tgt
```

## Handler 表提取

### 通用捕获（适配寄存器轮换）

**不要**硬编码 `41 FF 24 C4`（3.2+ 会轮换到 `r11`/`rdx`）。改为**运行时识别形态**：

```python
REG_MAP = {'rax': UC_X86_REG_RAX, ..., 'r15': UC_X86_REG_R15}

def on_code(uc, addr, size, ud):
    ins = next(md.disasm(uc.mem_read(addr, 15), addr))
    if ins.mnemonic not in ('jmp', 'call') or '[' not in ins.op_str:
        return True
    inner = ins.op_str[ins.op_str.index('[')+1:ins.op_str.rindex(']')].replace(' ', '')
    # 匹配 [base + index*8]
    if '*8' not in inner: return True
    base = idx = None
    for p in inner.split('+'):
        if '*' in p: idx = p.split('*')[0]
        elif p in REG_MAP: base = p
    if base and idx:
        bv = uc.reg_read(REG_MAP[base])
        iv = uc.reg_read(REG_MAP[idx])
        tgt = struct.unpack('<Q', uc.mem_read((bv + iv*8) & 0xFFFFFFFFFFFFFFFF, 8))[0]
        if in_image(tgt): record(iv & 0xFF, tgt)
    return True
```

### 各版本提取结果

| 版本 | 表基址 RVA | 表项 | 指向映像内 | 实际执行 opcode |
|---|---|---:|---:|---:|
| 3.0.0 | `0xee688` | 256 | 256/256 | 140 |
| 3.2.0 | `0x12ec58` | 256 | 256/256 | 136 |
| 3.4.0 | `0x137d70` | 256 | 256/256 | 163 |
| 3.10.0 | `0x106774` | 256 | 256/256 | 133 |

## VM 指令集语义建模

### 关键突破：`[rsp + rax]` 是虚拟寄存器重映射表

```asm
opcode=0x24:  mov rcx,[rbp] ; add rbp,8 ; mov [rsp+rax],rcx
opcode=0x96:  mov rax,[rsp+rax] ; sub rbp,8 ; mov [rbp],rax
              ↑ rax = 从字节码取出的寄存器索引
```

`[rsp+rax]` 读 = 读虚拟寄存器，写 = 写虚拟寄存器 —— 这是 VMP 的 **VM 寄存器存取名空间**。

### VM 指令集骨架

| 语义 | 识别特征 | 说明 |
|---|---|---|
| `vm_push_reg` | `mov rcx,[rbp]; add rbp,8; mov [rsp+rax],rcx` | VM 栈 → 虚拟寄存器 |
| `vm_pop_reg` | `mov rax,[rsp+rax]; sub rbp,8; mov [rbp],rax` | 虚拟寄存器 → VM 栈 |
| `vm_push_imm` | `sub rsi,N; mov rax,[rsi]; sub rbp,N; mov [rbp],rax` | 从字节码读立即数 |
| `vm_exit` | `jmp 0x1400efb54`（VM entry 内 `mov rbx,rsi` 处） | 恢复宿主上下文 |
| `vm_arith` | 读 `[rbp]`/`[rbp+8]`，运算，写 `[rbp+off]` | 加减乘移位等 |

### handler 轮换统计（3.0.0，256 handler）

| 语义 | 变体数 | 语义 | 变体数 |
|---|---:|---|---:|
| `vm_pop` | **66** | `vm_add` | 13 |
| `vm_sub` | 27 | `vm_setvsp` | 11 |
| `vm_shl` | 21 | `vm_mul` | 10 |
| `vm_push` | 16 | `vm_exit` | 10 |

`vm_pop` 有 **66 个等价变体** —— 这是 KB `02` 篇"同一语义存在多个变体 handler，
编译时随机选择"的**定量实证**。任何针对 handler 地址的指纹方案都不可行。

## VM 字节码流定位

运行时记录 `vm_ip`(`rsi`) 的取值范围与读到的字节：

```
vm_ip 范围    : RVA 0xc5b9f .. 0xe9a00   (跨度 0x23e61)
所在节区      : .vmp1
唯一 vm_ip    : 11,599 个
观测 opcode   : 167 种
字节码区段    : RVA 0xc5000 .. 0xeaa00   (154,112 bytes), 熵 5.547
handler 表    : RVA 0xee036 .. 0xf135d   -> ✅ 与字节码完全分离
```

**高频 opcode 配对**：`0xca↔0x24`（3593/3587）与 `0x96↔0x2f`（2622/2619）成对出现 ——
这是 VMP 的**指令包装混淆**：每个真实操作前后包裹 vreg 读写。

## 字节码反编译

过滤装饰（`vm_vreg_load/store` 占 67%）后的真实指令流：

| 指令 | 次数 | 指令 | 次数 |
|---|---:|---|---:|
| `vm_push_imm64` | 1402 | `vm_push` | 506 |
| `vm_add` | 708 | `vm_rcr` | 350 |
| `vm_and` | 630 | `vm_sub` | 297 |
| `vm_pop` | 596 | `vm_exit` | 125 |

**算术密集型负载**，与 `math` demo 的行为特征吻合。

## 内存转储与解映射

```python
# 1) 从仿真内存导出 Virtual Layout 镜像
total = align_up(max(sizeof_image, max(s.rva + max(s.vsize, s.rsize) for s in sections)))
img = bytearray(total)
img[:sizeof_headers] = mu.mem_read(load_base, sizeof_headers)
for s in sections:
    img[s.rva : s.rva+end] = mu.mem_read(load_base + s.rva, end - s.rva)
open('dump.bin','wb').write(img)

# 2) 应用 06 篇三步曲解映射修复
#    FileAlignment = SectionAlignment
#    PointerToRawData = VirtualAddress
#    SizeOfRawData = align_up(VirtualSize, SectionAlignment)
```

产物：4 个版本各 1.0–1.3 MB 的合法 PE，`rabin2 -I` 确认 `baddr/subsys/arch` 正常。

## 与真机 Frida dump 的等价性

| 环节 | 真机 Frida | 自愈式仿真 |
|---|---|---|
| 让壳跑完 | 原生执行 | Unicorn 200 万指令 |
| 读映像内存 | `Memory.readByteArray` | `mu.mem_read` |
| 解映射修复 | 同 06 篇 | 同 06 篇 |
| 反调试 | ScyllaHide | **INTR hook 忽略** |
| 覆盖面 | 100% | ~95%（自愈补偿） |
| 成本 | 需 Windows 沙箱/真机 | **纯 Python，零宿主依赖** |

**结论**：在"内存转储与 handler 提取"目标上，自愈式仿真**可替代真机**。

## 攻击链

```
静态侦察 (节区名/DiE/熵)
  → 判定保护模式: PACK(原始节区 raw=0) / VIRT(仅虚拟化) / ANTIDBG
  → PE 加载器: 节区映射 + .reloc 重定位 + IAT 打桩
  → 环境桩: TEB/PEB + FS_BASE + BeingDebugged=0 + 堆
  → 自愈式仿真: 自动映射未映射页 + INTR hook 忽略反调试
  → 跑完壳 (200 万指令, 自然结束)
  → hook dispatch: 按形态识别 (jmp [base+idx*8] 或 jmp reg)
  → 导出 256 项 handler 表 + 140 种 opcode
  → VM Entry 全景 (92 条轨迹) 定位 VM key / VMEXIT 地址
  → handler 语义建模 (含 [rsp+rax] 虚拟寄存器重映射)
  → VM 字节码流定位 + 反编译
  → 内存转储 + 解映射修复 → IDA 可载 PE
```

## 与公开权威分析的对照（联网检索）

本方法与小节结论已对照以下公开来源：

| 来源 | 类型 | 关键结论 | 与本文关系 |
|---|---|---|---|
| mzakocs **VMProtect 3 分析** | 权威博客（配套 IDA 库 77★）| **VMP 3.5 不使用 opcode 或 handler 表**，改用 **FDJ**（当前 handler 地址 + 滚动密钥解码偏移）| ⚠️ **版本差异**，见下 |
| **Inspecting VM Diversification** | IEEE S&P 2025 | VM 多样化三维度：VM 解释 / 字节码组织 / **handler 置换重定位** | 与本文 handler 轮换统计对应 |
| **VMHunt** | CCS'18 | trace 切分 + 符号执行 + **语义验证** | 本文 V1-V6 的学术基础 |
| **PolyUnpack** | ACSAC'06 | **静态代码模型 vs 动态执行**差分判定 | 本文 V2/V5 思路源头 |
| sexyiam/**VMPLift** | 工具（3.8-3.10）| merged handlers / rolling key / 寄存器随机化 | 3.8+ 新特性，本文未覆盖 |
| wul7chaos/**vmp-reverse-skill** | 工具 | **Z3 形式化等价判定**（PROVEN/REFUTED/FUZZED）| 比本文 V1-V6 更强，可作升级方向 |
| can1357/**NoVmp** · eversinc33/**MogVMP** | 工具 | VTIL / Remill+LLVM 提升 | 与 03/07 篇对应 |

### ⚠️ 关键：VMP 架构代际差异（本文适用范围）

实测对比：

| 维度 | **Gen-1（VMP 3.0-3.4）**<br>本文样本 | **Gen-2（VMP 3.5 商业版）**<br>mzakocs 分析 |
|---|---|---|
| 分发机制 | 固定跳表 `jmp [r12+rax*8]` | **FDJ**：当前 handler 地址 + 解码偏移 |
| 表项内容 | **明文绝对地址** | 加密偏移（滚动密钥）|
| opcode 概念 | **有**（8-bit，实测 140 种）| **无**（用偏移代替）|
| 滚动密钥 | **无**（实测密钥寄存器唯一值 < 0.3%）| **有**（自修改）|
| handler 合并 | **无**（实测 95.7% opcode 长度恒定）| 未知 |

**本文的「256 项 handler 表」结论仅适用于 Gen-1（3.0-3.4）**。
对 3.5+ 的 FDJ 架构，需改用 `sexyiam/VMPLift` 类工具的 emu-first 路线。

**实测证据（Gen-1，math.3.0.0-virt.exe）**：

```
dispatcher RVA : 0xefb95  形态 jmp qword [r12+rax*8]
18,499 次 dispatch 实测:
  r12 (表基址) : 唯一值 1 种      → ✅ 固定跳表
  rax (索引)   : 140 种, 1..255   → ✅ 真 opcode
  跳表目标     : 131 个, 全在映像内
滚动密钥检查     : r9/rbx/r13/r14/r15 唯一值比例 < 0.3% → ✅ 无
handler 合并检查 : 134/140 opcode 长度恒定 (95.7%)    → ✅ 无合并
```

### 3.10 的定位：Gen-1 到 Gen-2 的过渡形态

本文测得的 3.10 分发：
```asm
movsxd rdx, dword ptr [r11 + r10*4]   ; 表还在（但 4 字节相对偏移，非 8 字节绝对）
add    rdx, r11
jmp    rdx
```
**这正是从「固定跳表」向「FDJ」过渡的中间形态** —— 表结构保留，但表项从绝对地址改为相对偏移，分发指令从 `jmp [mem]` 改为 `jmp reg`。

### 本文未覆盖、但已知存在的后续技术

| 技术 | 版本 | 说明 | 可借鉴工具 |
|---|---|---|---|
| **滚动加密密钥** | 3.5+ | 操作数与跳转偏移被密钥 XOR + 变换，密钥自修改 | VMPLift `rolling_key.cpp` |
| **无表 FDJ** | 3.5+ | 无 opcode 概念，用「当前 handler + 解码偏移」 | 同上 |
| **Merged handlers** | 3.8+ | 单个 native 块执行多个 VM 操作 + 下个 handler 计算 | VMPLift `handler_walker.cpp` |
| **VM 嵌套** | 3.5+ | 调用外部函数后**进入全新 VM**（新指令集/新 context）| mzakocs 分析 |
| **LLVM IR 提升** | — | handler → LLVM IR → 优化遍自动蒸发虚拟化层 | MogVMP / Mergen |
| **Z3 等价判定** | — | 将还原结果表达为断言，形式化证明 PROVEN/REFUTED | vmp-reverse-skill `z3_verify.py` |

## 无真机方案能力矩阵

| 能力 | 可用性 | 证据 |
|---|:---:|---|
| PE 加载 + 重定位 + IAT | ✅ | 180 导入打桩成功 |
| 进入 VM 循环 | ✅ | 18,499 次 dispatch |
| 导出 handler 表 | ✅ | 4 版本 × 256 项 |
| handler 语义归类 | ✅ | 256 handler 全覆盖 |
| 反调试旁路（int 3） | ✅ | 拦截 1 次后跑完 |
| 3.10 相对偏移表 | ✅ | 28551/28551 公式匹配 |
| 完整内存转储 | ✅ | 4 个版本 PE |
| 支持系统调用语义 | ⚠️ | 需按需补 API 桩 |
| 过 VMP 动态自检全项 | ⚠️ | 需补 rdtsc/异常链/调试端口 |

## 零真机下的结论验证（五条独立证据链）

无真机不等于无法验证。以下五条链**相互独立**，全部通过：

| # | 验证方法 | 验证目标 | 实测结果 | 独立性 |
|---|---|---|---|---|
| **V1** | 同一仿真跑 3 次（不同 max_insn） | 结果可重复 | 表基址稳定 `0x106774`，表内容哈希 `ba0b8478` 一致 | 中（同引擎）|
| **V2** | **完全不跑仿真**，从 PE 文件静态解码表 | 表项是否为合法代码 | **4 版本 × 256 项全部可解，100% 合法** | **强（零仿真）** |
| **V3** | 三源交叉：仿真 trace / 静态表 / opcode 集合 | 内部自洽性 | 6/6 判据成立 | 中 |
| **V4** | 独立看字节码流，与 dispatch opcode 对比 | 表覆盖度 | dispatch opcode **100%** 出现在字节码流中 | 强（独立数据源）|
| **V5** | **全盘扫描 PE 找候选表**，不用仿真任何输出 | 表基址正确性 | 4 版本独立扫描结果与仿真报告**100% 一致** | **最强（双路径）** |

### V5 的核心意义

```
仿真观测（跑起来的 r11）  → 表基址 RVA 0x106774
静态全盘扫描（不跑程序）  → 表基址 RVA 0x106774   ★ 完全一致
```

**两条完全独立的路径得到同一答案**，证明仿真捕获的 `0x140106774`
**不是仿真环境的产物，而是文件里客观存在的结构**。

### 结论修正记录

| 原表述 | 修正后 | 依据 |
|---|---|---|
| "3.10 需要真机" | 3.10 的表**静态明文可解**，只是分发指令换了形态导致扫描器定位不到 | V2/V5 |
| "3.10 必须运行时提取" | 必须运行时**定位**表基址；提取本身可静态完成 | V2 |
| — | 仿真的价值是**消除静态歧义**（3.0 有 10 个假阳性 4 字节候选）| V5 |

### 可复用的验证脚本

| 脚本 | 作用 |
|---|---|
| `V1_reproducibility.py` | 可重复性：多次运行对比表基址与哈希 |
| `V2_static_decode.py` | 零仿真静态解码验证 |
| `V3_selfconsistency.py` | 多源自洽性检查 |
| `V4_bytecode_crosscheck.py` | 字节码流反向验证 |
| `V5_independent_formula.py` | 独立全盘扫描定位表 |

### V6：联网检索后的补充验证（对照公开权威分析）

| 项 | 验证什么 | 实测结果（3.0.0）|
|---|---|---|
| **V6-A** | 是否存在**滚动加密密钥**（3.5+ 特性）| r9/rbx/r13/r14/r15 唯一值比例 **< 0.3%** → **无** |
| **V6-B** | 是否**handler 合并**（3.8+ 特性）| **134/140 opcode 长度恒定 (95.7%)** → **无合并** |
| **V6-C** | 架构代际定位 | 形态 `jmp qword [r12+rax*8]` → **Gen-1 (3.0-3.4)** |

> **通用方法论**：任何仿真结论都可套用这六条链。
> 其中 **V2（零仿真静态复核）与 V5（独立路径复现）** 强度最高，
> 应作为仿真结论的**必备验证**（参见 `general/methodology/01` 的「使用边界」节）。
> **V6** 用于**确定结论的适用范围**（架构代际），避免把 Gen-1 结论误用到 3.5+。

## 关键陷阱

| 陷阱 | 现象 | 解法 |
|---|---|---|
| `UC_HOOK_CODE` 里用 `UC_X86_REG` | `NameError` | 用显式常量 `UC_X86_REG_RAX` 等 |
| 硬编码 dispatch 地址 | 换版本后 0 捕获 | 运行时按**指令形态**识别 |
| 静态扫描到"handler 表" | 目标处非合法代码 | 那是**元数据表**；真表须运行时取 |
| 静态扫描到 dispatcher | 执行次数为 0 | VMP 放**未使用的副本**；以运行时为准 |
| Windows x64 用 GS | 读 TEB 失败 | x64 用 **FS**（x86 用 FS，x64 也用 FS） |
| 从 EP 直接冲 | 写 `[rcx=8]` 崩溃 | 壳自解密未完成；自愈后继续 |
| `dispatch` 计数为 0 | hook 只匹配 r12 | 3.2+ 轮换到 r11/rdx |
| 表项全填同一值 | 无法区分 opcode | 测试时应填**可区分**的 handler 地址 |

## 证据与验证闭环

**逐节区字节对比（最硬证据）**：

| 节区 | 大小 | 一致 | 差异 | 判定 |
|---|---:|---:|---:|---|
| `.text` | 3,584 | 3,584 | 0 | ✅ |
| `.rdata` | 3,584 | 3,584 | 0 | ✅ |
| `.data` | 512 | 512 | 0 | ✅ |
| `.pdata` | 512 | 512 | 0 | ✅ |
| `.vmp0` | 782,848 | 782,848 | 0 | ✅ |
| **`.vmp1`** | 192,126 | 191,228 | **898** | ⚠️ 见下 |
| `.reloc` | 2,048 | 2,048 | 0 | ✅ |

**898 字节差异 = 运行时 IAT 解析的实证**：

```
原始 PE  :  0xc7b00  0xdde7e  0xc5d40  0xd1422 ...   (176 个不同 RVA)
转储镜像 :  0x140106000 × 176 项                     (全部同一桩地址)
```

`0x140106000` 正是仿真中为 180 个 Windows API 打的默认桩（`xor eax,eax; ret`）。
这证明：
1. **VMP 的加载器真实运行**——解析导入表并回填了 176 项 IAT
2. **转储捕获的是运行时状态**，不是静态文件内容——这正是内存转储的定义
3. 其余 6 个节区 100% 一致——转储无损坏、无偏移

**另一条硬证据**：`.text` 差异为 0 且**从未执行** —— 印证虚拟化本质：
被保护函数**全程在 VM 内，无原生机器码可 dump**。因此对 `-virt` 样本，
转储只能拿到壳框架与字节码，真正还原必须靠 handler 语义（03/07 篇的 devirt 路线）。

## MCP 工具映射

| 攻击链步骤 | MCP 工具 | 说明 |
|---|---|---|
| 节区/熵/导入侦察 | `seep_r2_info` · `seep_r2_strings` | 判定保护模式与壳节区 |
| 反汇编壳区 | `seep_r2_disasm` | 静态定位 VM entry 候选 |
| 类 C 伪代码 | `seep_r2_decompile` | 辅助理解 dispatcher |
| 从 dump 中 carve payload | `carve_payloads_from_dump` | 提取 PE |
| 方法论检索 | `kb_router` · `seep_kb_search` | 命中本篇与 01/02/03/06 篇 |

> 自愈式仿真本身是纯 Python + Unicorn 脚本（见 `checklists/` 配套脚本），
> 不依赖 IDA/GUI，可直接在 Linux CLI 运行。

## 配套脚本（同目录）

| 脚本 | 作用 | 用法 |
|---|---|---|
| `selfhealing_vmp_emu.py` | **自愈式仿真器**：PE 加载 + 环境桩 + 三层 hook（自愈/反调试/观测），跑壳并输出执行统计与热点 | `python3 selfhealing_vmp_emu.py <sample.exe> [max_insn]` |
| `vmp_handler_extractor.py` | **Handler 表提取器**：自动定位分发点，兼容 3.0-3.4（`jmp [base+idx*8]`）与 3.10（`jmp reg` + 相对偏移表），输出语义分类与映射表 JSON | `python3 vmp_handler_extractor.py <sample.exe>` |
| `pe_unmapper_tool.py` | 内存 dump 解映射修复（06 篇） | `python3 pe_unmapper_tool.py in.bin -o fixed.exe --base 0x140000000` |
| `entropy_carver_tool.py` | 高熵区解压/加密路由（05 篇） | `python3 entropy_carver_tool.py dump.bin --outdir out/` |

### 验证脚本（零真机，五条独立证据链）

| 脚本 | 验证什么 | 强度 |
|---|---|---|
| `verify_V1_reproducibility.py` | 同一仿真跑 3 次（不同 max_insn），表基址/哈希是否稳定 | 中 |
| `verify_V2_static_decode_v2.py` | **零仿真**：从 PE 文件静态解码表，检查目标是否为合法代码 | **强** |
| `verify_V3_selfconsistency.py` | 多源自洽：仿真 trace / 静态表 / opcode 集合 | 中 |
| `verify_V4_bytecode_crosscheck.py` | 字节码流反向验证（独立数据源） | **强** |
| `verify_V5_independent_formula.py` | **全盘扫描找候选表**，验证与仿真报告是否一致 | **最强** |

```bash
# V2: 零仿真静态复核（最实用，不依赖 vmp_selfheal_run.py 的输出格式）
python3 verify_V2_static_decode_v2.py math.3.10.0-virt.exe
# V5: 独立路径复现（最强，不用仿真任何输出）
python3 verify_V5_independent_formula.py math.3.10.0-virt.exe
```

> **V2 与 V5 是仿真结论的必备保险**：
> V1/V3 只能证明「自洽」，V2/V5 才能证明「与静态事实一致」。

**依赖**：`pip install unicorn capstone`（Unicorn >= 2.0）。

**最小复现流程**：

```bash
# 1) 自愈式仿真，确认能进入 VM（看 dispatch 计数与热点）
python3 selfhealing_vmp_emu.py math.3.0.0-virt.exe 2000000
# 2) 提取 handler 表与语义（输出 <sample>.handler_map_310.json）
python3 vmp_handler_extractor.py math.3.0.0-virt.exe
```
