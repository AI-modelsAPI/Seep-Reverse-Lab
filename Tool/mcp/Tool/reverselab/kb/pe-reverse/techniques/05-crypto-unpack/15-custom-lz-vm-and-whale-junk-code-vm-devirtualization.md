---
id: "pe-reverse/05-crypto-unpack/15-custom-lz-vm-and-whale-junk-code-vm-devirtualization"
title: "定制 LZ 壳与 38 指令 VM / 99.2% 花指令湮灭的 Whale 虚拟机：双样本端到端反虚拟化"
title_en: "Custom LZ Packer with 38-Opcode VM and Whale VM Defeated via 99.2% Junk-Code Annihilation: Dual-Sample End-to-End Devirtualization"
summary: >
  完整记录两个高度定制化 Windows 虚拟化保护样本的端到端白盒审计：
  (A) crackme.lucky.exe —— 自定义四指令 LZ 变体压缩壳（CRC32 自校验）+ 五变量流密码 SMC 自修改节
  + 五路反调试 + 38 操作码字节码虚拟机，其指令流采用「位置相关双因子流密码」
  plain[idx]=(c^((7*idx+seed-0x5B)&0xFF))^(D100>>(8*(idx&3))) 逐帧加密；
  (B) CrackMe0.exe（Whale）—— 256 项重定位分发表 + 8 类花指令体系（压缩比 99.2%，5600 条→43 条真语义）
  + 128 虚拟寄存器 VM，其立即数采用「地址自基准」加密 plain=raw^((K*imm_addr)^C)，
  并内嵌 PEB/NtGlobalFlag/NtQueryInformationProcess 三重反调试。
  沉淀了「立即数位置 = 解密基准」这一通用判据，以及运行时 VIP 轨迹与静态反编译序列的交叉验证方法。
summary_en: >
  End-to-end whitebox audit of two highly customized Windows virtualization-protection samples.
  (A) crackme.lucky.exe: a custom 4-instruction LZ-variant packer (CRC32 self-verified) guarding a
  5-variable stream-cipher SMC section plus 5-way anti-debug and a 38-opcode bytecode VM whose instruction
  stream is position-dependent double-factor encrypted: plain[idx]=(c^((7*idx+seed-0x5B)&0xFF))^(D100>>(8*(idx&3))).
  (B) CrackMe0.exe (Whale): a 256-entry relocated dispatch table guarded by an 8-class junk-code system
  (99.2% noise reduction, 5600 -> 43 real semantics) plus a 128-virtual-register VM whose immediates use
  address-self-based encryption plain=raw^((K*imm_addr)^C), with triple anti-debug
  (PEB / NtGlobalFlag / NtQueryInformationProcess).
  Establishes the general criterion "immediate position == decryption base" and a cross-validation method
  between runtime VIP traces and static disassembly sequences.
board: "pe-reverse"
category: "05-crypto-unpack"
signals:
  - "定制 LZ 压缩壳"
  - "CRC32 自校验"
  - "SMC 自修改节"
  - "五路反调试"
  - "38 指令虚拟机"
  - "位置相关流密码"
  - "花指令"
  - "junk code"
  - "256 项重定位分发表"
  - "Whale VM"
  - "地址自基准立即数加密"
  - "NtQueryInformationProcess"
  - "NtGlobalFlag"
  - "BSD 型不透明谓词"
  - "99.2% 压缩比"
  - "运行时 VIP 轨迹交叉验证"
mcp_tools:
  - "kb_router"
  - "seep_r2_disasm"
  - "seep_r2_decompile"
  - "seep_r2_functions"
keywords:
  - "custom LZ packer"
  - "SMC section"
  - "junk code annihilation"
  - "bytecode VM devirtualization"
  - "address-self-based immediate encryption"
  - "runtime VIP cross-validation"
  - "anti-debug PEB NtGlobalFlag"
difficulty: "advanced"
tags:
  - "custom-vm"
  - "packer"
  - "junk-code"
  - "anti-debug"
  - "smc"
  - "pe-reverse"
language: "zh-CN"
last_updated: "2026-10-19"
related_articles:
  - "pe-reverse/05-crypto-unpack/08-selfhealing-emulation-vmp-handler-extraction"
  - "pe-reverse/05-crypto-unpack/09-runtime-vm-detection-generic"
  - "pe-reverse/05-crypto-unpack/10-nested-vm-matryoshka-reverse-and-defeat"
  - "pe-reverse/05-crypto-unpack/13-inside-the-machine-custom-vm-and-rolling-hash-defeat"
  - "pe-reverse/05-crypto-unpack/14-aegisshield-rust-hwid-vm-and-aes-ctr-flag-recovery"
evidence: "reproduced"
---

# 定制 LZ 壳与 38 指令 VM / 99.2% 花指令湮灭的 Whale 虚拟机：双样本端到端反虚拟化

## 一、 双样本架构总览

两个样本代表虚拟化保护的两种正交设计路线：

```
【样本 A: crackme.lucky.exe (3.6 MB, PE32+ x86-64, Mingw-w64)】
    外壳对抗                                            虚拟机内核
  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
  │ .lucky0      │──▶│ .lucky1      │──▶│ 内层 PE      │──▶│ 38 指令 VM   │
  │ 定制 LZ 变体 │   │ 五路反调试   │   │ .smc 自修改  │   │ 8 帧流式解密 │
  │ CRC32 校验   │   │ 动态 API 解析│   │ 五变量流密码 │   │ 位置相关密钥 │
  └──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘

【样本 B: CrackMe0.exe (5.3 MB, PE32+ x86-64, MSVC, .whale 节 5.2 MB)】
                    分发层                                        混淆层
  ┌──────────────────┐   ┌──────────────────┐   ┌────────────────────┐
  │ 256 项重定位表    │──▶│ 主分发器          │──▶│ 8 类花指令体系      │
  │ dec=enc^((op*K)^C)│   │ 纯寄存器跳转      │   │ 5600 条 → 43 条     │
  └──────────────────┘   └──────────────────┘   └────────────────────┘
                                                          │
                     ┌────────────────────────────────────┘
                     ▼
  ┌──────────────────────────────────────────────────────────┐
  │ 128 虚拟寄存器 VM + 地址自基准立即数加密 + 三重反调试      │
  └──────────────────────────────────────────────────────────┘
```

