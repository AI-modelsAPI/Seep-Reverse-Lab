# 2026-10-16 VMProtect 官方 Demo 全版本：无真机自愈式仿真 → Handler 表提取 → 字节码反编译

## 场景分类

二进制分析 / VMProtect 虚拟化壳 / 无真实环境模拟执行 / 内存转储与还原解包 / Handler 语义还原

## 目标概述

对 VMProtect 官方 Demo 全系列（3.0.0 / 3.2.0 / 3.4.0 / 3.10.0，共 20 个样本，含 math/conditional/printf 三种形态）
执行端到端白盒审计：在**无 Windows 沙箱、无真机、无 x64dbg** 的条件下，用 Unicorn 自愈式仿真完整跑通壳，
提取 256 项 handler 表，破译 VM 指令集语义，定位并反编译 VM 字节码流，产出可拖入 IDA 的分析镜像。

## Scope 摘要（脱敏）

- auth_basis: 授权沙箱样本（开源官方 Demo，`windows/vmp-samples/`）
- network_profile: offline（全程离线，无网络交互）
- asset_types: ["PE x64 可执行文件", "VMProtect 虚拟化保护壳"]

## 角色

- lead_role: lead
- specialists: []

## 完整执行链路

### 阶段一：静态侦察与保护模式分类

1. `file` / `rabin2 -S` 摸底 20 个样本 → 全部 PE32+ x86-64，7–8 个节区
2. 节区名观察：3.0/3.2 用默认名 `.vmp0`/`.vmp1`；**3.4+ 改用混淆随机名**（`.awC`/`.h#o`/`.2Ha`）
3. **关键发现**：`-pack` 样本的 `.text/.rdata/.data/.pdata` 四个原始节区 `PointerToRawData=0 / SizeOfRawData=0`
   —— 磁盘上是**零填充空洞**，熵值为 **0.000**；而壳节区熵 **7.58–7.60**
4. 对比 `-virt` 样本：全部节区熵 5.67–5.95（正常代码），**无压缩**
5. **得出路由决策**：
   - `-pack` → 必须运行时 dump（磁盘上无原始代码）
   - `-virt` → dump 只能拿壳框架，必须走 handler 语义还原
   - `-antidbg` → 先过反调试

### 阶段二：Dispatcher 静态定位（成功的弯路）

6. 写字节模式扫描器找 `0F B6` 取指 + `FF 24` 查表分发的**紧邻模式**
7. 在 `math.3.0.0-virt.exe` 命中 2 个候选：
   - `.vmp0 @ 0x1400aae22`：`0F B6 06 | 41 FF 24 C4`
   - `.vmp1 @ 0x1400efb92`：同一字节模式
8. 扫描"密集代码指针表" → 在 `.vmp0 RVA 0x2c048` 找到 123 项递增 RVA 序列
9. **一度误判为 handler 表** → 二次验证发现目标处字节 `0b4519 43140111...` 按 16-bit 解释呈递减序列
   → **修正为 VMP 元数据表**
10. 用 `lea r12,[rip-0x536a4]` 静态算表基址 = `0x140057775`，但该处内容是加密混合数据
    → **静态路线到此为止，必须动态**

### 阶段三：切片仿真实证分发语义

11. 把 dispatcher 那 14 字节切出来喂给 Unicorn（`disp_slice_emu3.py`）
12. 构造可区分的测试表（`table[i] = 0x4000 + i*0x10`），扫描 12 个 opcode
13. **12/12 全部通过**：`RAX` 精确等于 opcode，跳转目标精确等于 `table[opcode]`
14. 确证语义：`handler_ptr = *(uint64_t*)(r12 + opcode*8)`，opcode 为 8-bit

### 阶段四：PE 加载器（ELF 模板的 PE 化改造）

15. 参照 KB `r2pay_headless_emulator.py`（ELF 版三件事）改写 PE 版：
    - 节区映射（替代 PT_LOAD）
    - `.reloc` 基址重定位（替代 `.rela.dyn`/`.rela.plt`）
    - IAT 打桩（替代 GOT）
