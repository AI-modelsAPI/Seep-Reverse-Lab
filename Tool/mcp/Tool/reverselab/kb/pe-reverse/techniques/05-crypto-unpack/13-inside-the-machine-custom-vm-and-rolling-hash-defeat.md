---
id: "pe-reverse/05-crypto-unpack/13-inside-the-machine-custom-vm-and-rolling-hash-defeat"
title: "极简自定义虚拟机（Inside-the-Machine）：反调试对抗、Opcode 滚动置换与双重约束求根"
title_en: "Compact Custom VM (Inside-the-Machine): Anti-Debug Countermeasures, Rolling Opcode Permutation, and Dual-Constraint Root Finding"
summary: >
  深度记录针对 24KB 极简自定义虚拟机（Inside-the-Machine）的端到端逆向分析与破译全流程。
  解析其集成的密集反调试机制（QPC 时钟判定 / 快照模块走查）、动态控制台异或解密例程、
  8 个 32 位寄存器的精简虚拟机解释器，以及 Opcode 滚动密钥置换规律。
  识别死代码花指令与无条件混淆跳转，建立 26 组单字符代数约束与全局 Rolling Hash 联合求解方程，
  实现 26 字节 Flag/Password 的毫秒级精确提取与实机 100% 验证。
summary_en: >
  End-to-end reverse engineering and defeat workflow for a 24KB compact custom virtual machine (Inside-the-Machine).
  Analyzes dense anti-debugging traps (QPC timing delta, Toolhelp module scanning), dynamic console string XOR decryption,
  an 8-register 32-bit virtual machine interpreter, and rolling-key opcode permutation. Unmasks dead code junk instructions
  and unconditional obfuscated jumps, formulating joint algebraic solvers for the 26 independent character constraints
  and global rolling hash to achieve millisecond-level exact password recovery with 100% test validation.
board: "pe-reverse"
category: "05-crypto-unpack"
signals:
  - "Inside-the-Machine"
  - "自定义虚拟机"
  - "custom VM"
  - "rolling opcode"
  - "Opcode 置换"
  - "花指令跳转"
  - "死代码消除"
  - "代数约束求解"
  - "Rolling Hash"
  - "QPC 反调试"
  - "反调试绕过"
mcp_tools:
  - "kb_router"
  - "seep_r2_disasm"
keywords:
  - "custom VM"
  - "opcode permutation"
  - "dead code"
  - "algebraic solving"
  - "rolling hash"
  - "anti-debug"
difficulty: "advanced"
tags:
  - "custom-vm"
  - "anti-debug"
  - "algebraic-solving"
  - "pe-reverse"
  - "deobfuscation"
language: "zh-CN"
last_updated: "2026-10-16"
related_articles:
  - "pe-reverse/05-crypto-unpack/08-selfhealing-emulation-vmp-handler-extraction"
  - "pe-reverse/05-crypto-unpack/10-nested-vm-matryoshka-reverse-and-defeat"
  - "pe-reverse/05-crypto-unpack/12-vault-nested-helix-aegis-packer-maze-and-vm-defeat"
evidence: "reproduced"
---

# 极简自定义虚拟机（Inside-the-Machine）：反调试对抗、Opcode 滚动置换与双重约束求根

## 一、 架构总览：24KB 极简虚拟机与防线编织

`Inside-the-Machine` 是由知名出题人设计的紧凑型自研虚拟机样本。与动辄数兆字节的重型保护壳不同，该样本体积仅有 **24.5 KB**，但将**反调试时钟侦测、动态控制台文本混淆、Opcode 滚动解码置换以及带花指令的自定义字节码**高度压缩于一体：

```
                    [ 用户输入 Password (期望长度: 26) ]
                                    │
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │ 【Layer 1: 运行时环境防护与时钟检测】                   │
       │ • QPC (QueryPerformanceCounter) 耗时检测 (执行 > 300ms) │
       │ • 进程模块快照 (Toolhelp32) 走查探测 (scylla 等注入器) │
       │ • 动态异或字符串解密 sub_140001EF0 掩盖所有交互提示     │
       └────────────────────────────┬────────────────────────────┘
                                    │
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │ 【Layer 2: 1762 字节虚拟机字节码与滚动解码】            │
       │ • 字节码由 LCG (1103515245*x + 12345) 动态还原          │
       │ • Opcode 映射: v8 = byte_140005520[(v3 ^ raw) & 0xFF]   │
       │ • 滚动状态更新: v3 = v8 + 33*v3 + 7                     │
       └────────────────────────────┬────────────────────────────┘
                                    │
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │ 【Layer 3: 虚拟机核心解释器 (sub_1400014C0)】           │
       │ • 8 个 32 位通用虚拟寄存器 (r0 ~ r7)                    │
       │ • 包含 MOV/XOR/ADD/MUL/ROL/SHR/OR/JZ 等 14 种字节码算子 │
       │ • 混淆机制: 恒等跳转死代码陷阱 (如 r7+=0x16805eed; JZ) │
       └────────────────────────────┬────────────────────────────┘
                                    │
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │ 【Layer 4: 双重约束核验矩阵】                           │
       │ • 门禁 1: 长度硬性断言 len(input) == 26 (0x1a)          │
       │ • 门禁 2: 26 组单字节代数方程判定 (r0 |= r3)            │
       │ • 门禁 3: 全局 Rolling Hash 终检 (r4 == 0xee6ceb17)     │
       └─────────────────────────────────────────────────────────┘
```

---

## 二、 虚拟机指令集与动态解码规约