### 1.1 两样本的核心差异

| 维度 | lucky | Whale |
|---|---|---|
| 壳层 | 定制 LZ 变体（四指令） | 无壳，`.whale` 节直接承载 VM |
| 分发方式 | jump table @ `.rdata` + switch | 256 项加密表 + `imul`/`xor` 现场解密 |
| 指令加密 | 位置相关双因子流密码 | 地址自基准单因子加密 |
| 混淆 | 无 | **8 类花指令，99.2% 噪声** |
| 反调试 | 五路（PEB/NtGlobalFlag/Heap/CRDP/NtQIP） | 三重（PEB/NtGlobalFlag/NtQIP） |
| 虚拟寄存器 | 16 × u32 | 128 × u64 |
| 输入校验 | **无**（纯展示型） | 有（但被假 API 调用挡住） |

---

## 二、 样本 A：定制 LZ 壳的四层剥离

### 2.1 Layer 1 — 自定义 LZ 变体解压

`.lucky1` 节头部为 32 字节结构：

```
偏移 0x00: magic      = 0x314B434C ("LCK1")
偏移 0x04: unpacked   = 203776
偏移 0x08: reserved
偏移 0x0C: checksum   = 0xF3F7B086   (输出 CRC32)
偏移 0x10: cmd_offset = 32
偏移 0x14: cmd_size   = 722183
偏移 0x18: dat_offset = 722215
偏移 0x1C: dat_size   = 843953
```

解压器只使用四条虚拟指令（非标准 LZ）：

| 指令 | 语义 |
|---|---|
| `0xA1` | 输出 1 字节：`out[v8] = data[v11++] ^ key(v8) ^ 0x5A` |
| `0xA2` | `v11 += cmd[++v12]`（数据流跳距） |
| `0xA5` | 跳过 2 字节参数 |
| `0xA6` | `v11 += (v11 < dat_size)`（单步前进） |

密钥是双因子混合，同时依赖 `a7`（`.lucky0` 的 CRC32）与 `a8`（头部校验）：

```python
def key_byte(i, a7, a8):
    shift1 = (8*i + 16) & 0x18
    shift2 = 8 * (i & 3)
    v17 = ((a8 >> shift1) & 0xFF) ^ ((-98*i) & 0xFF) \
        ^ ((4*i) & 0xFF) ^ ((a7 >> shift2) & 0xFF)
    v18 = (7*i*i) & 0xFF
    v19 = (13*i - 89) & 0xFF
    return (v19 + v18) ^ v17
```

**关键自校验点**：`a7 = CRC32(.lucky0)`。若 `.lucky0`（含入口与解压桩）被任何修改，解压立即产出垃圾。这是**典型的完整性绑定反补丁设计**。

**验证**：解出 203,776 字节，`MZ` 头合法，输出 CRC32 = `0xF3F7B086` 与头部字段**精确吻合**。

### 2.2 Layer 2 — 五路反调试（sub_140003510）

```c
BOOL detect(void) {
    PEB *peb = NtCurrentPeb();
    BOOL dbg = peb->BeingDebugged;                          // +0x02
    if (peb->NtGlobalFlag & 0x70) dbg = TRUE;               // +0xBC
    if (peb->ProcessHeap && peb->ProcessHeap->Flags)        // +0x74
        dbg = TRUE;
    if (CheckRemoteDebuggerPresent(GetCurrentProcess(), &b)) dbg = TRUE;
    ULONG_PTR port = 0;
    NtQueryInformationProcess(GetCurrentProcess(), 7, &port, sizeof(port), NULL);
    if (port) dbg = TRUE;                                    // ProcessDebugPort
    return dbg;
}
```

**绕过**：软件断点 `0xCC` 会被 `.lucky0` 的 CRC32 自校验发现，因此必须使用硬件断点：

```
hbreak *0x1400035ef
c
set *(int*)($rbp - 4) = 0     # 把检测结果标志位清零
```

### 2.3 Layer 3 — 五变量流密码 SMC 自修改节

`.smc` 节在 `sub_140001880` 中现场解密，密钥由五个全局变量构成：

```c
// d_10C = CRC32(.text)
// d_108 = CRC32(.text[0 : len/2])
// d_104 = CRC32(.text[len/2 : len])
// d_074 = 0xB007A3BB（初始化常量）
// d_100 = dword_140545100（运行时滚动值）

u8 acc = 0, v5 = 0;
for (i = 0; i < len; i++) {
    u8 v10 = v5, v11 = v5++;
    u8 v12 = acc ^ (d104 >> ((8*v10 + 16) & 0x18));
    acc = (acc + 17) & 0xFF;
    smc[i] ^= (d108 >> (8*(v5  & 3)))
            ^ (d100 >> (8*(v11 & 3)))
            ^ (d074 >> (8*(v11 & 3)))
            ^ (d10C >> (8*(v11 & 3)))
            ^ v12 ^ 0xC3;
}
```

**关键观察**：三个 CRC32 全部绑定 `.text` 节内容。任何对代码段的修改都会让 `.smc` 解出乱码 —— 这是**代码段与自修改节的完整性互锁**。

实测五个变量（在 `sub_140004118` 处读取，无调试器污染时）：

