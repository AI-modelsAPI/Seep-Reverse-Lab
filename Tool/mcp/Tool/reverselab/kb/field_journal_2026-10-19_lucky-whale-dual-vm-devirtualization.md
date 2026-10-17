---
id: "field_journal/2026-10-19_custom-lz-whale-junk-vm-dual-sample"
title: "实战手记：LZ 壳 38 指令 VM 与 Whale 99.2% 花指令湮灭的双样本攻坚"
title_en: "Field Journal: Dual-Sample Assault on an LZ-Packed 38-Opcode VM and the 99.2% Junk-Code Whale VM"
date: "2026-10-19"
samples:
  - name: "crackme.lucky.exe"
    size: "3.6 MB"
    arch: "PE32+ x86-64 (Mingw-w64)"
    protection: "定制 LZ 变体 + 五路反调试 + SMC + 38 指令 VM"
    verdict: "壳与 VM 全破；样本本身不含输入校验"
  - name: "CrackMe0.exe (Whale)"
    size: "5.3 MB"
    arch: "PE32+ x86-64 (MSVC)"
    protection: "256 项重定位分发表 + 8 类花指令 + 128 寄存器 VM + 三重反调试"
    verdict: "VM 全破；校验路径被假 API 调用阻断"
outcome: "devirtualized"
signals:
  - "定制 LZ 压缩壳"
  - "CRC32 自校验"
  - "SMC 自修改节"
  - "五路反调试"
  - "38 指令虚拟机"
  - "位置相关双因子流密码"
  - "帧内 idx 归零"
  - "花指令"
  - "8 类不透明谓词"
  - "256 项重定位分发表"
  - "地址自基准立即数加密"
  - "运行时 VIP 轨迹交叉验证"
  - "无输入校验样本识别"
tags:
  - "custom-vm"
  - "packer"
  - "junk-code"
  - "anti-debug"
  - "smc"
  - "field-journal"
language: "zh-CN"
last_updated: "2026-10-19"
related_articles:
  - "pe-reverse/05-crypto-unpack/15-custom-lz-vm-and-whale-junk-code-vm-devirtualization"
  - "pe-reverse/05-crypto-unpack/10-nested-vm-matryoshka-reverse-and-defeat"
  - "pe-reverse/05-crypto-unpack/13-inside-the-machine-custom-vm-and-rolling-hash-defeat"
evidence: "reproduced"
---

# 实战手记：LZ 壳 38 指令 VM 与 Whale 99.2% 花指令湮灭的双样本攻坚

> 日期：2026-10-19
> 目标：`crackme.lucky.exe`（3.6 MB） + `CrackMe0.exe`（5.3 MB）
> 环境：Linux CLI + Wine + winedbg --gdb + Python 静态分析
> 约束：无真机 GUI，全部通过命令行与调试器取证完成

---

## 一、开局：两条完全不同的路

两个样本表面上都是「自定义虚拟机 crackme」，但骨架截然不同：

```
lucky  = 【壳优先】定制 LZ → 反调试 → SMC → 小 VM（16 寄存器）
Whale  = 【混淆优先】无壳 → 分发表 → 海量花指令 → 大 VM（128 寄存器）
```

**决策**：先做 lucky（壳层有明确结构，可快速建立信心与工具基础），再做 Whale（需要大量运行时取证）。

---

## 二、lucky：四层剥离

### 2.1 第一层 —— LZ 壳（30 分钟）

`.lucky1` 头部 32 字节结构清清楚楚：

```
4c434b31 001c0300  ...  314b534c = "LCK1" 魔数
```

关键字段：
- `unpacked_size = 203776`
- `checksum = 0xF3F7B086`
- `cmd_offset = 32`，`cmd_size = 722183`
- `dat_offset = 722215`，`dat_size = 843953`

第一次尝试直接把 `a7` 猜成 `header[8]`，解出乱码。翻反编译发现 `a7` 实际是 **`.lucky0` 节的 CRC32**：

```c
// sub_140001D30 — a7 的来源
u32 crc = 0xFFFFFFFF;
for (p = lucky0_start; p < lucky0_end; p++) {
    crc ^= *p;
    for (int i = 8; i; i--)
        crc = (crc >> 1) ^ (-(crc & 1) & 0xEDB88320);
}
return ~crc;
```

修正后：**解出 203,776 字节，`MZ` 头正确，CRC32 = `0xF3F7B086` 与头部字段完全吻合。**

