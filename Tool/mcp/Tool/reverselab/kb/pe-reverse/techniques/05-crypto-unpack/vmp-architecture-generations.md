# 联网检索结果：VMP 验证技术与我的分析对照

检索时间：2026-10-16
检索来源：GitHub API / Crossref / Semantic Scholar / DuckDuckGo

---

## 一、找到的关键项目/文献

### 1. 学术论文

| 文献 | 出处 | 与我的关系 |
|---|---|---|
| **Inspecting Virtual Machine Diversification Inside Virtualization Obfuscation** | **IEEE S&P 2025** (安全顶会) DOI `10.1109/SP61157.2025.00071` | 从 **VM 解释/字节码组织/handler 置换重定位** 三维度分类 VM 多样化 —— 与我的 handler 轮换统计（vm_pop 66 变体）直接对应 |
| **VMHunt** | CCS'18 DOI `10.1145/3243734.3243827` cites=41 | 提出 **trace 切分 + 符号执行 + 语义验证** 三步法 |
| **PolyUnpack** | ACSAC'06 cites=154 | **静态代码模型 vs 动态执行** 交叉判定（我 V2/V5 思路的源头） |
| **QanDe: The Power of Binary Emulation for Obfuscation Analysis** | ICCEA 2025 DOI `10.1109/iccea65460.2025.11102286` | 二进制仿真做混淆分析 |

### 2. 开源工具（按相关度）

| 项目 | Stars | 关键价值 |
|---|---|---|
| **mzakocs/VirtualizationObfuscatorAnalysis** | 77 | **权威 VMP 3.5 分析**（配套博客），揭示 FDJ + 滚动密钥架构 |
| **fjqisba/VmpHelper** | 416 | IDA 插件，标记 VMEntry 后自动识别 handler（仅 3.5 x86）|
| **sexyiam/VMPLift** | 47 | **3.8-3.10 专用，emu-first**；有 `rolling_key.cpp` / `indirect_dispatch.cpp` / `semantic_peel.cpp` |
| **wul7chaos/vmp-reverse-skill** | 13 | **两代 IR + Z3 形式化等价判定**（`PROVEN`/`REFUTED`/`FUZZED`）|
| **eversinc33/MogVMP** | 319 | Remill 提升 + LLVM 优化遍（我的 KB 已有 07 篇）|

---

## 二、🚨 重大发现：VMP 3.5 与 3.0 的架构差异

### mzakocs 的权威结论（VMP 3.5.0 商业版）

> **"VMProtect... does not use opcodes or a handler table. Instead, it uses an offset that is decoded with the self-modifying decryption key and added to the address of the current handler."**

即 **FDJ（Fetch-Decrypt-Jump）架构**：
```
rdi = 当前 handler 地址
rsi -= 4                          (字节码反向读取)
ecx = [rsi]                       (加密的 handler 跳转偏移)
ecx ^= r9                         (r9 = 自修改滚动密钥)
ecx = 4 次随机变换 (neg/rol/inc/neg)
rdi += ecx                        (加到当前 handler 地址)
jmp rdi
r9 更新 (滚动)
```

### 我的实测（VMP 3.0.0 官方 Demo）

```asm
0x1400efb88: sub rsi, 1
0x1400efb8f: movsxd rax, r13d
0x1400efb92: movzx eax, byte ptr [rsi]
0x1400efb95: jmp qword ptr [r12 + rax*8]     ← 固定跳表
```

**18,499 次 dispatch 实测**：
- `r12`（表基址）**只有 1 种值** `0x1400ee688` ✅
- `rax`（索引）140 种，范围 1..255 ✅
- 表项**直接就是明文绝对地址**（`0x1400eff7a` 等）✅

### 结论：不矛盾，是版本差异

| 维度 | VMP 3.0 官方 Demo | VMP 3.5 商业版 |
|---|---|---|
| 分发机制 | **固定跳表** `jmp [r12+rax*8]` | **FDJ**：当前handler地址 + 解码偏移 |
| 表项内容 | **明文绝对地址** | 加密偏移 |
| 是否有 opcode | **有**（8-bit，140 种） | **无**（用偏移代替）|
| 密钥 | 无滚动密钥 | **自修改滚动密钥** |