```
dword_14054510C = 0x208E59B7
dword_140545108 = 0xF321689A
dword_140545104 = 0x6263BB A9
dword_140545074 = 0xB007A3BB
dword_140545100 = 0x51A70C1E   ← 后续 VM 指令解密的 D100
```

### 2.4 Layer 4 — 38 操作码字节码虚拟机

**解释器**：`sub_140003630`，jump table @ `0x14001C000`（`0x26` 项）

**VM 状态结构**（`a1`）：

| 偏移 | 类型 | 含义 |
|---|---|---|
| `+0x00..0x3F` | `u32[16]` | 虚拟寄存器 v0..v15 |
| `+0x40` | `u32` | EIP（字节码偏移） |
| `+0x44` | `u32` | halted |
| `+0x48..0x147` | `u8[256]` | vRAM |
| `+0x148` | `ptr` | 输入指针 |
| `+0x150` | `u32` | 输入长度 |

**完整操作码表（38 条）**：

```
0x00 HALT      halted = 1
0x01 FETCH     v16 = u8  code[eip++]
0x02 FETCH32   v16 = u32 code[eip]; eip += 4
0x03 FETCH32B  v17 = u32 code[eip]; eip += 4
0x04 FETCH16   v16 = u16 code[eip]; eip += 2
0x05 SEL_DST   dst = v16 & 0xF
0x06 SEL2      dst = (v16>>4)&0xF; src = v16&0xF
0x07 L_V0      v16 = reg[dst]
0x08 L_V1      v17 = reg[src]
0x09 S_V0      reg[dst] = v16
0x0A XOR       v16 ^= v17
0x0B OR        v16 |= v17
0x0C AND       v16 &= v17
0x0D ADD       v16 += v17
0x0E XORAND    v16 = (v16^v17) + 2*(v16&v17)   == v16+v17
0x0F SUB       v16 -= v17
0x10 ANDI      v16 &= code[eip++]
0x11 SHRI      v16 >>= code[eip++] & 0x1F
0x12 ROLI      v16 = rol32(v16, code[eip++])
0x13 ROR8      v16 = ror8(u8 v16, v17)
0x14 MEMRD     v16 = vram[v16 & 0xFF]
0x15 MEMWR     vram[reg[dst]&0xFF] = reg[src]
0x16 INPUTC    v16 = (reg[src] < len) ? input[reg[src]] : 0
0x17 INPUTLEN  v16 = len(input)
0x18 GETCFG    v16 = config[src & 3]
0x19 LOOKUP    v16 = lazy_lookup(reg[src])
0x1A EXIT      halted = 1
0x1B JNZ       if reg[dst] != 0: eip += v16
0x1C JMP       eip += v16
0x1D MUL       v16 *= v17
0x1E MOVZXB    v16 &= 0xFF
0x1F SHL1      v16 <<= 1
0x20 OR_DST    v16 |= reg[dst]
0x21 ROLVAR    v16 = rol32(v16, v17 & 31)
0x22 SHRVAR    v16 >>= v17 & 0x1F
0x23 MVTSRC    v17 = v16
0x24 OR_DST2   v16 |= reg[dst]
0x25 MEMRD2    v16 = vram[reg[src] & 0xFF]
```

### 2.5 指令流的「位置相关双因子流密码」

这是 lucky 最具特色的设计：**每帧指令用不同 seed 加密，且密钥同时依赖字节位置 idx 与本帧 seed**。

```c
// sub_140001790 — 精确实现
u8 decrypt_insn(u8 *buf, u32 idx, u8 seed) {
    u32 v = (7 * idx + seed - 0x5B) & 0xFF;          // 因子 1：位置 + seed
    u32 k = (D100 >> (8 * (idx & 3))) & 0xFF;        // 因子 2：滚动全局状态
    return buf[idx] ^ v ^ k;
}
```

### 2.6 关键陷阱：每帧 idx 独立归零

初次分析时按「绝对偏移」解密，得到满篇乱码。**运行时取证揭示了真相**：

```
SEED=0x21 IDX=0  SEED=0x21 IDX=1  SEED=0x21 IDX=2  ... SEED=0x21 IDX=4
SEED=0x2E IDX=0  SEED=0x2E IDX=1  ...                                    ← idx 重新从 0
SEED=0xAB IDX=0  SEED=0xAB IDX=1  SEED=0xAB IDX=2  SEED=0xAB IDX=3
SEED=0x7C IDX=0  ...  SEED=0x7C IDX=6
```

**每帧的 `idx` 都从 0 重新开始**，seed 逐帧变化。正确解析器必须以「帧」为单位重置 idx。

### 2.7 运行时实测的 8 帧完整程序

| 帧 | EIP | seed | 密文 | 明文 | 反汇编 |
|---|---|---|---|---|---|
| #0 | 0x00 | 0x21 | `d9c57182fc` | `0104020800` | `FETCH 4` / `FETCH32` / `S_V0` / `HALT` |
| #1 | 0x07 | 0x2E | `ccd244b1f1` | `0104020800` | 同构 |
| #2 | 0x0D | 0xAB | `4f5eed34` | `01051400` | `FETCH 5` / `MEMRD` / `HALT` |
| #3 | 0x0F | 0x7C | `3e208e7a2f40ec` | `0104061d0c0800` | `FETCH 4` / `SEL2` / `MUL` / `AND` / `L_V1` / `HALT` |
| #4 | 0x15 | 0x36 | `c4eb49a8e1f2` | `010507090800` | `FETCH 5` / `L_V0` / `S_V0` / `L_V1` / `HALT` |
| #5 | 0x17 | 0x76 | `042a887c203ae2` | `0104061d090800` | `FETCH 4` / `SEL2` / `MUL` / `S_V0` / `L_V1` / `HALT` |
| #6 | 0x1D | 0xB1 | `4955c0206c` | `0104031a00` | `FETCH 4` / `FETCH32B` / `HALT` |
| #7 | 0x21 | 0xB9 | `4372cb` | `031b00` | `FETCH32B` / `HALT` |