> **这一刻建立了两条纪律**：①每次解包必须验证 CRC；②解包失败时不要暴力猜，去找反编译里的字段来源。

### 2.2 第二层 —— 五路反调试（40 分钟）

`sub_140003510` 五路：

```c
PEB->BeingDebugged
PEB->NtGlobalFlag & 0x70
ProcessHeap->Flags              // PEB->ProcessHeap[29]
CheckRemoteDebuggerPresent
NtQueryInformationProcess(7)    // ProcessDebugPort
```

**第一个坑**：直接 `break *0x1400035ef` 导致 `.lucky0` 的 CRC32 变化，解压立刻失败，程序静默退出。

**解法**：改用硬件断点。

```
hbreak *0x1400035ef
c
set *(int*)($rbp - 4) = 0     # 把检测标志清零
```

> 从此记住：**任何有自校验的样本，软件断点就是自杀。**

### 2.3 第三层 —— SMC 自修改节（1 小时）

`.smc` 节解密在 `sub_140001880`，五个全局变量：

```c
acc = 0; v5 = 0;
for (i = 0; i < len; i++) {
    v10 = v5; v11 = v5++;
    v12 = acc ^ (d104 >> ((8*v10 + 16) & 0x18));
    acc = (acc + 17) & 0xFF;
    smc[i] ^= (d108 >> (8*(v5  & 3))) ^ (d100 >> (8*(v11 & 3)))
            ^ (d074 >> (8*(v11 & 3))) ^ (d10C >> (8*(v11 & 3)))
            ^ v12 ^ 0xC3;
}
```

**关键观察**：`d_10C`、`d_108`、`d_104` 是 `.text` 三个区段的 CRC32 —— 这是**代码段与自修改节的完整性互锁**。任何代码修改都会让 `.smc` 解出垃圾。

用 winedbg 在 `sub_140004118` 处读五个变量（无调试器污染时）：

```
dword_14054510C = 0x208E59B7
dword_140545108 = 0xF321689A
dword_140545104 = 0x6263BB A9
dword_140545074 = 0xB007A3BB
dword_140545100 = 0x51A70C1E    ← 记下这个 D100，后面 VM 指令解密要用
```

解密后是标准 x64 序言：`push rbp; mov rbp,rsp; sub rsp,0x70; ...`

### 2.4 第四层 —— 38 指令 VM（3 小时，含一次重大误判）

**解释器** `sub_140003630`，jump table @ `0x14001C000`，`0x26` 项。

**第一个重大误判**：我把 jump table 指向的地址当成了 handler 代码，反汇编出来是 `jb / jae / push -0x33 / imul ecx,esp,...` —— 典型的「数据被当代码」特征。

**原因**：`0x14002F170` 等地址全落在 `.rdata`，不是 `.text`。真正的 handler 在 `sub_140003630` 内的 `switch` 链里。

修正后拿到完整 38 条操作码语义。

**第二个重大误判（最贵的坑）**：指令流解密。

`sub_140001790` 的公式：

```c
out = buf[idx] ^ ((7*idx + seed - 0x5B) & 0xFF) ^ (D100 >> (8*(idx & 3)));
```

我最初把 `idx` 当作**字节码流中的绝对偏移**，得到满篇乱码，然后花了两小时怀疑公式、怀疑 D100、怀疑字节序。

**转折点**：winedbg 抓 `sub_140001790` 的调用三元组。

```
SEED=0x21 IDX=0  SEED=0x21 IDX=1  SEED=0x21 IDX=2  SEED=0x21 IDX=3  SEED=0x21 IDX=4
SEED=0x2E IDX=0  SEED=0x2E IDX=1  SEED=0x2E IDX=2  SEED=0x2E IDX=3  SEED=0x2E IDX=4
SEED=0xAB IDX=0  SEED=0xAB IDX=1  SEED=0xAB IDX=2  SEED=0xAB IDX=3
```

**idx 每帧都从 0 重新开始！**

立刻用正确公式验证 `seed=0x21`：

```python
buf = [0xD9, 0xC5, 0x71, 0x82, 0xFC]
# out[0] = 0xD9 ^ (0x21-0x5B) ^ 0x1E = 0x01
# out[1] = 0xC5 ^ (7+0x21-0x5B) ^ 0x0C = 0x04
# out[2] = 0x71 ^ (14+0x21-0x5B) ^ 0xA7 = 0x02
# out[3] = 0x82 ^ (21+0x21-0x5B) ^ 0x51 = 0x08
# out[4] = 0xFC ^ (28+0x21-0x5B) ^ 0x1E = 0x00
=> [0x01, 0x04, 0x02, 0x08, 0x00]
```