16. `math.3.0.0-virt.exe` 成功打桩 **180 个导入函数**（来自 10 个 DLL）

### 阶段五：环境桩与自愈式仿真（核心突破）

17. 补 Windows 运行时：TEB/PEB（`FS_BASE=TEB`）+ `BeingDebugged=0` + 堆 + 栈哨兵
18. 首次仿真：14,643 条指令后崩在 `mov [rcx],rax`（`rcx=8`）
19. 诊断：`mov rax,[rsp+opcode]` 读宿主栈 —— VM context 依赖此前副作用，静态无法预测
20. **策略转变 → 自愈式仿真**：`UC_HOOK_MEM_*_UNMAPPED` 自动映射缺失页并重试
21. 提升到 291,523 条指令，停在 `UC_ERR_EXCEPTION`
22. 挂 `UC_HOOK_INTR` 发现 **`int 3 @ RVA 0xede7d`** —— VMP 反调试陷阱
23. **忽略陷阱后跑完**：**2,086,502 条指令，18,499 次 dispatch，140 种 opcode，自然结束**

### 阶段六：VM Entry 全景还原

24. 记录 EP→首次 dispatch 的完整 92 条轨迹，破译：
    ```
    0xefb34: mov rbp, rsp          ; VM 栈 = 当前栈
    0xefb3f: sub rsp, 0x180        ; VM context 大小
    0xefb54: mov rbx, rsi          ; <- VMEXIT 返回点
    0xefb75: lea r12, [rip-0x14f4] ; r12 = 0x1400ee688
    ```
25. **双向验证**：静态算的 `0x1400ee688` 与仿真捕获的 `r12` 完全一致
26. **重大修正**：真正执行的 dispatcher 是 `.vmp1 @ 0x1400efb92`（870+ 次），
    `.vmp0 @ 0x1400aae22` 是**未使用的副本，执行次数 0**

### 阶段七：Handler 表多版本提取

27. 初版 hook 硬编码 `41 FF 24 C4` → 3.2/3.4 捕获 0 个
28. **改为运行时按指令形态识别**（`jmp/call [base+index*8]`）
29. 结果：3.0.0 (18,499) / 3.2.0 (18,134) / 3.4.0 (18,186) 全部捕获，各 256 项

### 阶段八：攻克 3.10.x（最难环节）

30. 3.10 执行 755,445 条指令但 **dispatch 事件 0**
31. 分析发现：3.10 **完全没有 `jmp [mem]` 形态**（其他 jmp 形态统计为零）
32. 热点分析定位分发点 `RVA 0x101149`：
    ```
    0x101124: movzx  r10d, byte ptr [rsi]
    0x101132: add    rsi, 1
    0x101142: movsxd rdx, dword ptr [r11 + r10*4]   ; ★ 32位相对偏移表
    0x101146: add    rdx, r11
    0x101149: jmp    rdx                            ; ★ 寄存器分发
    ```
33. 提取验证：**28,551/28,551 公式匹配（100%）**，表基址 `r11 = 0x140106774`
34. 得到 256 项表（全部指向映像内），133 种 opcode

### 阶段九：Handler 语义建模与字节码反编译

35. 三轮语义分析器迭代（关键词 → 数据流 → 模式匹配）
36. **关键发现**：`[rsp + rax]` 是 **VMP 的虚拟寄存器重映射表**
    ```
    opcode=0x24: mov rcx,[rbp] ; add rbp,8 ; mov [rsp+rax],rcx
    opcode=0x96: mov rax,[rsp+rax] ; sub rbp,8 ; mov [rbp],rax
    ```
37. 256 handler 语义分类：`vm_pop` (**66 变体**) / vm_sub (27) / vm_shl (21) / vm_push (16) / vm_exit (10)
38. 提取 VM 字节码流：RVA `0xc5b9f..0xe9a00`（在 `.vmp1` 内），11,599 唯一位置，167 种 opcode
39. 交叉验证：handler 表 `0xee036+` 与字节码 `0xc5b9f-0xe9a00` **完全分离**
40. 过滤 67% 装饰后的真实指令流：`vm_push_imm64(1402)` / `vm_add(708)` / `vm_and(630)` / `vm_rcr(350)`