**验证**：`seed=0x21` 解密得到 `[0x01, 0x04, 0x02, 0x08, 0x00]`，与 winedbg 运行时捕获的操作码序列 `[1,4,2,8,0]` **逐字节吻合**。

### 2.8 决定性发现：样本无输入校验

**运行时证据**：

```
state + 0x150（输入长度） = 0
state + 0x148（输入指针） = 0x21FBB0（内容全 0）
```

无论输入 `""` / `"a"` / `"test"` / `"ABCD-EFGH"` / `"SN-000000-0000-0000"`，输出恒为 `Lisans: YANLIS`。

**静态证据（决定性）**：解包后的内层 PE 全部 38 个导入函数中**无任何输入读取函数**：

| 类别 | 导入 |
|---|---|
| 无 `ReadFile` / `scanf` / `fgets` / `getchar` / `fread` | ❌ 全部未导入 |
| 实际 I/O | `GetStdHandle` + `WriteFile`（纯输出） |
| `strncmp` | ⚠️ 已导入但**全镜像内零引用**（纯诱饵） |

**结论**：`crackme.lucky.exe` 是**纯展示型壳样本**，只演示自定义压缩与 VM 保护，不含 license 校验。输出恒为土耳其语 `Lisans: YANLIS`（"License: WRONG"）。**不存在"正确序列号"。**

> **方法论教训**：遇到「无论输入如何输出恒定」的样本，应**优先检查导入表是否存在输入读取函数**，而非陷入 VM 字节码求解。导入表检查耗时 30 秒，VM 全解耗时数小时。

---

## 三、 样本 B：Whale VM 的花指令湮灭与地址自基准加密

### 3.1 基址修正：PE 头声明不可信

| 项 | PE 头声明 | **winedbg 实测** |
|---|---|---|
| 模块基址 | `0x140000000` | **`0x140000000`**（但 GDB `%x` 打印截断为 `0x40000000`） |
| `.whale` 节基址 | `0x14000A000` | **`0x14000A000`**（`R15`） |

**关键坑**：GDB 的 `printf "%x"` 对 64 位值会截断，导致误判基址为 `0x40000000`。必须用 `%lx`。

### 3.2 256 项重定位分发表

**位置**：`RVA 0x537BC0`，256 × u32

```c
dec_rva   = enc ^ ((op * 0x9E3779B9) ^ 0xBD62813A);
handler   = r15 + dec_rva;     // r15 = .whale 节基址
```

### 3.3 主分发器（纯寄存器跳转）

```asm
mov  rax, [rdi+0xb0]        ; VIP
movzx rcx, byte [rsi+rax]   ; opcode
inc  qword [rdi+0xb0]       ; VIP++
mov  eax, [rbx + rcx*4]     ; 查加密表
imul edx, ecx, 0x9e3779b9   ; key = op * K
xor  edx, 0xbd62813a
xor  eax, edx               ; 解密 handler RVA
add  rax, r15               ; + 节基址
jmp  rax
```

无跳表内存读取，**纯算术分发**。

### 3.4 八类花指令体系（压缩比 99.2%）

`op 0x1b` 单个 handler 原始 `0x5550` 字节、约 5600 条指令，剥离后仅剩 **43 条真语义**。

| 类 | 模式 | 数量 | 零副作用证明 |
|---|---|---|---|
| **FILL** | `jmp qword ptr [rip+0]` = `ff 25 00 00 00 00` | 8 | `jmp [rip+0]` 跳到紧随其后的字节，等价 NOP |
| **A** | `push; mov eax,K; bsr eax,edx; cmp eax,0x1f; jne; ud2; pop` | 114 | 对非零 32 位数，`bsr` 结果 ∈ [0,31]，恒 < 0x1f |
| **B** | `push; mov eax,K; mov edx,eax; xor edx,eax; test; je; ud2; jmp[rip+0]; pop` | 111 | `edx ^= edx` 恒为 0，`test` 后 ZF=1，恒跳 |
| **C** | `mov eax,K; ror 13; rol 13; cmp eax,K; je; ud2` | 113 | 循环移位抵消，`cmp` 恒等 |
| **D** | `mov eax,K; and 0xFFFFFFFE; test al,1; je; call <dead>` | 108 | 清除最低位后 `al` 恒为偶，恒跳 |
| **E** | `stc; jb; ud2` | 107 | `stc` 后 CF=1，`jb` 恒跳 |
| **G** | `push rcx; push rdx; mov eax,K1; mov ecx,K2; ... ror edx,3; pop rdx; pop rcx` | 116 | 重言式恒等变换 |
| **H** | `push rcx; mov eax,K; mov ecx,eax; lea eax,[rax+rcx]; shl ecx,1; cmp eax,ecx; je; ud2; pop rcx` | 114 | `2K == 2K` 恒真 |
| **I** | `push rcx; mov rax,[rdi+0x400]; xor K1; rol rax,0xb; add K2; mov [rdi+0x400],rax; pop rcx` | 117 | ⚠️ **非花指令**，是真实状态推进 |

**类 I 的特殊性**：它是滚动校验累积器 `acc = rol64(acc ^ K1, 11) + K2`，具有真实副作用，**必须保留语义**（但可从指令流中提取为独立相位）。

**合计剥离**：791 处花指令序列 + 556 对 `push rax/pop rax` 噪声对。

### 3.5 VM 状态结构（128 虚拟寄存器）

| 偏移 | 类型 | 含义 |
|---|---|---|
| `+0x000..0x3FF` | `u64[128]` | 虚拟寄存器 v0..v127 |
| `+0x040` | `u64` | VSP（虚拟栈指针） |
| `+0x048` | `u64` | 返回值槽 |
| `+0x0B0` | `u64` | VIP |
| `+0x0B8` | `u64` | EFLAGS 镜像 |
| `+0x0C8` | `u32` | 滚动计数器 |
| `+0x148` | `ptr` | 输入缓冲区指针 |
| `+0x150` | `u32` | 输入长度 |