**我的分析没有错**，但**适用范围应明确标注为「VMP 3.0-3.4 早期架构」**。

### 这解释了 VMP 3.10 为什么不同

我发现的 3.10 分发：
```asm
movsxd rdx, dword ptr [r11 + r10*4]   ← 4 字节表（不是 8 字节）
add    rdx, r11                        ← 加基址
jmp    rdx
```
**这正是从「固定跳表」向「FDJ」过渡的中间形态** —— 表还在，但表项从绝对地址变成了相对偏移。

---

## 三、我遗漏的技术（网上检索发现）

### 1. 🔴 滚动加密密钥（Rolling Key）

mzakocs 和 VMPLift 都强调：**VMP 3.5+ 的操作数（立即数）被滚动密钥加密**。

我的分析**没有检查这一点**。需要验证：我的 3.0/3.10 样本中，handler 里的立即数是否真的明文？

### 2. 🟡 Z3 形式化等价判定

`wul7chaos/vmp-reverse-skill` 提出：LLM 的产出必须是可执行断言，由 Z3 判定：
- `PROVEN` / `REFUTED`（带反例）/ `FUZZED`（超时降级）/ `UNVERIFIED`
- **"没有『我觉得等价』这一档"**

这比我目前的 V1-V5 验证**更强** —— 我的 V3 只是"自洽"，它是**形式化证明**。

### 3. 🟡 合并 handler（Merged Handlers）

VMPLift 指出 3.8+ 特性：

> **"Merged handlers — one native chunk often does several VM ops *and* the next-handler math. Old per-opcode maps just guess wrong."**

我的语义建模假设「1 opcode = 1 handler」，3.8+ 可能不成立。

### 4. 🟡 LLVM IR 提升 + 优化遍

`Mergen` (nac-l) 和 `MogVMP` 都走这条路：
- 把 handler 汇编提升为 LLVM IR
- 用 LLVM 优化遍（SROA/DCE/常量传播）**自动"蒸发"虚拟化层**
- 最终输出 `%realadd = add i32 %0, %1`

这比我的"语义分类"更彻底 —— 我给出「这是 vm_add」，它直接给出**等价的 C 代码**。

---

## 四、可借鉴的验证方法（按强度）

| 方法 | 来源 | 强度 | 可行性 |
|---|---|---|---|
| **静态模型 vs 动态执行差分** | PolyUnpack (2006) | 高 | ✅ 我已做（V2/V5）|
| **trace 切分 + 符号执行 + 语义验证** | VMHunt (CCS'18) | 高 | ⚠️ 需 angr/Z3 |
| **Z3 形式化等价判定** | vmp-reverse-skill | **最高** | ⚠️ 需 pypcode+z3 |
| **多版本样本对照** | IEEE S&P 2025 | 中 | ✅ 我已做（4 版本）|
| **LLVM IR 优化后人工核对** | Mergen / MogVMP | 高 | ⚠️ 需 Remill+LLVM |
| **回归断言（已知输出）** | Qiling test_pe.py | 中 | ✅ 可做 |

---

## 五、立即要做的补充验证

### 补充验证 A：滚动密钥检查（最重要）

验证 3.0/3.10 的 handler 立即数是否明文。

### 补充验证 B：handler 合并检查

验证是否「1 opcode = 1 handler」，还是存在合并。

### 补充验证 C：多版本架构定位

明确 3.0/3.2/3.4/3.10 各属于哪个架构代际。

---

## 六、参考链接

- mzakocs VMProtect 3 分析: https://www.mitchellzakocs.com/blog/vmprotect3
- VMPLift: https://github.com/sexyiam/VMPLift
- vmp-reverse-skill: https://github.com/wul7chaos/vmp-reverse-skill
- MogVMP: https://github.com/eversinc33/MogVMP
- Mergen (nac-l): https://nac-l.github.io/2025/01/25/lifting_0.html
- VmpHelper: https://github.com/fjqisba/VmpHelper
