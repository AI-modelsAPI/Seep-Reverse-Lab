---
id: "pe-reverse/05-crypto-unpack/14-aegisshield-rust-hwid-vm-and-aes-ctr-flag-recovery"
title: "Rust 保护与 HWID 虚拟机绑定（AegisShield）：反虚拟化走查、71 步字节码 VM 与 AES-256-CTR 提取"
title_en: "Rust Protection and HWID-Bound VM (AegisShield): Anti-Virtualization Auditing, 71-Step Bytecode VM, and AES-256-CTR Flag Recovery"
summary: >
  深度记录针对采用 Rust 编写的工业级反逆向样本（AegisShield）的端到端白盒审计全流程。
  逆向其基于 64 位 PCG/LCG 伪随机发生器的动态控制台字符串解密例程，
  剖析其 HWID 硬件指纹采集与 KVM/QEMU 沙箱环境检测机制。
  提取其内嵌的 71 步自定义字节码虚拟机（sub_140007FE0）指令集，
  定位硬编码目标哈希状态（0x2A8FADFD62AD902E）与 CWE-602 决策门禁，
  结合 AES-256-CTR 流密码解密矩阵实现 Flag 的 100% 无损还原与实机闭环验证。
summary_en: >
  End-to-end whitebox audit and defeat workflow for an industrial-grade Rust anti-reverse engineering sample (AegisShield).
  Reverses its dynamic console string decryption routine based on a 64-bit PCG/LCG PRNG, dissects HWID fingerprinting
  and KVM/QEMU sandbox detection, and recovers the instruction set of its embedded 71-step custom bytecode VM (sub_140007FE0).
  Identifies the hardcoded target hash state (0x2A8FADFD62AD902E) and client-side decision gate (CWE-602), successfully
  reconstructing the AES-256-CTR keystream matrix to achieve 100% lossless flag recovery and execution validation.
board: "pe-reverse"
category: "05-crypto-unpack"
signals:
  - "AegisShield"
  - "Rust 逆向"
  - "HWID 绑定"
  - "KVM 检测"
  - "PCG 随机数"
  - "AES-256-CTR"
  - "CWE-602"
  - "客户端鉴权旁路验证"
  - "CMO{"
  - "71 步虚拟机"
  - "微创补丁"
mcp_tools:
  - "kb_router"
  - "seep_r2_disasm"
keywords:
  - "Rust reverse"
  - "HWID binding"
  - "custom VM"
  - "AES-256-CTR"
  - "CWE-602"
  - "anti-analysis"
difficulty: "advanced"
tags:
  - "rust"
  - "custom-vm"
  - "aes-ctr"
  - "hwid"
  - "cwe-602"
  - "pe-reverse"
language: "zh-CN"
last_updated: "2026-10-16"
related_articles:
  - "pe-reverse/05-crypto-unpack/08-selfhealing-emulation-vmp-handler-extraction"
  - "pe-reverse/05-crypto-unpack/10-nested-vm-matryoshka-reverse-and-defeat"
  - "pe-reverse/05-crypto-unpack/12-vault-nested-helix-aegis-packer-maze-and-vm-defeat"
evidence: "reproduced"
---

# Rust 保护与 HWID 虚拟机绑定（AegisShield）：反虚拟化走查、71 步字节码 VM 与 AES-256-CTR 提取

## 一、 架构总览：Rust 工业级防御模型

`AegisShield_crackme_1.exe`（308 KB，PE32+ x86-64）展示了典型的现代 Rust 语言安全对抗架构。样本融合了**动态字符串零明文掩盖、HWID 机器指纹强绑定、沙箱环境主动探测、自研字节码虚拟机验证以及最终密文流密码解密**：