**初始寄存器值**（VM 启动前）：

```
r0 = 0x11FBB8 (VSP)      r1 = 0                r2 = 1
r4 = input_ptr           r5 = input_len        r6 = 0xA000 (.whale 大小)
r7 = heap_base           r8 = VSP              r9 = 0x2C75130A4 (seed)
```

### 3.6 指令编码长度表（运行时校准）

通过 winedbg 抓取连续 20 步执行的 VIP 序列，反推每条指令的真实长度：

| 长度 | opcode 数量 | 代表 |
|---|---|---|
| 2 | 54 | `NOP` / `RET` / `PUSH r` / `POP r` / 单寄存器操作 |
| 3 | 86 | `MUL` / `MOV` / `ADD` / `XOR` / `ROL` / `ROR` 等三字节编码 |
| 4 | 20 | `TEST w` / `CMP w` / `JCMP` |
| 5 | 8 | `CALL` / `LEA` / `MOVI32` |
| 6 | 7 | `JCC` / 6 字节 `LEA` |
| 7 | 3 | `ROLM` 变体 |
| 8 | 12 | `STORE` / `LOAD` |
| 9 | 63 | `MOVI` / `ORI` / `TESTI` / `MULI` |
| 10 | 3 | 部分 `MOVI` / `ORI` |

**交叉验证（23/24 精确匹配）**：

```
0x01 op=0x1b len=8    0x23 op=0x40 len=8    0x53 op=0x88 len=5
0x09 op=0xCF len=8    0x2B op=0x22 len=3    0x58 op=0x78 len=8
0x11 op=0x15 len=2    0x2E op=0x73 len=8    0x60 op=0x04 len=5
0x13 op=0xFA len=10   0x36 op=0x0E len=10   0x65 op=0x3A len=4
0x1D op=0x46 len=6    0x40 op=0xB3 len=6    0x69 op=0x63 len=6
```

### 3.7 【核心突破】地址自基准立即数加密

这是 Whale VM 最难的一层。立即数的加密密钥由**其自身的物理地址**决定：

```c
plain = raw ^ ((K * imm_addr) ^ C)

32-bit : K = 0x4C957F2D           C = 0xF7A79D5D
64-bit : K = 0x5851F42D4C957F2D   C = 0xA2C4FC7DF7A79D5D

imm_addr = 立即数在字节码流中的绝对偏移（不是 VIP，不是 EIP+k 的固定偏移）
```

**判定过程（踩坑记录）**：

| 尝试规则 | 结果 | 失败原因 |
|---|---|---|
| 基准 = `EIP` | 全乱码 | handler 会先 `inc rax` |
| 基准 = `VIP + 1` | 部分正确 | `CALL` 与 `MOVI` 的 VIP 推进方式不同 |
| 基准 = `EIP + 1` | 部分正确 | `LEA` 的 imm 在 `EIP+2` |
| **基准 = imm 自身地址** | **11/11 通过** | ✅ 正确 |

**关键洞察**：不同 handler 的 VIP 推进时机不同，导致 `imm` 位置各异，但**基准恒为 imm 自身地址**：

| 指令类别 | handler 读取模式 | imm 位置 |
|---|---|---|
| `MOVI/ORI`（9/10B） | `rax=VIP; inc rax; rdx=[rsi+rax]` | `EIP+1` |
| `CALL`（5B） | `rax=VIP; edx=[rsi+rax]` | `EIP+1` |
| `LEA`（5/6B） | `rax=VIP; edx=[rsi+rax+1]; inc rax` | `EIP+2` |
| `JCC`（6B） | 明文读取 | 不解密 |

**11/11 验证结果**：

```
ORI r8               EIP=0x012 -> 0x8F3E172D52CD4402   OK
MOVI r1              EIP=0x035 -> 0x5C04BB7069E0B822   OK
MOVI r7              EIP=0x045 -> 0xFAE8D5D5D69F7C14   OK
LEA r9               EIP=0x01C -> 0x7040 (PEB)          OK
LEA r13              EIP=0x03F -> 0x1D90               OK
CALL AddVectoredExceptionHandler  EIP=0x052 -> 0x80004068   OK
CALL GetModuleHandleA            EIP=0x05F -> 0x80004040   OK
CALL GetProcAddress              EIP=0x079 -> 0x80004038   OK
CALL GetCurrentThread            EIP=0x08B -> 0x80004048   OK
CALL GetCurrentProcess           EIP=0x11A -> 0x80004060   OK
CALL _beginthreadex              EIP=0x19E -> 0x800042D8   OK
```

### 3.8 双重交叉验证：运行时 VIP vs 静态反编译

最有力的正确性证明 —— **运行时 VIP 序列与静态反编译 VIP 序列完全吻合（偏移恒为 +1）**：

```
运行时 : 0x01 0x09 0x11 0x13 0x1D 0x23 0x2B 0x2E 0x36 0x40
         0x46 0x50 0x53 0x58 0x60 0x65 0x69 0x6F 0x77 0x7A
反编译 : 0x00 0x08 0x10 0x12 0x1C 0x22 0x2A 0x2D 0x35 0x3F
         0x45 0x4F 0x52 0x57 0x5F 0x64 0x68 0x6E 0x76 0x79
差值   : +1   +1   +1   +1   +1   +1   +1   +1   +1   +1
         +1   +1   +1   +1   +1   +1   +1   +1   +1   +1
```

偏移恒为 +1 是因为 dispatcher 在读取 opcode 后立即 `inc [rdi+0xb0]`。

