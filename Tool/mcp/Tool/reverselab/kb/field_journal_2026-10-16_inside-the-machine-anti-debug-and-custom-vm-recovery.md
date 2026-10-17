# 2026-10-16 Inside-the-Machine 攻坚手记：极简自定义 VM 逆向、死代码花指令消除与代数约束求根

## 场景分类

二进制逆向 / 自定义代码虚拟化 / 反调试对抗 / 花指令消除 / 代数约束求解

## 目标概述

对 `windows/vmp-crackmes/Inside-the-Machine/crackme.exe`（24KB 极简自研虚拟机样本）执行全流程破译：
梳理其集成的密集反调试策略（时钟差、模块检测、控制台动态解密），
逆向其 8 寄存器精简虚拟机解释器及 Opcode 滚动密钥置换机制，
识别并消除花指令恒真跳转形成的死代码盲区，
还原出 26 组单字节代数方程与全局 Rolling Hash 约束，实现秒级求根并在实机环境达成 Exit Code 0 闭环。

## Scope 摘要（脱敏）

- auth_basis: 授权沙箱样本（CTF/Crackme 评估目标，`windows/vmp-crackmes/Inside-the-Machine/`）
- network_profile: offline（全程离线，无网络交互）
- asset_types: ["PE32+ x86-64 可执行文件", "MinGW GCC 16.2.0", "精简自定义代码虚拟化 (Custom VM)"]

## 角色

- lead_role: lead
- specialists: ["逆向分析副官", "Headless 仿真工程师"]

## 完整执行链路

### 阶段一：静态侦察与动态文本解密

1. **反调试机制梳理**：
   - 样本集成了 QPC 耗时检测，要求关键验证函数执行时间 $\le 300\text{ms}$，否则强行将结果异或污染；
   - 在启动阶段通过快照遍历枚举模块，阻断调试注入工具（如 `scylla`）。
2. **控制台文本解密**：
   - 样本控制台无明文字符串，全部调用 `sub_140001EF0` 动态 4 字节轮换异或解密；
   - 提取并解密出标题 Banner、`Enter password:` 提示、错误提示 `[-] Wrong password.` 以及成功回显 `[+] Correct! The machine accepted your password.`。

### 阶段二：虚拟机解释器架构与 Opcode 映射还原

1. 核心解释器位于 `sub_1400014C0`，维护 8 个通用 32 位虚拟寄存器 `r0` ~ `r7`，返回值为 `r0`。
2. 识别滚动密钥取指解码：
   $$v8 = \text{byte\_140005520}[(v3 \oplus \text{raw}) \ \& \ 0xFF]$$
   $$v3 = (v8 + 33 \times v3 + 7) \pmod{256}$$
3. 提取全部 14 种字节码算子（包含寄存器运算、直接数加载、单字节输入映射、长度获取及相对条件跳转）。

### 阶段三：花指令跳跃与死代码消除

1. 在对 1762 字节的虚拟字节码进行反汇编追踪时，发现指令序列中多次出现恒真跳转：
   `[0171] r7 = 0xe97fa113; r7 += 0x16805eed; if r7 == 0 goto 0x1c7`
2. 由于常数相加后溢出严格为 0，程序直接跳过了后续 71 字节；若反汇编器线性扫描未执行区，会导致滚动密钥 `v3` 步进错位。
3. 修正反汇编引擎后，完整还原出 366 条真实执行指令。

### 阶段四：代数求根与全局哈希验证

1. 判定逻辑高度结构化：
   - 首先硬性约束长度 `len(input) == 26`（0x1a）；
   - 对 26 个输入字符依次执行独立代数表达式（乘/加/异或/循环移位）并与目标常数比对，结果 OR 进 `r0`；
   - 全局滚动哈希校验：$\text{hash}_{26} == \text{0xee6ceb17}$。
2. 编写求解脚本对 26 个单字节独立方程进行瞬时求根：
   $$\mathbf{V1rtu4lM4ch1n3\_1ns4n3\_2026}$$
3. 代入全局 Rolling Hash 验证，结果完全吻合（异或差值为 0）。

### 阶段五：真实环境验证

- 在 Wine 环境下运行交互测试，输入 `V1rtu4lM4ch1n3_1ns4n3_2026`：
  - 成功捕获放行文本：`[+] Correct! The machine accepted your password.`
  - 退出码为 `0`！

---

## 关键技术突破与经验教训

1. **紧凑不等于脆弱，但代数独立断言仍是死穴**：
   - 24KB 的体积能集成反调试、字符串加密、VM 解释器与花指令跳转，展现了极高的代码密度；
   - 然而最核心的漏洞依然是**逐字符独立断言（Lack of Diffusion）**，使得防御者耗费心血构造的复杂虚拟机在简单的单字节穷举面前不堪一击。
2. **滚动密钥状态机的死代码敏感性**：
   - 当虚拟指令集引入上下文滚动密钥解码（Rolling Decoding）时，任何死代码跳跃都会直接影响解码上下文；逆向分析必须采用控制流可达性追踪，绝不能使用简单的盲目线性反汇编。

---

## 交付物清单

1. **技术方法论文档**：`pe-reverse/techniques/05-crypto-unpack/13-inside-the-machine-custom-vm-and-rolling-hash-defeat.md`
2. **自动化破译脚本**：`pe-reverse/techniques/05-crypto-unpack/solve_inside.py`
3. **本地复现验证脚本**：`/root/逆向测试/work/inside-machine/scripts/solve_inside.py`
4. **验证依据 (Evidence)**：`reproduced`