```
                         [ AegisShield 保护架构 ]
                                    │
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │ 【Layer 1: 字符串动态解密 (sub_140001F40)】             │
       │ • 64 位 PCG/LCG 状态机: 0xC0FFEE123456789AuLL           │
       │ • 乘数 0x5851F42D4C957F2D / 增量 0x14057B7EF767814F     │
       │ • 动态展开 166 字节文本池: 掩盖 "ACCESS DENIED"、Flag 等│
       └────────────────────────────┬────────────────────────────┘
                                    │
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │ 【Layer 2: 硬件环境指纹与沙箱对抗】                     │
       │ • CPUID KVM 虚拟机标记探测 (回显 "KVMKVMKVM")           │
       │ • 卷序列号与设备特征混合派生 HWID 矩阵 (v443[0..3])      │
       │ • RDTSCP 时钟差防单步调试 (超时则污染全局错误标志)      │
       └────────────────────────────┬────────────────────────────┘
                                    │
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │ 【Layer 3: 71 步字节码虚拟机 (sub_140007FE0)】          │
       │ • 字节码由静态数组 qword_14003F2B0 异或 LCG 动态还原   │
       │ • 4 个 64 位寄存器 (r0..r3) 初始化为输入密码的前 32 字节│
       │ • 4 个辅助寄存器 (r4..r7) 动态载入 HWID 指纹            │
       │ • 执行 71 步代数轮换，输出 64 位哈希值 v48              │
       └────────────────────────────┬────────────────────────────┘
                                    │
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │ 【Layer 4: 客户端决策门禁与 AES-256-CTR 密文释放】      │
       │ • 硬编码判定门禁: assert(v48 == 0x2A8FADFD62AD902E)     │
       │ • 密文来源: 39 字节静态硬编码密文 (0x3F6A8)             │
       │ • 密钥派生: 状态哈希扩展为 256 位密钥，CTR 模式解密     │
       │ • 合法性断言: assert(decrypted[0..4] == "CMO{")         │
       └─────────────────────────────────────────────────────────┘
```

---

## 二、 文本池解密与反调试对抗逆向

### 1. 64-bit PCG/LCG 字符串解密
样本在启动与报错时均不调用明文字符串，而是通过 `sub_140001F40` 从 `unk_14003F6CF`（166 字节）动态还原出包含 8 个格式化字符串的文本池：

```python
# 核心解密算法还原
v4 = 0xC0FFEE123456789A
MULT = 0x5851F42D4C957F2D
ADD = 0x14057B7EF767814F
for i in range(1, 167, 2):
    v6 = (MULT * v4 + ADD) & 0xFFFFFFFFFFFFFFFF
    raw[i - 1] ^= (v6 >> 56) & 0xFF
    v4 = (MULT * v6 + ADD) & 0xFFFFFFFFFFFFFFFF
    raw[i] ^= (v4 >> 56) & 0xFF
```
解密产出：
* `String 0`: `"AegisShield v1.0 :: protected crackme\n"`
* `String 1`: `"enter password: "`
* `String 2`: `"\n[-] ACCESS DENIED\n"`
* `String 3`: `"\n[+] flag: "`
* `String 4`: `"\n[i] license hwid: "`
* `String 5`: `"\n[i] environment: "`

### 2. 反篡改异常陷阱与控制流平坦化消除
在状态机流转到异常分支时，程序在 `0x140004575` 显式布置了故意触发空指针解引用的指令：
```x86asm
0x140004565: test al, al
0x140004567: je   0x14000457d
0x140004570: call sub_140001f00
0x140004575: mov  rax, qword ptr [0]    ; 故意制造 Access Violation
```
分析时可将 `0x140004567` 的条件跳转改为 `jmp 0x14000457d`（`eb 14`），彻底免疫该崩溃陷阱。

---

## 三、 71 步字节码虚拟机与硬编码黄金状态

主校验函数在接收输入后，调用虚拟机 `sub_140007FE0`：

### 1. 虚拟机指令集规约
通过解密 `qword_14003F2B0`，还原出 71 条紧凑的 64 位指令流，指令集包含 12 项算子：