### 3.9 CALL 指令：IAT 间接调用

```c
u32 imm = decrypt32(...);
void *fn;
if (imm & 0x80000000) {
    u32 rva = imm & 0x7FFFFFFF;
    fn = *(void**)(imageBase + rva);    // 取 IAT 项
} else {
    fn = (void*)(imageBase + imm);      // 直接地址（内部函数）
}
u64 ret = ((u64(*)(u64,u64,u64,u64,u64))fn)(
              state->reg[2],              // RCX = [rdi+0x10]
              vsp[4], vsp[5], vsp[6], vsp[7]);
state->retval = ret;                       // [rdi+0x48]
```

**已验证的 IAT 映射**：

| 常量 | 函数 |
|---|---|
| `0x80004038` | `KERNEL32!GetProcAddress` |
| `0x80004040` | `KERNEL32!GetModuleHandleA` |
| `0x80004048` | `KERNEL32!GetCurrentThread` |
| `0x80004060` | `KERNEL32!GetCurrentProcess` |
| `0x80004068` | `KERNEL32!AddVectoredExceptionHandler` |
| `0x800042D8` | `api-ms-win-crt-runtime!_beginthreadex` |
| `0x80004108` | `MSVCP140!std::cout` |

高位置位（`0x80000000`）就是「这是一个 IAT 索引而非直接地址」的标记。

### 3.10 JCC：绝对跳转而非相对

```c
u8  cond   = code[VIP];                                  // 0=TRUE 1=EQ 2=NE ...
u32 target = *(u32*)(code+VIP+1);                        // 明文
VIP += 5;
if (cond_table[cond]) VIP = target;                      // 绝对赋值，不是 +=
```

`cond_table` 由 EFLAGS 镜像现场构造：

```asm
popfq                                    ; 恢复 EFLAGS
mov  byte [rsp], 1                       ; cond 0 = TRUE
sete byte [rsp+1]                        ; cond 1 = EQ
setne byte [rsp+2]                       ; cond 2 = NE
setg byte [rsp+3]                        ; cond 3 = GT
setge byte [rsp+4]  setl [rsp+5]  setle [rsp+6]
seta byte [rsp+7]   setae [rsp+8]  setb [rsp+9]  setbe [rsp+0xa]
movzx eax, r8b                           ; cond
mov  al, byte [rsp+rax]                  ; 条件表查找
```

### 3.11 反调试函数（RVA 0x19D0）完整还原

```c
bool anti_debug(void) {
    PEB *peb = NtCurrentTeb()->ProcessEnvironmentBlock;
    if (peb) {
        if (peb->BeingDebugged)         return true;   // +0x02
        if (peb->NtGlobalFlag & 0x70)   return true;   // +0xBC
    }
    HMODULE h = GetModuleHandleA(enc_module_name_at_0x4480);
    if (!h) return false;
    fn NtQIP = GetProcAddress(h, "NtQueryInformationProcess");   // 明文 @0x44A8
    if (!NtQIP) return false;
    HANDLE hp = GetCurrentProcess();
    ULONG_PTR v = 0;
    if (NtQIP(hp, 7,    &v, 8, NULL) >= 0 && v != 0) return true;   // ProcessDebugPort
    v = 0;
    if (NtQIP(hp, 0x1E, &v, 8, NULL) >= 0 && v != 0) return true;   // ProcessDebugObjectHandle
    return false;
}
```

**运行时验证**：单步跟踪显示

```
0x19DA: mov  rax, gs:[0x60]      ; PEB
0x19E8: cmp  byte [rax+2], 0     ; BeingDebugged
0x19EC: jne  0x1A8F              ; ★ 跳转发生（winedbg 检测到调试）
```

`0x1A8F` 即 `return true` 分支。

### 3.12 反编译后的完整 VM 程序（182 条）

```asm
; === 初始化：保存现场、读取 PEB ===
[0000] STORE  [r8+8],  r7, 8
[0008] STORE  [r8+16], r1, 8
[0010] PUSH   r4                          ; 压入输入指针
[0012] ORI    r8, 0x8F3E172D52CD4402      ; 密钥常量
[001C] LEA    r9, base+0x7040             ; r9 = PEB
[0022] LOAD   r9, [r9+0], 8
[002A] XORAND r9, r8
[002D] STORE  [r8+96], r9, 8
[0035] MOVI   r1, 0x5C04BB7069E0B822
[003F] LEA    r13, base+0x1D90            ; 加密模块名
[0045] MOVI   r7, 0xFAE8D5D5D69F7C14
[004F] MOV    r2, r7

; === 反调试初始化：注册 VEH + 解析 API ===
[0052] CALL   *AddVectoredExceptionHandler
[005F] CALL   *GetModuleHandleA
[0064] TEST   r9, r9, 8
[0068] JCC    EQ, -> 0x0B3                ; 失败则跳过
[0076] MOV    r2, r9
[0079] CALL   *GetProcAddress
[007E] MOV    r4, r9
[0081] TEST   r9, r9, 8
[0085] JCC    EQ, -> 0x0B3
[008B] CALL   *GetCurrentThread
[0090] MOV    r2, r9

; === 主校验循环 ===
[00C2] JCC    EQ, -> 0x10B
[00C8] LEA    r13, base+0x4490            ; NtQueryInformationProcess 密文
[00DD] JCC    EQ, -> 0x10B
[00E3] CALL   *GetCurrentThread
[010B] CALL   0x19D0                      ; ★ 反调试函数
[0110] TEST   r9, r9, 1
[0114] JCC    EQ, -> 0x131
[011A] CALL   *GetCurrentProcess
[0131] ...
[013B] CALL   0x2720                      ; 堆操作
[0144] JCC    EQ, -> 0x15D
[014A] LEA    r2, base+0x2220             ; 内部函数

; === 线程创建（反调试监控线程）===
[0160] STORE  [r8+64], r9, 8
[0179] STORE  [r8+32], r1, 4
[0184] LEA    r15, base+0x1470
[019E] CALL   *_beginthreadex
[01AF] JCC    EQ, -> 0x43A

; === 输出阶段 ===
[02BF] LOAD   r2, r9, 8
[02C7] LOAD   r2, r2, 4
[02D8] CALL   *std::ios_base::operator bool
[02E1] JCC    NE, -> 0x368                ; 输出失败则退出
[02F8] LEA    r2, base+0x4108             ; r2 = &std::cout
[0326] CALL   *std::ostream::operator<< (manipulator)
[033B] CALL   0x1220                      ; cout 输出封装
[0346] CALL   *std::ostream::operator<< (int)   ; ★ 输出错误码
[0354] CALL   0x1220
[036C] RET
```

