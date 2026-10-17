---
id: "pe-reverse/05-crypto-unpack/10-nested-vm-matryoshka-reverse-and-defeat"
title: "多层嵌套虚拟机（Matryoshka-VM）逆向与破译方法论：从分发层逐级剥离到最内层代数约束求解"
title_en: "Nested Virtual Machine (Matryoshka-VM) Reversing and Defeat: Layer-by-Layer Peeling to Inner Algebraic Constraint Solving"
summary: >
  针对多层嵌套虚拟机（5 层俄罗斯套娃架构）的端到端逆向分析全流程与破译方法论。
  详细记录外层 VM 密钥流解密（LCG / Xorshift）、SIMD/SSE 矢量解包还原、虚拟指令集语义提取，
  以及最内层断言虚拟机的单字节代数方程逆向还原。总结规避全空间蛮力搜索陷阱的逆向思维模型，
  实现 24 字节 Flag 的毫秒级精确代数求解，并给出 Linux Headless 与 Wine 双重闭环验证。
summary_en: >
  End-to-end reverse engineering methodology and defeat workflow for multi-layer nested virtual machines
  (5-layer Russian doll architecture). Documents key-stream decryptions (LCG / Xorshift), SIMD/SSE vector
  unpacking, virtual instruction semantics extraction, and algebraic constraint solving for the innermost
  assertion VM. Avoids brute-force search traps and achieves millisecond-level exact recovery of the 24-byte
  password flag with dual validation under Linux headless emulation and Wine.
board: "pe-reverse"
category: "05-crypto-unpack"
signals:
  - "Matryoshka-VM"
  - "嵌套虚拟机"
  - "nested VM"
  - "套娃 VM"
  - "多层 VM"
  - "VM 字节码解密"
  - "LCG 密钥流"
  - "Xorshift"
  - "SIMD SSE 展开"
  - "单字节断言"
  - "约束求解"
  - "无真机逆向"
mcp_tools:
  - "kb_router"
  - "seep_r2_disasm"
keywords:
  - "nested VM"
  - "virtualization"
  - "bytecode decryption"
  - "algebraic constraint"
  - "headless emulation"
  - "Matryoshka"
  - "custom VM"
difficulty: "advanced"
tags:
  - "custom-vm"
  - "nested-vm"
  - "algebraic-solving"
  - "pe-reverse"
  - "emulation"
language: "zh-CN"
last_updated: "2026-10-16"
related_articles:
  - "pe-reverse/05-crypto-unpack/08-selfhealing-emulation-vmp-handler-extraction"
  - "pe-reverse/05-crypto-unpack/09-runtime-vm-detection-generic"
evidence: "reproduced"
---

# 多层嵌套虚拟机（Matryoshka-VM）逆向与破译方法论

## 一、 架构总览：五层嵌套虚拟机拓扑

`Matryoshka-VM` 属于典型的自研多层嵌套代码虚拟化（Nested Custom VM）保护。其外层以“嵌套套娃”形式组织，只有当所有层级全部判定通过时，最终状态汇聚点才保持为 0，并放行合法性验证。

```
[用户输入 Password] (期望长度: 24)
         │
         ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ 【VM-1: 外层状态机】                                         │
 │ - 字节码长度: 1720 字节 (解密自 unk_14000CF40)              │
 │ - 解密机制: 线性同余发生器 (LCG) 伪随机密钥流               │
 │ - 分发方式: switch-case + 查表置换 byte_14000C220            │
 │ - 核心分支: Case 12 调用 VM-2                               │
 └──────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ 【VM-2: 寄存器机】                                           │
 │ - 字节码长度: 974 字节 (解密自 unk_14000CB60)               │
 │ - 解密机制: 32 位 Xorshift 伪随机序列                       │
 │ - 核心分支: Case 9 触发 SIMD 解密并调用 VM-3                 │
 └──────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ 【VM-3: 栈式虚拟机】                                         │
 │ - 字节码长度: 608 字节 (解密自 unk_14000C8E0)               │
 │ - 解密机制: 128 位 SSE 矢量计算与交错解包 (_mm_unpack)      │
 │ - 核心分支: Case 9 触发二次 SSE 解密并调用 VM-4              │
 └──────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ 【VM-4: 寄存器混淆机】                                       │
 │ - 字节码长度: 1075 字节 (解密自 unk_14000C440)              │
 │ - 解密机制: SSE 混淆打乱与 S-box 变换                       │
 │ - 核心分支: Case 9 触发解密并调用 VM-5                       │
 └──────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ 【VM-5: 核心核验虚拟机】                                     │
 │ - 字节码长度: 269 字节 (解密自 byte_14000C320 / C207)       │
 │ - 解密机制: 仿射加密轮换变换                                │
 │ - 核心逻辑: 长度断言 (Op 0x88) + 24 组单字节代数断言 (Op 0x66) │
 └─────────────────────────────────────────────────────────────┘
```

---

