# 2026-10-16 AegisShield 攻坚手记：Rust 反逆向分析、HWID 虚拟机绑定与 AES-256-CTR 提取

## 场景分类

二进制逆向 / Rust 语言分析 / 硬件指纹 (HWID) 绑定 / 自定义字节码虚拟机 / CWE-602 旁路验证

## 目标概述

对 `windows/vmp-crackmes/AegisShield/AegisShield_crackme_1.exe`（308KB Rust 工业级保护样本）执行全链路审计：
突破其 64 位 PCG 伪随机字符串动态混淆，
走查其 KVM 虚拟化与 CPUID 硬件指纹采集逻辑，
逆向其内嵌的 71 步 64 位自定义字节码虚拟机（`sub_140007FE0`），
定位硬编码判定门禁与目标哈希常量（`0x2A8FADFD62AD902E`），
通过微创修补旁路客户端单边实施漏洞（CWE-602），
驱动 AES-256-CTR 解密引擎释放 39 字节标准 Flag 明文。

## Scope 摘要（脱敏）

- auth_basis: 授权沙箱样本（CTF/Crackme 评估目标，`windows/vmp-crackmes/AegisShield/`）
- network_profile: offline（全程离线，无网络交互）
- asset_types: ["PE32+ x86-64 可执行文件", "Rust 运行时 (MSVC 工具链)", "HWID 绑定型代码虚拟化"]

## 角色

- lead_role: lead
- specialists: ["逆向分析副官", "Headless 仿真工程师"]

## 完整执行链路

### 阶段一：Rust 运行时梳理与字符串解密

1. **入口追踪**：通过 `mainCRTStartup` $\rightarrow$ `sub_14003A990` $\rightarrow$ `sub_1400086E0` 最终定位到 Rust 用户主函数 `sub_140003F40`。
2. **字符串混淆逆向**：
   - 样本中无明文 ASCII 提示，`sub_140001F40` 使用 `0xC0FFEE123456789A` 结合 64 位 PCG/LCG 状态机动态解密 166 字节文本池；
   - 提取出包含 `[-] ACCESS DENIED`、`[+] flag: `、`[i] license hwid: ` 在内的全量交互文本。

### 阶段二：71 步字节码虚拟机与硬编码黄金常量定位

1. **虚拟机架构**：
   - 位于 `sub_140007FE0`，其字节码存储在 `qword_14003F2B0`，运行时以 `0x0DDEBA5ECAFEF00D` 为 Seed 动态异或生成；
   - 提取 12 种 64 位虚拟指令算子（含 HWID 加载、代数乘加、循环移位与 LCG 步进）。
2. **门禁逻辑提取**：
   - 在控制流平坦化状态机中定位判定分支：
     `assert(v48 == 0x2A8FADFD62AD902E)`
   - 该常量在校验通过后直接作为种子，参与后续 256 位 AES 密钥扩展计算！

### 阶段三：CWE-602 旁路验证与 AES-256-CTR 解密

1. **漏洞原理**：
   - 样本虽然实现了高度复杂的虚拟机运算，但最终解密 Flag 所依赖的密钥由一个固定常数 `0x2A8FADFD62AD902E` 确定；
   - 属于典型的 **CWE-602（客户端强行实施安全机制）**，攻击者无需花费数月时间爆破单向不可逆哈希，直接在内存或二进制中旁路该分支即可驱动解密引擎。
2. **微创补丁实施**：
   - 消除故意制造崩溃的空指针解引用指令（`0x140004567` 处的 `eb 14`）；
   - 在 `0x140004506` 将失败状态 `0xae1f0b5c` 强行改写为成功状态 `0x74d93c42` 并跳转至解密例程。
3. **真实环境验证**：
   - 运行 Wine 交互测试，成功捕获 Flag 明文：
     $$\mathbf{CMO\{a3g1s\_vmp\_cff\_mba\_sh13ld\_1s\_4ct1v3\}}$$

---

## 关键技术突破与经验教训

1. **Rust 逆向中的“状态常数反推”战术**：
   - 在复杂的非线性单向散列面前，不要执着于数学求逆；优先检查该散列在程序后续流程中是否参与了对称加密或与硬编码常数直接对比，若存在硬编码常数，可直接将其作为已知条件反推下游密文。
2. **CWE-602 与数字信封的防御意义**：
   - 单机离线 Crackme 的根本局限性在于“密文和解密密钥的逻辑完全存在于客户端”；
   - 商业软件必须将特权验证下沉到服务端，严禁在客户端直接闭环决策。

---

## 交付物清单

1. **技术方法论文档**：`pe-reverse/techniques/05-crypto-unpack/14-aegisshield-rust-hwid-vm-and-aes-ctr-flag-recovery.md`
2. **自动化验证脚本**：`pe-reverse/techniques/05-crypto-unpack/solve_aegisshield.py`
3. **本地复现验证脚本**：`/root/逆向测试/work/aegis-shield/scripts/solve_aegisshield.py`
4. **验证依据 (Evidence)**：`reproduced`
