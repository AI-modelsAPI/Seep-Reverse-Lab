# pe-reverse 技术库目录

> 本目录由 `kb_maintain.py --sync-index` 自动生成（2026-10-17）
> 共 10 类 / 46 篇

## 完整目录

### 01-triage — 初筛（1）

- [`01-triage/01-aob-signature-scan.md`](01-triage/01-aob-signature-scan.md) — AOB 特征码扫描

### 02-pe-structure — PE 结构（2）

- [`02-pe-structure/01-pe-header-parsing.md`](02-pe-structure/01-pe-header-parsing.md) — PE 头解析与节区定位
- [`02-pe-structure/02-tls-callback-analysis.md`](02-pe-structure/02-tls-callback-analysis.md) — TLS Callback 定位与早期执行链

### 03-static-analysis — 静态分析（7）

- [`03-static-analysis/01-struct-reconstruction.md`](03-static-analysis/01-struct-reconstruction.md) — 内存结构体逆向重建
- [`03-static-analysis/02-disasm-jit-asm.md`](03-static-analysis/02-disasm-jit-asm.md) — 反汇编（Zydis）与 JIT 汇编（Xbyak）
- [`03-static-analysis/03-x64dbg-breakpoints.md`](03-static-analysis/03-x64dbg-breakpoints.md) — x64dbg 断点策略
- [`03-static-analysis/04-reclass-reconstruction.md`](03-static-analysis/04-reclass-reconstruction.md) — ReClass 结构体实时重建
- [`03-static-analysis/05-dynamic-api-resolution.md`](03-static-analysis/05-dynamic-api-resolution.md) — 动态 API 解析链还原
- [`03-static-analysis/06-go-rust-binary-reconstruction.md`](03-static-analysis/06-go-rust-binary-reconstruction.md) — Go 与 Rust 编译型二进制逆向特征还原指南
- [`03-static-analysis/07-ida-microcode-mba-deobfuscation-d810.md`](03-static-analysis/07-ida-microcode-mba-deobfuscation-d810.md) — IDA Pro 微代码（Microcode）现代反混淆：D810-ng 消除 MBA 与虚假控制流

### 04-dynamic-analysis — 动态分析（8）

- [`04-dynamic-analysis/01-dll-injection.md`](04-dynamic-analysis/01-dll-injection.md) — DLL 注入三模式
- [`04-dynamic-analysis/02-trampoline-detour.md`](04-dynamic-analysis/02-trampoline-detour.md) — Trampoline Hook（函数劫持）
- [`04-dynamic-analysis/03-external-memory-rw.md`](04-dynamic-analysis/03-external-memory-rw.md) — 外部进程内存读写
- [`04-dynamic-analysis/04-naked-function-hook.md`](04-dynamic-analysis/04-naked-function-hook.md) — Naked 函数 Hook（内联汇编）
- [`04-dynamic-analysis/05-anti-debug-bypass.md`](04-dynamic-analysis/05-anti-debug-bypass.md) — 反调试检测与绕过
- [`04-dynamic-analysis/06-manual-map-injection.md`](04-dynamic-analysis/06-manual-map-injection.md) — 手动映射 DLL 注入
- [`04-dynamic-analysis/07-direct-syscall.md`](04-dynamic-analysis/07-direct-syscall.md) — Direct Syscall：绕过用户态 Hook
- [`04-dynamic-analysis/08-procmon-patterns.md`](04-dynamic-analysis/08-procmon-patterns.md) — Procmon 行为监控与过滤

### 05-crypto-unpack — 加密/内存转储与还原解包（13）