## 二、 逆向分层分析与逐层剥离

### 1. VM-1：外层调度与 LCG 解密
- **数据源**：`unk_14000CF40`，长度 1720 字节。
- **解密算法**：标准 LCG 递推公式：
  $$\text{seed}_{n+1} = (1103515245 \times \text{seed}_n + 12345) \pmod{2^{32}}$$
  $$\text{bytecode}[i] = \text{raw}[i] \oplus ((\text{seed} \gg 16) \ \& \ 0xFF)$$
- **分发机制**：通过查表 `byte_14000C220` 解码真实 Handler，其中 `Case 12` 为启动 VM-2 的网关。

### 2. VM-2：32-bit Xorshift 解密
- **数据源**：`unk_14000CB60`，长度 974 字节。
- **解密算法**：Xorshift 伪随机序列：
  $$\text{val} \leftarrow \text{val} \oplus (\text{val} \ll 13)$$
  $$\text{val} \leftarrow \text{val} \oplus (\text{val} \gg 17)$$
  $$\text{val} \leftarrow \text{val} \oplus (\text{val} \ll 5)$$
  $$\text{bytecode}[i] = \text{raw}[i] \oplus (\text{val} \ \& \ 0xFF)$$
- **分发机制**：`Case 9` 进入 SIMD 向量计算，还原下一层 VM 字节码。

### 3. VM-3 & VM-4：SIMD/SSE 矢量展开
- 采用 `_mm_add_epi32`、`_mm_unpacklo_epi16`、`_mm_packus_epi16` 对静态高熵常量数组进行矢量展开与反交错，动态释放 608 字节与 1075 字节的代码页。
- 关键特征：**解密过程不依赖用户输入**，输入仅在执行特定 Opcode 时由只读寄存器传导。这说明外层所有解密均可**完全离线静态还原**。

### 4. VM-5：核心核验虚拟机的指令集还原
解密自 `byte_14000C320` 与 `byte_14000C207`，长度 269 字节。逆向提取出的 VM-5 虚拟指令集（Opcode Map）如下：

| Opcode (Hex) | 助记符 | 操作数 | 语义 |
| :---: | :--- | :---: | :--- |
| `0x11` | `LOAD_INP` | `idx (1B)` | `ACC = input[idx]` (载入输入字符) |
| `0x22` | `XOR_IMM` | `val (1B)` | `ACC = ACC ^ val` (按位异或常量) |
| `0x33` | `ADD_IMM` | `val (1B)` | `ACC = (ACC + val) & 0xFF` (加常量) |
| `0x44` | `ROL_IMM` | `val (1B)` | `ACC = ROL8(ACC, val)` (8 位循环左移) |
| `0x55` | `MUL_IMM` | `val (1B)` | `ACC = (ACC * val) & 0xFF` (模乘常量) |
| `0x66` | `ASSERT_EQ`| `val (1B)` | `if (ACC != val) ERR \|= 1` (校验断言) |
| `0x88` | `CHECK_LEN`| `val (1B)` | `if (len(input) != val) ERR \|= 2` (长度门禁) |
| `0x99` | `RESET_ACC`| 无 | `ACC = 0` (累加器清零) |
| `0xFF` | `HALT` | 无 | 退出虚拟机主循环 |

---

## 三、 漏洞成因分析：从蛮力陷阱到精确代数求解

### 1. 规避蛮力搜索陷阱
在初次分析 VM 外层时，容易被外层 VM 中的复合校验公式误导（例如试图对 32 位全空间暴力跑 `cksum(v2, 0xffffffff) == 0x16607cc9`）。由于其包含多轮复杂变换，单线程遍历 $2^{32}$ 空间需要数十分钟且极易超时。

### 2. 核心脆弱点：单字节独立性（Lack of Diffusion）
深入逆向最内层 VM-5 发现，其验证逻辑存在严重的**无雪崩效应（Lack of Avalanche Effect）**：
- 输入被硬性要求为 24 字节（`0x88 0x18`）；
- 每个字符 `input[0]` 到 `input[23]` 是**完全独立**计算并断言的；
- 没有任何跨字节的信息混合或状态传递。

因此，原本看似复杂的 $256^{24}$ 搜索空间，直接塌缩为 24 个独立的单字节代数方程：
$$\forall i \in [0, 23], \quad f_i(\text{input}[i]) == K_i \pmod{256}$$

每个方程的解空间仅为 $256$，全局求解总复杂度仅为 $24 \times 256 = 6144$ 次计算，耗时不超过 1 毫秒！

---

## 四、 24 字节单约束全量推导表

通过解析 VM-5 字节码，还原出的 24 组约束及精确解如下：