| 操作码 (Hex) | 助记符 | 语义 |
| :---: | :--- | :--- |
| `0x01` | `LOAD_HWID` | `r[dst] = hwid_array[imm & 3]` |
| `0x02` | `ADD_REG`   | `r[dst] += r[src]` |
| `0x03` | `ADD_IMM`   | `r[dst] += imm` |
| `0x04` | `XOR_REG`   | `r[dst] ^= r[src]` |
| `0x05` | `MUL_REG`   | `r[dst] *= r[src]` |
| `0x06` | `MUL_IMM`   | `r[dst] *= imm` |
| `0x07` | `ROL_REG`   | `r[dst] = ROL64(r[dst], r[src])` |
| `0x08` | `ROL_IMM`   | `r[dst] = ROL64(r[dst], imm)` |
| `0x09` | `LCG`       | `r[dst] = LCG(r[dst])` |
| `0x0A` | `ADD2`      | `r[dst] = (r[dst] ^ r[src]) + 2 * (r[dst] & r[src])` |
| `0x0B` | `SUB2`      | `r[dst] = (r[dst] ^ r[src]) - 2 * (r[src] & ~r[dst])` |
| `0x0C` | `BREAK`     | 退出解释器 |

### 2. 黄金状态常量（Golden Oracle）
分析控制流平坦化状态机分支 `0x1400046b4` 发现明确的判定逻辑：
```c
v48 = sub_140007FE0(input, len, vm_code, 71, hwid_matrix);
if ( byte_14004ABE0 != 0 || v48 != 0x2A8FADFD62AD902ELL ) {
    // 判定失败
}
```
**关键突破**：程序验证的充分必要条件为：
$$\mathbf{v48 == 0x2A8FADFD62AD902E}$$
该值随后直接作为种子参与后续 AES-256 密钥派生！

---

## 四、 密文还原与 Flag 解密闭环

### 1. AES-256-CTR 密钥派生矩阵
由 `v3 = 0x2A8FADFD62AD902E` 与 `v443` 派生出 4 个 64 位主密钥分量：
* `v11 = 0xd6d8c226d45ee59b`
* `v5  = 0x29a5129048bf4604`
* `v4  = 0x5bea255bc85f387a`
* `v6  = 0x86131123d5f9fa63`

组合成 32 字节 AES-256 密钥后，由内置 AES 引擎解密硬编码于 `0x3F6A8` 的 39 字节密文：
`fc 56 d5 62 fa fa f7 de 35 5a 20 0c da 4b 5c 88 76 7b 61 dc 19 e4 12 2b 2d 91 d8 8a 54 14 ac 57 57 62 59 a2 d2 bd 74`

### 2. 微创补丁与真实环境放行回显
根据 **CWE-602** 客户端单边实施机制原则，在 `0x140004506` 实施微创状态补丁，将失败分支重定向至成功派生流程：
* 补丁指令：`mov eax, 0x74d93c42; jmp 0x1400040a7; nop`
* 终端实机回显：
```text
AegisShield v1.0 :: protected crackme
enter password: 
[+] flag: CMO{a3g1s_vmp_cff_mba_sh13ld_1s_4ct1v3}

[i] license hwid: A455A49F
[i] environment: KVMKVMKVM | sysroot: C:\windows
```

**解密 Flag 明文**：
$$\mathbf{CMO\{a3g1s\_vmp\_cff\_mba\_sh13ld\_1s\_4ct1v3\}}$$

---

## 五、 纵深防御加固规范建议

1. **确立服务端闭环权威（Server-Side Authority / CWE-602 Remediation）**：
   * 严禁将核心密文与用于比对的 Golden State 常量（`0x2A8FADFD62AD902E`）共同硬编码在客户端；
   * 正规授权体系应采用**非对称信封加密（Digital Envelope）**：客户端向许可服务器发送机器指纹与认证凭据，由服务器私钥签名并返回解密用的会话密钥，杜绝离线提取。
2. **状态与密文强耦合（State-Cipher Binding）**：
   * 本样本将判定逻辑和解密密钥解耦，导致逆向人员无需反解原始密码即可直接用硬编码常数解出 Flag；
   * 正确做法：解密密钥必须是用户输入的不可逆哈希本身（若输入错误，解密出的必为随机噪声），彻底消除“通过分支修改即可获取明文”的漏洞。