- [`05-crypto-unpack/01-pe-unpack-dump.md`](05-crypto-unpack/01-pe-unpack-dump.md) — PE 脱壳与内存 Dump
- [`05-crypto-unpack/02-vmp-virtualization-analysis.md`](05-crypto-unpack/02-vmp-virtualization-analysis.md) — VMP 虚拟化原理与 VM Entry 定位
- [`05-crypto-unpack/03-vmp-devirtualization-toolchain.md`](05-crypto-unpack/03-vmp-devirtualization-toolchain.md) — VMP 去虚拟化工具链（Devirtualization）
- [`05-crypto-unpack/04-twinbasic-compressed-resource-recovery.md`](05-crypto-unpack/04-twinbasic-compressed-resource-recovery.md) — TwinBasic/VB6 程序压缩资源还原与自复制样本分析
- [`05-crypto-unpack/05-high-entropy-compression-vs-crypto-routing.md`](05-crypto-unpack/05-high-entropy-compression-vs-crypto-routing.md) — 高熵数据鉴别与无头解压/解密自动化路由手册
- [`05-crypto-unpack/06-modern-pe-unmapping-and-dump-reconstruction.md`](05-crypto-unpack/06-modern-pe-unmapping-and-dump-reconstruction.md) — 现代 Windows PE 内存解映射（Unmapper）与内存转储与还原解包重构实战指南
- [`05-crypto-unpack/07-modern-virtual-machine-devirtualization-mogvmp-llvm.md`](05-crypto-unpack/07-modern-virtual-machine-devirtualization-mogvmp-llvm.md) — 现代代码虚拟化壳（VMP 3.x）去虚拟化前沿实战：基于 Remill 提升与 LLVM 优化遍
- [`05-crypto-unpack/08-selfhealing-emulation-vmp-handler-extraction.md`](05-crypto-unpack/08-selfhealing-emulation-vmp-handler-extraction.md) — 自愈式仿真：无真机提取 VMP Handler 表与字节码（PE x64）
- [`05-crypto-unpack/09-runtime-vm-detection-generic.md`](05-crypto-unpack/09-runtime-vm-detection-generic.md) — 运行时 VM 探测：跨实现通用的虚拟机识别与验证（零真机）
- [`05-crypto-unpack/10-nested-vm-matryoshka-reverse-and-defeat.md`](05-crypto-unpack/10-nested-vm-matryoshka-reverse-and-defeat.md) — 多层嵌套虚拟机（Matryoshka-VM）逆向与破译方法论：从分发层逐级剥离到最内层代数约束求解
- [`05-crypto-unpack/11-two-ring-vow-decoy-corridor-and-dual-verifier-reverse.md`](05-crypto-unpack/11-two-ring-vow-decoy-corridor-and-dual-verifier-reverse.md) — 双环互锁与欺骗走廊（two_ring_vow）：对抗诱导陷阱与确定性黄金输入发生器提取
- [`05-crypto-unpack/12-vault-nested-helix-aegis-packer-maze-and-vm-defeat.md`](05-crypto-unpack/12-vault-nested-helix-aegis-packer-maze-and-vm-defeat.md) — Aegis 加壳与双螺旋嵌套虚拟机（VAULT）：Reflective Dump、迷宫唯一解约束与双层 VM 破译
- [`05-crypto-unpack/vmp-architecture-generations.md`](05-crypto-unpack/vmp-architecture-generations.md) — 联网检索结果：VMP 验证技术与我的分析对照

### 06-ioc-extraction — IOC 提取（2）

- [`06-ioc-extraction/01-ioc-extraction.md`](06-ioc-extraction/01-ioc-extraction.md) — IOC 提取技巧
- [`06-ioc-extraction/02-persistence-startup-chain.md`](06-ioc-extraction/02-persistence-startup-chain.md) — 持久化与启动链 IOC 提取

### 07-yara-sigma — YARA/Sigma（1）

- [`07-yara-sigma/01-yara-rule-writing.md`](07-yara-sigma/01-yara-rule-writing.md) — YARA 规则编写（逆向视角）

### 08-patch — Patch（1）

- [`08-patch/01-code-patching.md`](08-patch/01-code-patching.md) — 代码 Patch 与字节修改

### 09-av-evasion — AI 检测签名分析与规避（1）

- [`09-av-evasion/01-ai-powered-evasion.md`](09-av-evasion/01-ai-powered-evasion.md) — AI 驱动免杀：Shellcode 处理 + Loader 编写

### 10-license-keygen — license-keygen（10）

- [`10-license-keygen/01-license-mechanism-classification.md`](10-license-keygen/01-license-mechanism-classification.md) — 许可证机制分类与攻击路径选择
- [`10-license-keygen/02-validation-function-location.md`](10-license-keygen/02-validation-function-location.md) — 许可证校验函数定位
- [`10-license-keygen/03-key-algorithm-recovery.md`](10-license-keygen/03-key-algorithm-recovery.md) — 注册码算法还原与 keygen 复现
- [`10-license-keygen/04-signature-chain-pubkey-swap.md`](10-license-keygen/04-signature-chain-pubkey-swap.md) — 签名链校验与公钥替换攻击
- [`10-license-keygen/05-keygen-frida-verification-loop.md`](10-license-keygen/05-keygen-frida-verification-loop.md) — keygen 实机验证闭环（Frida 进程内替换）
- [`10-license-keygen/06-cloud-license-frida-hook.md`](10-license-keygen/06-cloud-license-frida-hook.md) — 云端授权识别与 Frida hook 替代路径
- [`10-license-keygen/07-self-referencing-signature-convergence.md`](10-license-keygen/07-self-referencing-signature-convergence.md) — 自引用签名嵌入与单步迭代收敛
- [`10-license-keygen/08-cross-version-aob-migration.md`](10-license-keygen/08-cross-version-aob-migration.md) — 跨版本 AOB 特征码迁移与双态修补
- [`10-license-keygen/09-runtime-callstack-locating.md`](10-license-keygen/09-runtime-callstack-locating.md) — 运行时调用栈定位法（静态 xref 断裂时的破局）
- [`10-license-keygen/10-multiversion-signature-narrowing.md`](10-license-keygen/10-multiversion-signature-narrowing.md) — 多版本特征码收窄与数据段填充漂移陷阱