与 winedbg 运行时捕获的操作码 `[1,4,2,8,0]` **逐字节吻合**。

> **沉淀出通用判据**：**位置相关加密中，若同一密文在不同 seed 下解出相同明文，则 idx 基准是帧内的。** 取证方法是抓 `(seed, idx)` 配对看序列是否重置。

### 2.5 结局：样本不含校验

8 帧全部解出后，我把所有帧拼接试图还原完整程序，结果发现每帧都是**独立小程序**（`FETCH / ... / HALT`）。

于是直接问：程序读输入了吗？

```python
readers = ['ReadFile','scanf','fgets','getchar','fread']
# lucky 的 38 个导入 → 零命中
```

再看运行时：

```
state+0x150（输入长度）= 0
state+0x148（输入指针）= 0x21FBB0，内容全 0
```

**结论：`crackme.lucky.exe` 是纯展示型壳样本，不含任何 license 校验逻辑。** 输出恒为 `Lisans: YANLIS`。

> **沉痛教训**：这个结论本应在**开始 VM 逆向之前**用 30 秒得出。导入表检查应该在壳解开后立刻做。
>
> 新纪律：**壳解开后，第二步（反调试之后）就是查导入表是否存在输入读取函数。无则立刻终止 VM 逆向。**

---

## 三、Whale：99.2% 噪声的湮灭

### 3.1 第一个坑 —— GDB 截断 64 位值

在 `0x14000A44C`（`jmp rax`）抓 handler 地址：

```
RAX=0x40098eb0  R15=0x4000a000  RDI=0x11cdb8  RSI=0x40538e80
```

据此判断「模块基址 = 0x40000000」，然后所有静态地址计算全部错位，Unicorn 仿真在第一跳就报「未映射」。

**真相**：`printf "%x"` 对 64 位值会截断。改用 `%lx`：

```
R14full=0x140000000  RDX=0x140001d90
```

**基线就是标准的 `0x140000000`。** 之前两小时的「未映射」困惑全部源于一个格式化字符。

> **纪律**：GDB 读 64 位值一律 `%lx`。

### 3.2 分发表（20 分钟）

`RVA 0x537BC0`，256 × u32：

```python
dec_rva = enc ^ ((op * 0x9E3779B9) ^ 0xBD62813A)
handler = r15 + dec_rva
```

256 项全部解出，分布均匀（步长 ≈ 0x5400）。

### 3.3 花指令：从「看不懂」到「99.2%」

打开 `op 0x1b` 的 handler（`0x140098EB0`，5.5 KB），满眼都是：

```asm
mov  eax, 0x4b720b7f
mov  edx, eax
bsr  eax, edx
cmp  eax, 0x1f
jne  +2
ud2
```

一开始以为是加密逻辑，直到在 15 处不同的 IMM 值上看到**完全相同的模式**才意识到是花指令。

**识别过程**：

1. 先写出 `is_junk_sequence()` 匹配最明显的一类（`bsr` 型）
2. 跑一遍：消掉 225 处
3. 看剩余，发现新的模式（`xor edx,eax` 型）→ 再加一条规则
4. 重复 5 轮，最终覆盖 8 类

**最终统计**：

| 类 | 模式 | 数量 |
|---|---|---|
| FILL | `jmp [rip+0]` | 8 |
| A | `bsr eax,edx; cmp 0x1f; jne; ud2` | 114 |
| B | `mov edx,eax; xor edx,eax; test; je; ud2` | 111 |
| C | `ror 13; rol 13; cmp K; je; ud2` | 113 |
| D | `and 0xFFFFFFFE; test al,1; je; call <dead>` | 108 |
| E | `stc; jb; ud2` | 107 |
| G | 重言式恒等（14 条） | 116 |
| H | `lea eax,[rax+rcx]; shl ecx,1; cmp eax,ecx; je; ud2` | 114 |
| **I** | **`acc = rol64(acc^K1,11)+K2`（真实副作用）** | 117 |

加上 556 对 `push rax/pop rax` 噪声，从 5600 条砍到 **43 条真语义**。

> **关键洞察**：类 I 看起来像花指令（同样的 push rcx / pop rcx 包裹），但它是**真实的滚动校验状态推进**。剥离后必须单独提取为「状态相位」，否则丢失语义。