### 阶段十：内存转储与解映射

41. 从仿真内存导出 Virtual Layout 镜像（4 个版本，1.0–1.3 MB）
42. 应用 KB 06 篇三步曲解映射修复 → 合法 PE32+，`Ptr2Raw == VA`
43. **逐节区字节对比验证**：6/7 节区 100% 一致，仅 `.vmp1` 有 898 字节差异
44. **差异定位**：集中在 RVA `0xe0000`，原始是 176 个不同 RVA，转储后全变 `0x140106000`
    —— 这正是仿真中打的 180 个 API 桩地址，**证明 VMP 加载器真实运行并回填了 IAT**

## Evidence 链摘要（脱敏）

| E-id | severity | status | source_type | 可复用命令模式 | 关联 Finding |
|------|----------|--------|-------------|----------------|--------------|
| E-001 | info | validated | command | `python3 disp_slice_emu3.py` (12/12 通过) | F-001 dispatcher 语义 |
| E-002 | high | validated | command | `python3 extract_310_final.py` (28551/28551 公式匹配) | F-002 3.10 相对偏移表 |
| E-003 | high | validated | artifact | 逐节区字节对比，6/7 节区一致 + 898 字节 IAT 差异 | F-003 转储有效性 |
| E-004 | high | validated | command | `python3 verify_V2_static_decode_v2.py` (4 版本 × 256 = **1024/1024** 合法代码) | F-004 零仿真静态复核 |
| E-005 | high | validated | command | `python3 verify_V5_independent_formula.py` (独立扫描与仿真基址 **100% 一致**) | F-005 双路径同结论 |
| E-006 | high | validated | command | `python3 verify_V6_online_crosscheck.py` (无滚动密钥 / 无 handler 合并 / **Gen-1 架构定位**) | F-006 适用范围界定 |

## Finding / Path 摘要

- top_finding: VMP 全版本 handler 表与 VM 指令集可在无真机条件下通过自愈式仿真完整提取，并经**五条独立证据链**验证
- path_type: solve
- path_one_liner: 自愈式 Unicorn 仿真跑完壳 → 运行时 hook dispatch → 导出 256 项 handler 表 → **零仿真静态复核(V2) + 独立路径复现(V5)** → 语义建模 → 字节码反编译

## 结论验证（零真机，六条独立链）

| # | 方法 | 实测结果 | 强度 |
|---|---|---|---|
| V1 | 同一仿真跑 3 次 | 表基址稳定 `0x106774`，哈希 `ba0b8478` 一致 | 中 |
| **V2** | **零仿真**从文件静态解码 | **4 版本 × 256 = 1024/1024 全部合法代码** | **强** |
| V3 | 三源自洽 | 6/6 判据成立 | 中 |
| V4 | 字节码流反向验证 | dispatch opcode **100%** 出现在字节码流中 | 强 |
| **V5** | **全盘扫描**找候选表 | 4 版本独立扫描与仿真报告 **100% 一致** | **最强** |
| **V6** | **对照公开权威分析** | **无滚动密钥 / 无 handler 合并 / Gen-1 架构定位** | 界定适用范围 |

**V5 核心结果**：
```
仿真观测（跑起来的 r11）  → 表基址 RVA 0x106774
静态全盘扫描（不跑程序）  → 表基址 RVA 0x106774   ★ 完全一致
```

### 重要认知修正

| 原表述 | 修正后 | 依据 |
|---|---|---|
| "3.10 需要真机" | 表**静态明文可解**，只是分发指令换成 `jmp reg` 导致扫描器定位不到 | V2/V5 |
| "必须运行时提取" | 必须运行时**定位**表基址；提取本身可静态完成 | V2 |
| — | 仿真价值 = **消除静态歧义**（3.0 有 10 个假阳性 4字节候选）| V5 |

### 联网检索后的重大发现（V6）