### 3.13 样本行为与遮挡机制

**运行时观测**：

| 输入 | 输出 |
|---|---|
| 空（仅换行） | `password:` 后直接退出 |
| 任意 1~64 字符 | `password:` + `failed (1)` |

**关键事实**：
1. `failed` 与 `password` 字符串**不在镜像中**（VM 动态构造）
2. `%d` 格式串可见于 `RVA 0x35CF` 的跳转桩内
3. VM 通过 `std::ostream::operator<<(int)` 输出错误码 `1`
4. 错误码恒为 `1` —— 说明 **`GetProcAddress` 必失败**

**失败根因**：
- `VM reg[2]` 初值 = `1`（无效模块句柄）
- `GetProcAddress(RCX=1, RDX=0x140001D90)`
- `0x140001D90` 指向 `.text` 内的代码字节 `ff c0 8b ff 00 0f ff cc`，**不是字符串**
- 因此 `GetProcAddress` 必然失败返回 0
- `[007E] MOV r4, r9` 把输入指针覆盖为 0，后续校验分支走失败路径

**这是样本的主动反分析设计** —— 用无效 API 名阻断调试路径。

---

## 四、 方法论沉淀

### 4.1 三层渐进式去混淆范式

两样本共通的处理骨架：

```
第一层：壳/压缩 → 静态解压 + CRC 自校验
   判据：文件体积 vs 内存体积差异过大；节名自定义；raw=0 而 VSize 巨大
   验证：解出 MZ + CRC32 与头部字段吻合

第二层：花指令/不透明谓词 → 模式匹配批量消除
   判据：大段 mov/bsr/ror/rol/setcc + ud2 序列，且无内存副作用
   验证：运行时 VIP 轨迹与反编译序列逐条比对

第三层：虚拟机语义 → 提取操作码表 + 指令编码长度 + 立即数解密
   判据：单点间接跳转（jmp rax / call r15+k）
   验证：小样本字段全部解出且语义自洽
```

### 4.2 硬件断点纪律（血泪教训）

| 场景 | 错误做法 | 正确做法 |
|---|---|---|
| 有 CRC 自校验的样本 | `break *addr`（插入 `0xCC`） | **`hbreak *addr`** |
| 有 PEB 反调试 | 直接断在目标 | 先 `hbreak` 反调试函数尾，`set *(int*)($rbp-4)=0` |
| 需要读取 64 位值 | `printf "%x"` | **`printf "%lx"`**（否则截断） |
| 断在相对偏移标签 | 把 `$rbp-relative` 当绝对地址 | 确认 `info symbol` 或反汇编上下文 |

### 4.3 「帧」概念：位置相关加密的正确解析

**通用判据**：当同一块密文在不同 seed 下解出完全相同的明文时，说明 **idx 基准是帧内的，而非绝对的**。

```python
# 错误：把 idx 当作绝对偏移
plain[i] = decrypt(buf[i], seed=first_seed, idx=i % len(buf))

# 正确：每帧独立重置 idx
frames = [(seed, buf) for each invocation]
for seed, buf in frames:
    plain = bytes(decrypt(buf[i], seed, i) for i in range(len(buf)))
```

**取证方法**：在解密函数入口抓 `(seed, idx, buf[idx])` 三元组，按 seed 分组，观察每组的 idx 序列是否从 0 开始。

### 4.4 「地址自基准」：立即数加密的终极形态

**通用判据**：当穷举 `EIP+k`（k ∈ {0,1,2,3,4}）作为解密基准都无法让多数立即数解出合理值时，尝试 **基准 = imm 自身地址**。

**反推方法**（已知一个目标明文时）：

```python
# 已知 raw（密文）、expected（期望明文）、K、C
# plain = raw ^ ((K * addr) ^ C)
# => (K * addr) = raw ^ plain ^ C
need = (raw ^ expected ^ C) & MASK
addr = (need * pow(K, -1, 1 << 64)) & MASK
# 若 addr 落在合理的字节码偏移范围内，规则成立
```

### 4.5 「无输入校验」的快速判据

遇到「无论输入如何行为恒定」的样本，**优先做导入表检查**，而非陷入 VM 求解：

```python
readers = ['ReadFile', 'ReadConsole', 'scanf', 'fgets', 'getchar',
           'fread', 'recv', 'WSARecv', 'std::cin']
hits = [i.name for e in pe.DIRECTORY_ENTRY_IMPORT
        for i in e.imports if i.name and any(r in i.name.decode() for r in readers)]
if not hits:
    print("样本无输入读取能力 → 纯展示型，不存在正确序列号")
```

**本案实证**：lucky 的 38 个导入中无任何读取函数，`strncmp` 导入但零引用。检查耗时 30 秒，避免了数小时的 VM 字节码求解。

### 4.6 交叉验证铁律

任何 VM 语义还原，**必须**运行双重验证：

