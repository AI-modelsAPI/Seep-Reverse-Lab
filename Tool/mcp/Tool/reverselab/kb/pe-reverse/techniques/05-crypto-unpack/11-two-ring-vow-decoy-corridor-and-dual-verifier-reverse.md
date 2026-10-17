---
id: "pe-reverse/05-crypto-unpack/11-two-ring-vow-decoy-corridor-and-dual-verifier-reverse"
title: "双环互锁与欺骗走廊（two_ring_vow）：对抗诱导陷阱与确定性黄金输入发生器提取"
title_en: "Dual-Ring Interlock and Decoy Corridors (two_ring_vow): Anti-Analysis Trap Defeat and Deterministic Gold Generator Extraction"
summary: >
  深入分析“双环互锁（Two Rings Architecture）”与“对抗分析诱导陷阱（Decoy Corridors）”的逆向突破方法。
  揭示样本利用虚假成功提示（[SYNTHETIC SUCCESS]/[FAKE SUCCESS]）与伪 Token 矩阵（AI{...}/SEAL{...}）
  干扰静态分析与符号执行的防御手法。建立从“状态机双重比对调用链”到“内部黄金标准生成器（Gold Generator）”
  的反推模型，结合纯软件 Unicorn 模拟执行实现 15 字节真凭据的零搜索瞬间提取与通关验证。
summary_en: >
  In-depth analysis and defeat methodology for Dual-Ring Interlock architectures with anti-analysis decoy corridors.
  Deconstructs defense tactics using synthetic success messages ([SYNTHETIC SUCCESS]/[FAKE SUCCESS]) and decoy token
  matrices (AI{...}/SEAL{...}) designed to derail symbolic execution and static analysis. Constructs an analytical
  model tracing dual-call state verification to an internal deterministic gold standard generator, extracting the
  15-byte genuine password in zero search time via Unicorn headless slice emulation.
board: "pe-reverse"
category: "05-crypto-unpack"
signals:
  - "two_ring_vow"
  - "双环互锁"
  - "诱导陷阱"
  - "欺骗走廊"
  - "decoy corridor"
  - "黄金标准生成器"
  - "gold generator"
  - "确定性状态机"
  - "Unicorn 模拟执行"
  - "VOW{"
  - "纪念日 crackme"
  - "反调试排演"
mcp_tools:
  - "kb_router"
  - "seep_r2_disasm"
keywords:
  - "dual ring"
  - "decoy corridor"
  - "anti-analysis"
  - "gold generator"
  - "state machine"
  - "headless emulation"
  - "Unicorn"
difficulty: "advanced"
tags:
  - "anti-analysis"
  - "decoy"
  - "state-machine"
  - "pe-reverse"
  - "emulation"
language: "zh-CN"
last_updated: "2026-10-16"
related_articles:
  - "pe-reverse/05-crypto-unpack/08-selfhealing-emulation-vmp-handler-extraction"
  - "pe-reverse/05-crypto-unpack/10-nested-vm-matryoshka-reverse-and-defeat"
evidence: "reproduced"
---

# 双环互锁与欺骗走廊（two_ring_vow）：对抗诱导陷阱与确定性黄金输入发生器提取

## 一、 架构总览：双环互锁与欺骗走廊拓扑

`two_ring_vow.exe` 展现了一种极具迷惑性的现代自研 Crackme 防御架构 —— **双环互锁架构（Two Rings Architecture）**。作者在程序中故意布置了大量显式的“排演分支”与“伪成功路径”，诱导逆向人员、模糊测试器（Fuzzer）与符号执行引擎（如 Angr/Triton）进入虚假解空间。