**对照权威分析（mzakocs VMP3，77★ 配套 IDA 库）**，发现 **VMP 存在架构代际差异**：

> mzakocs 原文：**"VMProtect... does not use opcodes or a handler table. Instead, it uses an offset that is decoded with the self-modifying decryption key and added to the address of the current handler."**

| 维度 | **Gen-1（3.0-3.4，本样本）** | **Gen-2（3.5 商业版）** |
|---|---|---|
| 分发 | 固定跳表 `jmp [r12+rax*8]` | **FDJ**：当前 handler 地址 + 解码偏移 |
| 表项 | **明文绝对地址** | 加密偏移 |
| opcode | **有**（实测 140 种）| **无** |
| 滚动密钥 | **无** | **有**（自修改）|
| handler 合并 | **无** | 未知 |
| VM 嵌套 | 未观测 | **有**（调用外部函数后入新 VM）|

**V6 实测证据（3.0.0，18,499 次 dispatch）**：
```
r12 (表基址)  : 唯一值 1 种      → ✅ 固定跳表
rax (索引)    : 140 种, 1..255   → ✅ 真 opcode
滚动密钥检查  : r9/rbx/r13/r14/r15 唯一值 < 0.3% → ✅ 无
handler 合并  : 134/140 opcode 长度恒定 (95.7%)  → ✅ 无合并
架构定位      : jmp qword [r12+rax*8] → Gen-1 (3.0-3.4)
```

**结论**：本次分析的 256 项 handler 表结论**仅适用于 Gen-1（3.0-3.4）**。
对 3.5+ 的 FDJ 架构需改用 emu-first 路线（参考 `sexyiam/VMPLift`）。

### 本文未覆盖、但已确认存在的后续技术

| 技术 | 版本 | 可借鉴工具 |
|---|---|---|
| 滚动加密密钥 | 3.5+ | VMPLift `rolling_key.cpp` |
| 无表 FDJ | 3.5+ | 同上 |
| Merged handlers | 3.8+ | VMPLift `handler_walker.cpp` |
| VM 嵌套 | 3.5+ | mzakocs 分析 |
| LLVM IR 提升 + 优化遍 | — | MogVMP / Mergen |
| **Z3 形式化等价判定** | — | vmp-reverse-skill `z3_verify.py` |

> 其中 **Z3 等价判定**（PROVEN/REFUTED/FUZZED，无「我觉得等价」档位）
> 比本次的 V1-V6 更强，是后续升级方向。

## 踩坑记录

| 问题 | 原因 | 解决方案 | 耗时 |
|---|---|---|---|
| `UC_X86_REG` NameError | Unicorn Python 绑定无此常量类 | 用显式常量 `UC_X86_REG_RAX` 等，建 REG_MAP 字典 | 低 |
| 静态扫描到 123 项"handler 表" | 实为 VMP 元数据表，目标处非合法代码 | 二次验证目标字节（按 16-bit 解释呈递减序列）→ 修正判定 | 中 |
| 静态算出的 r12 与扫描表不匹配 | 两者是不同东西；真表由运行时决定 | 放弃静态，改用切片仿真实证 | 中 |
| 从 EP 直冲崩在 `mov [rcx=8],rax` | VM context 依赖此前副作用，壳自解密未完成 | **自愈式仿真**：自动映射 + 继续 | 中 |
| 291,523 条后 `UC_ERR_EXCEPTION` | VMP 反调试 `int 3 @ RVA 0xede7d` | `UC_HOOK_INTR` 回调返回 True 忽略 | 中 |
| 3.2/3.4 的 dispatch 捕获为 0 | hook 硬编码 `41 FF 24 C4`，3.2+ 轮换到 r11/rdx | 改为**运行时按指令形态识别** `[base+index*8]` | 中 |
| 3.10 完全无 dispatch 事件 | 分发是 `jmp rdx`（寄存器），非 `jmp [mem]` | 热点分析定位分发点，抓 r10/r11/rdx 三寄存器 | 高 |
| 切片仿真测试表全填 0xAA | 无法区分 opcode | 填可区分值 `0x4000 + i*0x10` | 低 |
| 语义分类器 233 个误判 `vm_next` | `get_body` 在首条 jmp 处停止，只看 1-2 条指令 | 跟踪到跳回 dispatcher；用数据流而非关键词 | 高 |
| 语义分类器 104 个误判 `vm_flags` | `pushfq/popfq` 作花指令随处可见 | 只保留操作数涉及 `[rbp]`/`rsi`/`rsp` 的指令 | 中 |
| Windows x64 读 TEB 失败 | 误用 GS（x64 实际用 **FS**） | `UC_X86_REG_FS_BASE = TEB` | 低 |
| 二次运行捕获为 0 | `SelfHealingEmu` 每次是全新状态，路径不同 | 改为**单次运行内**动态发现分发点 + 捕获 | 中 |