### 3.4 最硬的一关：立即数加密

**症状**：反编译出来 `LOAD r9, [r9+0]`，`disp=0`，但 `r9` 的值是 `0x140007040`（PEB 地址）。

追下去发现 `LEA r9, base+0x7842ae4d` —— 但运行时 `r9 = 0x140007040`，即偏移只有 `0x7040`。

**第一次尝试**：基准 = `VIP`
→ 解出 `0x556bff1f`，加上 base 是 `0x956bff1f`，不是 `0x7040`。失败。

**第二次尝试**：基准 = `EIP+1`
→ `0x7040`，命中了！但只对 `LEA` 有效，`ORI`/`MOVI` 全部乱码。

**第三次尝试**：基准 = `EIP+2`
→ `LEA` 对了，`ORI` 还是 `0x70`（期望 `0x8F3E172D52CD4402`）。

**穷举反推**（转折点）：

```python
for pos in range(0x0a, 0x100):
    raw = int.from_bytes(code[pos:pos+8], 'little')
    for base in range(pos-16, pos+16):
        if d64(raw, base) == 0x8F3E172D52CD4402:
            print(hex(pos), hex(base))
# => 0x13 0x13
```

**`pos == base`！立即数的物理位置就是解密基准！**

再对 `LEA` 做同样反推：`pos=0x1e, base=0x1e`。

**规则**：`plain = raw ^ ((K * imm_addr) ^ C)`，`imm_addr` 是 imm 在字节码流中的绝对偏移。

**11/11 全部验证通过**：

```
ORI r8  EIP=0x012 imm@0x013 -> 0x8F3E172D52CD4402   OK
MOVI r1 EIP=0x035 imm@0x036 -> 0x5C04BB7069E0B822   OK
MOVI r7 EIP=0x045 imm@0x047 -> 0xFAE8D5D5D69F7C14   OK
LEA r9  EIP=0x01C imm@0x01E -> 0x7040  (PEB)        OK
LEA r13 EIP=0x03F imm@0x041 -> 0x1D90               OK
CALL AddVeh       -> 0x80004068   OK
CALL GetModuleHandleA -> 0x80004040   OK
CALL GetProcAddress   -> 0x80004038   OK
CALL GetCurrentThread -> 0x80004048   OK
CALL GetCurrentProcess -> 0x80004060   OK
CALL _beginthreadex    -> 0x800042D8   OK
```

> **为什么不同指令的 imm 位置不同？** 因为不同 handler 的 VIP 推进时机不同：
> - `MOVI`：`rax=VIP; inc rax; rdx=[rsi+rax]` → imm 在 `VIP+1`
> - `CALL`：`rax=VIP; edx=[rsi+rax]` → imm 在 `VIP`
> - `LEA`：`rax=VIP; edx=[rsi+rax+1]; inc rax` → imm 在 `VIP+1`
>
> 但基准**恒为 imm 自身地址** —— 这是个漂亮的统一。

### 3.5 黄金验证：运行时 VIP vs 静态反编译

最有力的正确性证明：

```
运行时 : 0x01 0x09 0x11 0x13 0x1D 0x23 0x2B 0x2E 0x36 0x40
         0x46 0x50 0x53 0x58 0x60 0x65 0x69 0x6F 0x77 0x7A
反编译 : 0x00 0x08 0x10 0x12 0x1C 0x22 0x2A 0x2D 0x35 0x3F
         0x45 0x4F 0x52 0x57 0x5F 0x64 0x68 0x6E 0x76 0x79
差值   : +1   +1   +1   +1   +1   +1   +1   +1   +1   +1
         +1   +1   +1   +1   +1   +1   +1   +1   +1   +1
```

20 步全部偏移恒定 +1（dispatcher 读完 opcode 就 `inc`）。**这证明指令长度表和控制流 100% 正确。**

> **纪律**：反编译验证要看 **VIP 边界序列**，不要看指令内容。内容可能因为操作数解读偏差而「看起来合理」，但边界一旦错位立刻暴露。

### 3.6 顺便揪出的反调试

反编译后发现 `[010B] CALL 0x19D0`，跟进：