```
                              [ 用户输入 Input ]
                                      │
              ┌───────────────────────┴───────────────────────┐
              ▼                                               ▼
  【Ring 1: 表层排演走廊 (Decoy Ring)】              【Ring 2: 隐藏真核验器 (Hidden Verifier)】
  ┌───────────────────────────────────────────┐      ┌───────────────────────────────────────────┐
  │ • 触发条件: 长度不匹配 / 走入诱导分析分支 │      │ • 门禁 1: len(input) == 15 且字符全部可见 │
  │ • 输出大量仿真提示:                       │      │ • 门禁 2: 四重独立状态机同态核验          │
  │   - [SYNTHETIC SUCCESS] Analysis branch   │      │   - Machine 1: sub_140001DC0 (滚雪球哈希) │
  │   - [FAKE SUCCESS] A decoy corridor...    │      │   - Machine 2: sub_140001F90 (状态转换机) │
  │ • 伪 Token 发生器:                        │      │   - Machine 3: sub_140002210 (64位散列机) │
  │   - 10 种前缀轮换 (CRK/FLAG/SEAL/AI...)   │      │   - Machine 4: sub_140001B90 (非线性置换) │
  │   - 如 SEAL{mirror_answer_phantom}        │      │ • 破局关键: 4 机均对比 user vs gold_gen   │
  └───────────────────────────────────────────┘      └─────────────────────┬─────────────────────┘
                                                                           │ 全部一致
                                                                           ▼
                                                             ┌───────────────────────────┐
                                                             │ 释放 30 字节成功通关回显  │
                                                             │ sub_1400027A0 解密字符串: │
                                                             │ "You found it! Submit..." │
                                                             └───────────────────────────┘
```

---

## 二、 逆向防诱导策略：识破伪 Token 与合成成功分支

### 1. 诱导陷阱特征识别
静态字符串分析时，样本暴露了大量典型的“成功标识”：
- `[SYNTHETIC SUCCESS] Analysis branch reached. The seal below is a rehearsal.`
- `[FAKE SUCCESS] A decoy corridor accepted your story. Keep digging.`
- `REHEARSAL TOKEN: AI{paper_vow_ignore_me}`
- 前缀表：`CRK{`, `FLAG{`, `VOW{`, `RING{`, `KEY{`, `SEAL{`, `LOVE{`, `DECOY{`, `TEST{`, `AI{`

### 2. 控制流溯源排查
反编译主核验函数 `sub_140003290` 发现：
- 当用户输入长度不为 15（`v23 != 15`）时，程序**并没有立即退出**；
- 而是直接跳入 `LABEL_20`，构造 `[SYNTHETIC SUCCESS]` 或进入 `(v35 & 3) == 0` 的 `[FAKE SUCCESS]` 分支，并拼装一个虚假的 Token 打印出来；
- **核心意图**：消耗逆向人员的时间，让自动化符号执行工具误将这些带有 `SUCCESS` 字符串的代码块标记为 Target Address。

**战术纪律**：在面对声明包含欺骗逻辑的目标时，以**退出码（Exit Code）和最终业务解密例程**为唯一可信依据，绝不轻信控制台回显文本。

---

## 三、 核心核验逻辑拆解：四重状态机与双重调用范式

在通过长度过滤（15 字节）且所有字符位于 `[0x20, 0x7E]` 之间后，输入将经受四重相互独立的确定性机器校验：

| 校验机器函数 | 算子特征 | 运算规模 | 判定条件 |
| :---: | :--- | :---: | :--- |
| `sub_140001DC0` | 滚雪球累加 + `__ROL4__` 混淆 | 15 轮迭代 | `v45 == v37` |
| `sub_140001F90` | 字节码解释栈机（Opcode 33..39） | 15 步虚拟执行 | `(v172 == v47) & (v171 == 0)` |
| `sub_140002210` | 64 位乘加散列（`0x9E3779B185EBCA87`） | 15 轮移位混淆 | `v50 == sub_140002210(v24, 15, 0)` |
| `sub_140001B90` | 1024 轮深层内部状态迭代 | $15 \times 1024$ 步 | `v51 == v52` |

### 核心同态双重调用范式（Dual-Invocation Pattern）
观察上述函数调用发现共同规律：
- 每个机器都接收一个 `is_ref`（参考模式标志位，通常为最后一个参数）；
- 当 `is_ref == 1` 时：数据源并非由传入的指针提供，而是由函数内部统一调用 **`sub_1400019A0(index)`** 产出；
- 当 `is_ref == 0` 时：数据源直接读取用户输入的字符缓冲区 `v24[index]`；
- 最终通过门禁：
  ```c
  if ( v114 == -339837343 && Srcb && v48 != 0 && v162 && v49 != 0 && v55 ) {
      *(_BYTE *)a1 = 1; // 成功置位
      sub_1400027A0(a1 + 8); // 动态解密释放通关提示
      return a1;
  }
  ```