## 工具链发现

- **Unicorn 2.1.4 已足够**：无需 Qiling/angr/Triton，纯 Python + Unicorn 即可完成 VMP 全流程仿真。
  `UC_HOOK_MEM_*_UNMAPPED` + `UC_HOOK_INTR` 两个 hook 是自愈式仿真的全部关键。
- **`UC_HOOK_MEM_*_UNMAPPED` 返回 True 表示"已处理，重试当前指令"**，返回 False 才上报异常。
  这是自愈机制的核心，KB 现有文档未记载。
- **KB 的 ELF 版模板可直接 PE 化**：`r2pay_headless_emulator.py` 的三件事（重定位/init_array/TLS）
  与 PE 的三件事（.reloc/IAT/TEB）一一对应，改写成本低。
- **`rabin2 -S` + 自定义 PE 解析脚本**足以完成保护模式分类，无需 DiE。
- **图片化验证报告**对非技术用户极有效：把逐节区字节对比做成 PNG，一眼可见。

## 关键代码/命令

```python
# ① 自愈式仿真核心（三层 hook）
from unicorn import *
from unicorn.x86_const import *

mu = Uc(UC_ARCH_X86, UC_MODE_64)
auto_pages = set()

def map_page(addr):
    page = addr & ~0xFFF
    if page in auto_pages: return False
    try:
        mu.mem_map(page, 0x1000, UC_PROT_ALL); auto_pages.add(page); return True
    except UcError:
        return False

# 自愈层: 返回 True = 已处理, 重试当前指令
mu.hook_add(UC_HOOK_MEM_READ_UNMAPPED,  lambda uc,a,ad,s,v,u: map_page(ad) or True)
mu.hook_add(UC_HOOK_MEM_WRITE_UNMAPPED, lambda uc,a,ad,s,v,u: (map_page(ad), True)[1])
mu.hook_add(UC_HOOK_MEM_FETCH_UNMAPPED, lambda uc,a,ad,s,v,u: map_page(ad) or True)

# 反调试旁路层
mu.hook_add(UC_HOOK_INTR, lambda uc, intno, ud: True)
```

```python
# ② 通用 dispatch 捕获（适配寄存器轮换 + 两种分发形态）
REG_MAP = {'rax': UC_X86_REG_RAX, 'rcx': UC_X86_REG_RCX, 'rdx': UC_X86_REG_RDX,
           'rsi': UC_X86_REG_RSI, 'rdi': UC_X86_REG_RDI, 'rbx': UC_X86_REG_RBX,
           'r8': UC_X86_REG_R8, 'r9': UC_X86_REG_R9, 'r10': UC_X86_REG_R10,
           'r11': UC_X86_REG_R11, 'r12': UC_X86_REG_R12, 'r13': UC_X86_REG_R13,
           'r14': UC_X86_REG_R14, 'r15': UC_X86_REG_R15}

def on_code(uc, addr, size, ud):
    ins = next(md.disasm(bytes(uc.mem_read(addr, 15)), addr))
    # 形态A (3.0-3.4): jmp qword [base + index*8]
    if ins.mnemonic in ('jmp','call') and '[' in ins.op_str and '*8' in ins.op_str.replace(' ',''):
        inner = ins.op_str[ins.op_str.index('[')+1:ins.op_str.rindex(']')].replace(' ','')
        b = i = None
        for p in inner.split('+'):
            if '*' in p: i = p.split('*')[0]
            elif p in REG_MAP: b = p
        if b and i:
            bv = uc.reg_read(REG_MAP[b]); iv = uc.reg_read(REG_MAP[i])
            tgt = struct.unpack('<Q', uc.mem_read((bv+iv*8)&0xFFFFFFFFFFFFFFFF, 8))[0]
    # 形态B (3.10): jmp rdx, rdx = [r11 + r10*4] + r11
    elif ins.mnemonic == 'jmp' and ins.op_str in REG_MAP:
        r10 = uc.reg_read(UC_X86_REG_R10); r11 = uc.reg_read(UC_X86_REG_R11)
        tgt = uc.reg_read(REG_MAP[ins.op_str])
        off = struct.unpack('<i', uc.mem_read(r11 + r10*4, 4))[0]
        assert (r11+off) & 0xFFFFFFFFFFFFFFFF == tgt   # 100% 匹配验证
    return True
```