```c
bool anti_debug(void) {
    PEB *peb = NtCurrentTeb()->ProcessEnvironmentBlock;
    if (peb) {
        if (peb->BeingDebugged)         return true;
        if (peb->NtGlobalFlag & 0x70)   return true;
    }
    HMODULE h = GetModuleHandleA(enc_str_at_0x4480);
    fn NtQIP = GetProcAddress(h, "NtQueryInformationProcess");
    HANDLE hp = GetCurrentProcess();
    ULONG_PTR v;
    if (NtQIP(hp, 7,    &v, 8, NULL) >= 0 && v) return true;
    if (NtQIP(hp, 0x1E, &v, 8, NULL) >= 0 && v) return true;
    return false;
}
```

单步验证：

```
0x19DA: mov  rax, gs:[0x60]      ; PEB
0x19E8: cmp  byte [rax+2], 0
0x19EC: jne  0x1A8F              ; ★ 跳转（winedbg 检测到）
```

### 3.7 最后一道墙：假 API 调用

VM 程序反编译完后，看输出逻辑：

```
[02F8] LEA  r2, base+0x4108              ; r2 = &std::cout
[0326] CALL *std::ostream::operator<<
[0333] CALL 0x1220
[0346] CALL *std::ostream::operator<< (int)   ; 输出错误码
[036C] RET
```

问：错误码怎么算的？追到 `GetProcAddress`：

```
GetProcAddress(RCX=1, RDX=0x140001D90)
```

- `RCX = 1`：`VM reg[2]` 的初值，不是有效模块句柄
- `RDX = 0x140001D90`：指向 `.text` 的**代码字节** `ff c0 8b ff 00 0f ff cc`，**不是字符串**

`GetProcAddress` 必然返回 0 → `[007E] MOV r4, r9` 把输入指针清零 → 后续走失败分支 → 输出 `failed (1)`。

**这是样本的主动反分析设计**：用无效 API 名阻断调试路径。

---

## 四、两条纪律的诞生

### 4.1 纪律一：壳解开后，第二步查导入表

```
解壳 → 查反调试 → 【查导入表是否有读输入函数】→ 才开始 VM 逆向
```

lucky 用了这个纪律的「事后版本」：如果早做，能省 3 小时。

```python
READERS = ['ReadFile','ReadConsole','ReadConsoleInput','scanf','fgets',
           'getchar','fread','recv','WSARecv','std::cin']
hits = [i.name for e in pe.DIRECTORY_ENTRY_IMPORT
        for i in e.imports
        if i.name and any(r in i.name.decode() for r in READERS)]
if not hits:
    print("样本无输入读取能力 → 纯展示型，无正确序列号")
```

### 4.2 纪律二：反编译器正确性必须双验

| 验证 | 方法 | 标准 |
|---|---|---|
| 静态自洽 | 小样本字段（API 名、IAT 槽位、路径串）是否全部合理 | 100% |
| 动态对齐 | 运行时 VIP 序列 vs 静态指令边界序列 | 偏移恒定，无跳变 |

只有两条都过，才能说「VM 已破译」。

---

## 五、时间账

| 阶段 | 耗时 | 备注 |
|---|---|---|
| lucky 壳层解压 | 30 min | 含一次 `a7` 来源误判 |
| lucky 反调试绕过 | 40 min | 含软件断点自杀一次 |
| lucky SMC 解密 | 1 h | 五变量流密码 |
| lucky VM 操作码 | 1 h | 含 jump table 误判 |
| **lucky VM 指令解密** | **2 h** | 帧内 idx 归零的顿悟 |
| lucky 确认无校验 | 10 min | 导入表检查（太晚） |
| **Whale GDB 截断坑** | **2 h** | `%x` vs `%lx` |
| Whale 分发表 | 20 min | 顺利 |
| Whale 花指令 5 轮迭代 | 2 h | 从 1 类到 8 类 |
| **Whale 立即数加密** | **3 h** | 穷举反推发现「地址自基准」 |
| Whale 反调试还原 | 40 min | 反编译后顺手跟 |
| Whale 假 API 定位 | 30 min | 输出逻辑反推 |

**总计：约 14 小时**，其中约 **4 小时浪费在三个格式化/基准误判上**。

---

## 六、留给下一次的三条备忘

1. **进 GDB 前先写一份检查清单**：`%lx` / `hbreak` / `x/<N>bx` 用对地址。这三个错误占了总耗时的 30%。
2. **花指令消解是迭代过程，不是一次性工程**：写一条规则 → 跑 → 看剩余 → 加规则。5 轮是正常节奏。
3. **「地址自基准」应进工具箱**：下次遇到立即数解密失效，第一反应就试这个，而不是逐个 `EIP+k` 猜。