| 索引 | 字节码计算过程 | 目标常量 | 解出明文 (Hex) | ASCII |
| :---: | :--- | :---: | :---: | :---: |
| `0` | `((((c * 0xd3) * 0xb5) + 0xc0) + 0x86) & 0xFF` | `0x3f` | `0x57` | `'W'` |
| `1` | `((((c * 0xad) * 0x9f) * 0xbf) ^ 0x87) & 0xFF` | `0x5b` | `0x4c` | `'L'` |
| `2` | `(ROL8(((c + 0xfd) ^ 0x14), 7) ^ 0x8f) & 0xFF` | `0x9f` | `0x37` | `'7'` |
| `3` | `ROL8((((c * 0xc5) ^ 0x8e) + 0x37), 3) & 0xFF` | `0x41` | `0x73` | `'s'` |
| `4` | `((ROL8(c, 4) * 0x9f) * 0xf5) & 0xFF` | `0x91` | `0x33` | `'3'` |
| `5` | `(ROL8(c, 7) * 0xf5) ^ 0x17` | `0x1d` | `0x45` | `'E'` |
| `6` | `((ROL8(c, 2) * 0xfb) + 0x70) ^ 0x93` | `0x54` | `0x55` | `'U'` |
| `7` | `ROL8((ROL8(c + 0x8a, 3) * 0x07), 2)` | `0x4b` | `0x39` | `'9'` |
| `8` | `ROL8(ROL8(ROL8(c + 0xd7, 1), 6), 7)` | `0x10` | `0x69` | `'i'` |
| `9` | `((ROL8(c, 1) * 0x7f) + 0x12 + 0x04) & 0xFF` | `0xd4` | `0x21` | `'!'` |
| `10` | `ROL8(c ^ 0xd5 ^ 0xca, 5)` | `0xaf` | `0x62` | `'b'` |
| `11` | `(((c ^ 0x16) * 0xc3) * 0xbd) & 0xFF` | `0xe8` | `0x4e` | `'N'` |
| `12` | `ROL8(ROL8(c, 5) ^ 0x49, 4)` | `0xd6` | `0x21` | `'!'` |
| `13` | `((c * 0x9b) ^ 0x84 ^ 0x09) & 0xFF` | `0xcb` | `0x32` | `'2'` |
| `14` | `(ROL8(ROL8(c ^ 0x7e, 6), 2) * 0x33) & 0xFF` | `0x58` | `0x36` | `'6'` |
| `15` | `(c ^ 0x96) + 0x8a + 0xb2` | `0xde` | `0x34` | `'4'` |
| `16` | `(((c * 0x7b) ^ 0x84) * 0x3d) & 0xFF` | `0xa3` | `0x21` | `'!'` |
| `17` | `ROL8(((c ^ 0x53) + 0x4b) ^ 0x20, 1)` | `0x23` | `0x35` | `'5'` |
| `18` | `(((c ^ 0x7f) + 0xe5) ^ 0x03 ^ 0x5e) & 0xFF` | `0xae` | `0x71` | `'q'` |
| `19` | `(c ^ 0x08) + 0x5a + 0x01` | `0xbb` | `0x68` | `'h'` |
| `20` | `((((c * 0x53) * 0x35) * 0x85) ^ 0x18) & 0xFF` | `0x30` | `0x78` | `'x'` |
| `21` | `(ROL8(ROL8(c, 7) * 0xf5, 3) ^ 0x15) & 0xFF` | `0xce` | `0x5f` | `'_'` |
| `22` | `(((c * 0x8b) * 0x01) * 0xe9) & 0xFF` | `0x19` | `0x33` | `'3'` |
| `23` | `ROL8(ROL8(ROL8(c, 3), 6), 3)` | `0x17` | `0x71` | `'q'` |

**最终破译明文 Flag**：
$$\mathbf{WL7s3EU9i!bN!264!5qhx\_3q}$$

---

## 五、 双重环境验证与落地

### 1. Wine CLI 实测回显
```bash
printf "WL7s3EU9i!bN!264!5qhx_3q\n" | wine crackme.exe
```
```text
====================================================
   Crackme - five nested virtual machines
   Goal: find the password.
====================================================

Enter password: 
[+] Correct! All five virtual machines agree. You found the password.
```

### 2. Linux Headless (Unicorn 模拟器) 回显
通过自主编写的 `pe_loader_v2.py` 无真机模拟执行：
```text
=== Headless Emulation Output ===
====================================================
   Crackme - five nested virtual machines
   Goal: find the password.
====================================================

[+] Correct! All five virtual machines agree. You found the password.
```

---

## 六、 自动化求解脚本实现

求解脚本已集成并归档：
`matryoshka_vm_solver.py`（见同目录），核心解析代码如下：

```python
def solve_flag(binary_path):
    # 1. PE 节区映射与静态解密 byte_14000C320 / C207
    ...
    # 2. 24 个单字节方程逐个枚举 (0..255)
    solved = []
    for idx in range(24):
        for b in range(256):
            if evaluate_constraint(idx, b):
                solved.append(b)
                break
    return bytes(solved).decode('ascii')
```
运行即可实现 100% 确定性、零依赖的一键破译。