```python
# ③ 解映射修复（KB 06 篇三步曲）
struct.pack_into('<I', data, opt + 36, sa)          # FileAlignment = SectionAlignment
for sec in sections:
    struct.pack_into('<I', data, off + 16, align_up(vsize, sa))  # SizeOfRawData
    struct.pack_into('<I', data, off + 20, rva)                  # PtrToRawData = VA
```

## 对本包的改进建议

1. **`general/methodology/01-headless-emulation-windows-android-handbook.md` 已补充「自愈式仿真」章节** ✅
   （2026-10-16 已执行）—— 原文只讲“精确复刻”（Qiling 全系统、Unicorn 手工补环境），
   现已覆盖“遇错自动修”范式，并明确 `UC_HOOK_MEM_*_UNMAPPED` 的重试语义。
2. **`pe-reverse/05-crypto-unpack/02-vmp-virtualization-analysis.md` 应补 3.10 分发机制**
   —— 原文表格说“3.x 间接跳转被加密/运行时计算”，但没给出**具体实现形式**
   （32 位相对偏移表 + `jmp reg`）。本次已实证并写入新篇 08。
3. **`03-vmp-devirtualization-toolchain.md` 的三级降级策略应增加“第 0 级”**
   —— 在 NoVmp/Triton/trace 之前，还有一个更前置的选项：
   **自愈式仿真直接跑壳并提取运行时数据**，成本远低于三者。
4. **`general/techniques/kb-index.json` 的 methodology 分类存在路径映射缺陷** ✅
   （2026-10-16 已修复）—— `general/methodology/` 下的两篇文档（01-headless-emulation、
   02-remote-mcp-device-bridge）之前**未被 kb-index 收录**，现已挂接。
5. **建议在 `headless_slice_emulator_tool.py` 旁增加 `selfhealing_vmp_emu.py`** ✅
   （2026-10-16 已入 `05-crypto-unpack/`）作为可复用脚本。

## 可复用的模式/脚本片段

### 模式 1：保护模式自动分类

```
原始节区(raw=0) 存在  -> PACK   -> 必须运行时 dump
节区名 .vmp0/.vmp1     -> VMP2 经典命名
节区名 混淆随机        -> VMP3.4+ 改了节区名选项
壳节区熵 > 7.5         -> 压缩/加密
全节区熵 5-6           -> 正常代码, 仅虚拟化
```

### 模式 2：dispatcher 定位的双保险

```
静态: 扫 0F B6 + FF 24 紧邻 -> 得到候选（可能有未使用的副本）
动态: 仿真时统计各候选执行次数 -> 次数为 0 的是诱饵
```

### 模式 3：VM 指令集语义判定的过滤原则

```
VMP 插入大量不影响结果的花指令。
辨别: 只保留操作数涉及 [rbp](VM栈) / rsi(vm_ip) / rsp(解密表) 的指令。
其余视为混淆噪声。
```

### 模式 5：仿真结论的零真机验证（五链法）