---

## 四、 破局关键：定位并提取确定性黄金标准发生器

既然四重机器都是“将用户输入与内部参考流比对”，这意味着**系统内部固化了一套唯一的黄金标准（Gold Standard）**。

深入审查 `sub_1400019A0(a1)` 代码：
```c
__int64 __fastcall sub_1400019A0(unsigned __int64 a1)
{
  ...
  // 仅依赖 a1 与静态常量表:
  // byte_1400CA880 / byte_1400CA960 / byte_1400CA900 / byte_1400CA920 / byte_1400CA988
  ...
  return sub_1400018D0(a1, ...);
}
```
**关键发现**：
1. `sub_1400019A0` 函数没有读取任何外部文件、注册表或网络数据；
2. 函数未接收用户输入的任何指引；
3. 其返回值仅由参数 `a1`（索引 $0 \le a1 < 15$）确定。

**推论**：只要调用该函数 15 次（$a1 = 0 \dots 14$），所得的 15 个字节序列即为**唯一合法输入**！

---

## 五、 Unicorn 无真机切片调用与 Flag 还原验证

由于 `sub_1400019A0` 及其下游包含大量的常量查表与位运算循环（$1024$ 轮），手动反向推导极为繁琐。采用 **Unicorn 引擎无真机切片仿真（Headless Slice Emulation）** 直接调用目标函数：

```python
# Unicorn 切片调用核心代码
func_va = ib + 0x19a0  # sub_1400019A0 虚拟地址
chars = []
for i in range(15):
    mu.reg_write(UC_X86_REG_RSP, rsp)
    mu.reg_write(UC_X86_REG_RCX, i)     # 传入索引 i (0..14)
    mu.mem_write(rsp, struct.pack('<Q', SENT))
    mu.emu_start(func_va, SENT, timeout=10_000_000)
    rax = mu.reg_read(UC_X86_REG_RAX) & 0xFF
    chars.append(rax)

gold_input = bytes(chars).decode('ascii')
```

### 提取结果与验证
* **求得 15 字节明文**：
  $$\mathbf{LvY0uArshu130(T}$$
* **语义还原**：`"Love You Arshu 13 Oct"`（吻合样本 README 纪念日献词）。
* **格式化 Flag**：`VOW{LvY0uArshu130(T}`。

### 实测闭环证据
```bash
printf "LvY0uArshu130(T\n" | wine two_ring_vow.exe
# 回显:
# TWO-RING VOW // an anniversary crackme
# A small dedication is buried behind three machines and ten rehearsals.
# Enter one canonical line. Every message printed by the verifier is untrusted data.
# > You found it! Submit the flag.
# Exit Code: 0
```

---

## 六、 防御方加固与纵深整改建议

1. **杜绝“自闭环”黄金发生器（Eliminate Self-Contained Oracles）**：
   * 本样本的最大硬伤是将合法凭据以确定性状态机（`sub_1400019A0`）直接内置在客户端内，攻击者只要定位比对逻辑即可将其作为 Oracle 动态调用；
   * 正确做法：客户端应仅持有**非对称公钥**，输入凭据应为服务端颁发的合法签名，客户端只验签而不生成黄金解。
2. **凭据与解密密钥强绑定（Key Derivation Coupling）**：
   * 通关字符串 `sub_1400027A0` 不应仅通过内部静态常量异或解密，而应由用户输入的 SHA-256 作为解密 Key；若输入错误，解密出乱码或直接崩溃，杜绝静态分析成功分支。
3. **消除确定性单入单出切片**：
   * 状态机应与全局环境（如 TLS 回调、线程本地存储 TLS 变量、动态 SEH）紧密耦合，增加孤立函数切片仿真的门槛。