虚拟机核心位于 `sub_1400014C0`，解释器维护 8 个 32 位虚拟寄存器 `r0` ~ `r7`，返回值为 `r0`（若 `r0 == 0` 则验证通过）。

### 1. 动态滚动密钥置换（Rolling Opcode Decoding）
每一步取指时，Opcode 并不是明文编码，而是受到上下文历史操作的强约束：
```c
v8 = byte_140005520[(unsigned __int8)(v3 ^ bytecode[pc])];
v3 = v8 + 33 * v3 + 7;
```
`byte_140005520` 是一个 256 字节的非线性 S-Box 置换表。

### 2. 虚拟操作码全景映射表

| Opcode | 助记符 | 长度 | 操作数与语义 |
| :---: | :--- | :---: | :--- |
| `0` | `RET` | 1 B | `return r0;` (退出解释器) |
| `1` | `MOV_IMM` | 6 B | `r[dst] = imm32;` |
| `2` | `XOR_IMM` | 6 B | `r[dst] ^= imm32;` |
| `3` | `ADD_IMM` | 6 B | `r[dst] += imm32;` |
| `4` | `MUL_IMM` | 6 B | `r[dst] *= imm32;` |
| `5` | `ROL_IMM` | 3 B | `r[dst] = ROL32(r[dst], imm8 & 0x1F);` |
| `6` | `LOAD_INP`| 3 B | `r[dst] = input[imm8];` (载入单个输入字符) |
| `7` | `LOAD_LEN`| 2 B | `r[dst] = len(input);` (载入输入总长度) |
| `8` | `XOR_REG` | 3 B | `r[dst] ^= r[src];` |
| `9` | `ADD_REG` | 3 B | `r[dst] += r[src];` |
| `10`| `SHR_IMM` | 3 B | `r[dst] >>= imm8;` |
| `11`| `OR_REG`  | 3 B | `r[dst] \|= r[src];` |
| `12`| `MOV_REG` | 3 B | `r[dst] = r[src];` |
| `13`| `JZ`      | 3 B | `if (r[src] == 0) pc += (int8)rel + 3;` |

---

## 三、 死代码花指令识别与虚拟控制流消除

在反汇编虚拟字节码时，我们发现数个看似复杂却从未被执行的代码块：
```text
[0171] r7 = 0xe97fa113
[0177] r7 += 0x16805eed
[017d] if r7 == 0 goto 0x1c7 (regs[r7]=0)
... (0x180 ~ 0x1c6: 包含虚假计算的死代码)
[01c7] r1 = input[6]
```
`0xe97fa113 + 0x16805eed = 0x100000000 \equiv 0 \pmod{2^{32}}`。
`r7` 经过常数加法后必定为 0，导致紧随其后的 `if r7 == 0` 是一个**无条件跳转（Opaque Predicate Jump）**，其跳过的 71 字节全部为干扰静态分析的垃圾花指令。

在编写反汇编与仿真分析工具时，必须动态跟踪寄存器状态并严格遵循跳转分支，避免因线性遍历未执行区域而污染 `v3` 滚动密钥。

---

## 四、 约束求解与 Password 还原

在消除死代码后，整个虚拟程序的语义被清晰还原为对 26 个字符的独立约束与 1 个全局滚动哈希约束：

1. **长度断言**：`len(input) == 26`（对应 `[06bb] r6 = len(input); r6 ^= 0x1a; r0 |= r6`）；
2. **26 组单字符代数约束**：每个字符经过独一无二的代数变换（乘法、加法、异或、循环移位），随后与目标常数异或放入 `r3`，并执行 `r0 |= r3`；
3. **全局 Rolling Hash**：
   $$\text{hash}_0 = \text{0x591731de}$$
   $$\text{hash}_{i+1} = (\text{hash}_i \times \text{0x2a19363f} + \text{input}[i]) \pmod{2^{32}}$$
   最终断言：$\text{hash}_{26} == \text{0xee6ceb17}$。

### 毫秒级求根
由于 26 个字符各自独立断言，单字符仅有 256 种可能取值，利用单循环直接求根，并在最后代入 Rolling Hash 进行双重校验：

```python
# 求解示例片段
for idx in range(26):
    for b in range(256):
        if eval_constraint(idx, b):
            solved.append(b)
            break
```

**解出明文**：
$$\mathbf{V1rtu4lM4ch1n3\_1ns4n3\_2026}$$

**Rolling Hash 校验**：
$$\text{0xee6ceb17} \oplus \text{0xee6ceb17} = \mathbf{0x00000000} \quad (\text{100\% 自洽吻合})$$

---

## 五、 真实环境闭环验证

```bash
printf "V1rtu4lM4ch1n3_1ns4n3_2026\n" | wine crackme.exe
echo "Exit code: $?"
```
```text
=================================================
   VM Crackme - custom virtual machine
   Goal: find the password.
=================================================

Enter password: 
[+] Correct! The machine accepted your password.
Exit code: 0
```

---

## 六、 纵深防御加固规范建议

1. **废弃单字符独立判决模型**：
   * 即使采用了字节码虚拟化，但如果每个字符的校验结果只是独立通过 `r0 |= r3` 汇聚，其密码学安全性几乎等同于明文单字节比对，可以被极其简单的穷举攻击击溃；
   * 必须采用**分组密码网络（Feistel 或 SPN 结构）**，使整个密码块在第一轮后发生全面扩散（Diffusion）。
2. **深化虚拟机状态互锁**：
   * 不应仅在最后计算一个只读的 Rolling Hash，而应将上一轮的计算结果作为下一轮虚拟指令执行的密钥或指针偏移行程，使单个字符的微小篡改直接导致后续 VM 解码发生异常崩溃。