```
V1 可重复性    → 同仿真跑多次, 表基址/哈希是否稳定
V2 零仿真静态  → 从文件直接解码验证（最强实用）
V3 多源自洽    → trace / 静态表 / 数据集合 交叉
V4 独立数据源  → 字节码流 vs opcode 集合
V5 全盘扫描    → 不用仿真输出, 自己重新推导（最强）

关键: V2+V5 是必备 —— V1/V3 只能证明「自洽」,
      V2/V5 才能证明「与静态事实一致」。
```

### 模式 6：区分「明文但难定位」与「加密」

```
发现静态扫描失效时, 不要急于下结论「数据被加密」。
先验证: 假定一个基址, 按不同宽度解释表项, 看目标是否为合法代码。

本例: VMP 3.10 的表静态明文(4字节相对偏移),
      只是分发指令 jmp reg 导致扫描器扫不到位置。
判据: 静态能解码出 100% 合法代码 -> 明文, 只是定位难
      静态解出大量 invalid -> 真加密
```

## 进化动作

- [x] 新增技术文档 `pe-reverse/05-crypto-unpack/08-selfhealing-emulation-vmp-handler-extraction.md`
- [x] 新增本 field-journal 条目
- [x] 更新 `field_journal__index.md`（场景分类 + 高频模式 + 实体倒排）
- [x] **更新 `general/methodology/01-headless-emulation-windows-android-handbook.md`**
      —— 新增「四、自愈式仿真（Self-Healing Emulation）」与「五、方案选择决策树」两节，
      将本方法从 PE 专题升级为**跨平台通用方法论**（含三层 Hook 架构、崩溃点推进数据、使用边界、实现陷阱）
- [x] 更新路由矩阵（`kb_maintain.py --signals` 重新生成，2133 信号）
- [x] 更新 kb-index：`pe-reverse/crypto-unpack` 4→58 信号 / 4→8 文件；`general/methodology` 21→29 信号
- [x] 新增 pitfalls 记录（12 条，见踩坑记录表）
- [x] 补充可复用脚本：`selfhealing_vmp_emu.py` + `vmp_handler_extractor.py`（已入 `05-crypto-unpack/`）
- [x] 顺带修复 KB 原有缺陷：`general/techniques/kb-index.json` 中 `methodology` 分类
      的 4 条路径映射，其中 2 条（`general/methodology/*`）之前**未被收录**，现均已挂接

## 环境信息

- OS: Linux (Debian, CLI only，无图形界面)
- 工具版本:
  - Unicorn 2.1.4
  - Capstone 5.0.7
  - Keystone 0.9.2
  - radare2 / rabin2（辅助侦察）
  - Python 3.11
  - 未安装: Qiling, angr, Triton, lief, Wine（均不需要）
- 目标平台/版本: Windows PE32+ x86-64，VMProtect 3.0.0 / 3.2.0 / 3.4.0 / 3.10.0 官方 Demo

## 脱敏要求

- 本条目全部内容为**开源官方 Demo 样本**（VMProtect 官方发布的示例程序），不含任何真实目标信息
- 未涉及任何真实域名/IP/Token/凭据
- 样本哈希可保留（用于复现验证）：
  - `math.3.0.0-virt.exe` SHA256 `1eeeda2618cef5562e86f82c7c0710eb3f40a15ae0021d25b76f8852e2ab6eec`
  - `math.3.10.0-virt.exe` SHA256 `84b6c529aff75f9eb367434e4d573e283cdfbd153951fe224ce4dc3fdf46f9f5`

## 索引同步（提交前最后一步）

- [x] 在「按场景分类 → 二进制 / 固件 / CTF」新增一行
- [x] 在「高频成功模式（按技术）」新增「VMProtect 虚拟化壳无真机仿真」小节
- [x] 在「实体倒排（按目标特征）」新增「VMProtect 保护 PE」小节
- [x] 更新「统计」的总数与"最近更新"日期

---
<!-- [进化统计] 本包累计完成项目: 24 | 本次新增模式: 4 | 本次修复工具链问题: 0 -->