| 验证 | 方法 | 通过标准 |
|---|---|---|
| **静态自洽** | 解码后的小样本字段（函数名、IAT 槽位、路径串）是否全部落在合理范围 | 100% |
| **动态对齐** | 运行时抓 VIP 序列，与反编译指令边界序列比对 | 偏移恒定，无跳变 |

只有双重验证都通过，才能宣布「VM 已破译」。

---

## 五、 踩坑日志（单条即坑）

1. **GDB `%x` 截断 64 位值** —— 把 `0x140000000` 显示成 `0x40000000`，导致误判基址、误判「handler 未映射」。必须用 `%lx`。
2. **软件断点 `0xCC` 被 CRC 自校验发现** —— 有完整性校验的样本必须用 `hbreak`。
3. **`push rax` / `pop rax` 成对噪声** —— 单条看是无害的保存/恢复，但夹在花指令之间会误判上下文。需成对合并消解。
4. **`jmp qword ptr [rip]` 不是跳表** —— `ff 25 00 00 00 00` 是 `jmp [rip+0]`，目标即下一条指令，纯填充。
5. **`op 0x1b` 的 VIP 已自增** —— dispatcher 读 opcode 后立即 `inc`，所以 handler 内的 `rax` 是「opcode 位置 + 1」。所有 `EIP+k` 推算都要 +1。
6. **花指令 `bsr` 型不可静态判死** —— `bsr eax, edx` 对非零数恒返回 [0,31]，但若 K=0 则结果未定义。需确认 K≠0。
7. **类 I 累积器不是花指令** —— `acc = rol64(acc ^ K1, 11) + K2` 有真实副作用，剥离时必须单独提取为「状态推进相位」。
8. **JCC 是绝对跳转** —— 不要当成相对偏移累加，否则控制流全错。
9. **VM 首指令在启动时已消费** —— `runtime[i] = file[8+i]`。若忽略这 8 字节偏移，整个字节码流水线错位。
10. **「无论输入输出恒定」优先查导入表** —— 不要先陷 VM 求解。30 秒的导入表检查可能直接中止整个分析。
11. **`LEA` 与 `CALL` 的 imm 位置不同** —— `LEA` 在 `EIP+2`（handler 用 `[rsi+VIP+1]`），`CALL` 在 `EIP+1`（handler 用 `[rsi+VIP]`）。不可统一处理。
12. **反编译验证要看 VIP 序列而非指令内容** —— 指令内容可能因为操作数解读偏差而看起来合理，但 VIP 边界序列一旦错位就会立刻暴露。

---

## 六、 工具与脚本

### 6.1 lucky 侧

| 文件 | 功能 |
|---|---|
| `unpack_lucky.py` | 定制 LZ 变体解压（含 CRC32 自校验验证） |
| `lucky_disasm.py` | 38 操作码解释器 + 8 帧流式解密反汇编 |
| `lucky_vm.py` | 完整 VM 解释器（可执行字节码） |
| `decrypt_lucky_vm.py` | 位置相关双因子流密码指令解密 |

### 6.2 Whale 侧

| 文件 | 功能 |
|---|---|
| `whale_handlers.py` | 256 项分发表解密 + 基址修正 |
| `whale_dejunk.py` | 8 类花指令全谱消解器（791 处 + 556 对） |
| `whale_isa.py` | 256 handler 批量提取与语义归类 |
| `whale_final2.py` | **最终反编译器（地址自基准立即数解密，11/11 验证）** |

### 6.3 关键脚本片段：花指令消解器骨架

```python
def match_junk(insns, i):
    """返回 (类别, 消耗指令数)；容错允许前导 push 缺失"""
    n = len(insns)
    if insns[i].bytes == b'\xff\x25\x00\x00\x00\x00':
        return ("FILL", 1)                    # jmp [rip+0]

    # 类 I：状态累积器（真实副作用，需保留）
    for pre in (0, 1):
        j = i + pre
        if (j + 8 < n and _m(insns[j], "push", "rcx")
                and "qword ptr [rdi + 0x400]" in insns[j+1].op_str
                and _m(insns[j+8], "pop", "rcx")):
            return ("I_acc", pre + 9)

    # 类 A：bsr 不透明谓词
    for pre in (0, 1, 2):
        k = i + pre
        while k < n and k < i + pre + 4 and _m(insns[k], "push"):
            k += 1
        if (k < n and _m(insns[k], "mov") and insns[k].op_str.startswith("eax,")
                and k + 6 < n and _m(insns[k+3], "cmp") and _m(insns[k+6], "ud2")):
            return ("A", k + 8 - i)

    # ... 类 B/C/D/E/G/H 类似
    return (None, 0)
```

---

## 七、 核心结论

| 项 | lucky | Whale |
|---|---|---|
| **壳层** | ✅ 完全解包（CRC32 吻合） | 无壳 |
| **反调试** | ✅ 五路全部识别并绕过 | ✅ 三重全部还原 |
| **自修改节** | ✅ 五变量流密码解密 | 无 |
| **花指令** | 无 | ✅ 8 类全削（99.2%） |
| **VM 操作码** | ✅ 38 条全还原 | ✅ 256 条全还原（72 组语义） |
| **指令解密** | ✅ 位置相关双因子 | ✅ 地址自基准 |
| **控制流** | ✅ 8 帧完整还原 | ✅ 182 条完整反编译 |
| **输入校验** | ❌ **样本不存在** | 存在但被假 API 调用阻断 |
| **Flag/Password** | **不存在**（纯展示型） | 未提取（反分析设计） |

**最大收获**：
1. **「地址自基准」立即数加密** 是一个通用判据 —— 任何 VM 在常规基准失效时都应尝试
2. **「帧内 idx 归零」** 是位置相关流密码的正确解析前提
3. **导入表 30 秒检查** 可避免数小时无效的 VM 求解
4. **运行时 VIP 序列核对** 是验证反编译器正确性的黄金标准
