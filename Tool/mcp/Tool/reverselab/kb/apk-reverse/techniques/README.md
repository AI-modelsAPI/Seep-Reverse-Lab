# apk-reverse 技术库目录

> 本目录由 `kb_maintain.py --sync-index` 自动生成（2026-10-18）
> 共 8 类 / 26 篇

## 完整目录

### 01-dex-java — DEX/Java（1）

- [`01-dex-java/01-smali-injection.md`](01-dex-java/01-smali-injection.md) — Smali 代码注入与 DEX 修改

### 02-native — Native（8）

- [`02-native/01-il2cpp-offset-discovery.md`](02-native/01-il2cpp-offset-discovery.md) — Unity IL2CPP 静态逆向与偏移发现
- [`02-native/02-pointer-chain-patterns.md`](02-native/02-pointer-chain-patterns.md) — 指针链遍历模式
- [`02-native/03-ue4-offset-hunting.md`](02-native/03-ue4-offset-hunting.md) — UE4 引擎游戏偏移发现
- [`02-native/04-kernel-procfs-driver.md`](02-native/04-kernel-procfs-driver.md) — Kernel Driver 注入：proc 节点读写
- [`02-native/05-virt-phys-memory.md`](02-native/05-virt-phys-memory.md) — 虚拟地址 → 物理地址转换
- [`02-native/06-jni-register-natives-tracing.md`](02-native/06-jni-register-natives-tracing.md) — JNI RegisterNatives 追踪与 Native 入口还原
- [`02-native/07-unidbg-native-emulation-pipeline.md`](02-native/07-unidbg-native-emulation-pipeline.md) — UniDbg 现代 Native 模拟执行与 JNI 自动化打桩手册
- [`02-native/08-flutter-dart-aot-reconstruction.md`](02-native/08-flutter-dart-aot-reconstruction.md) — Dart / Flutter AOT 逆向还原与 Snapshot 特征提取指南

### 03-manifest — Manifest（1）

- [`03-manifest/01-entry-point-tracing.md`](03-manifest/01-entry-point-tracing.md) — 入口点追踪与组件分析

### 04-crypto — 加密（2）

- [`04-crypto/01-game-encryption-patterns.md`](04-crypto/01-game-encryption-patterns.md) — 游戏数据加解密识别与绕过
- [`04-crypto/02-rc4-custom-crypto.md`](04-crypto/02-rc4-custom-crypto.md) — 自定义对称加密：RC4 与组合模式

### 05-network — 网络（3）

- [`05-network/01-game-protocol-hook.md`](05-network/01-game-protocol-hook.md) — 游戏协议 Hook 与封包分析
- [`05-network/02-license-verification-bypass.md`](05-network/02-license-verification-bypass.md) — 在线验证系统分析与绕过
- [`05-network/03-tls-pinning-unpinning.md`](05-network/03-tls-pinning-unpinning.md) — TLS Pinning 定位与 Unpinning

### 06-dynamic — 动态（3）

- [`06-dynamic/01-memory-rw-hook.md`](06-dynamic/01-memory-rw-hook.md) — 进程内存读写检测与 Hook
- [`06-dynamic/02-overlay-rendering-hook.md`](06-dynamic/02-overlay-rendering-hook.md) — Overlay 渲染与 ImGui 检测
- [`06-dynamic/03-touch-input-hook.md`](06-dynamic/03-touch-input-hook.md) — 触摸输入 Hook 与注入分析

### 07-packer — 壳（6）

- [`07-packer/01-obfuscation-detection.md`](07-packer/01-obfuscation-detection.md) — 编译期混淆检测与识别
- [`07-packer/02-modern-art-dex-dump-and-repair.md`](07-packer/02-modern-art-dex-dump-and-repair.md) — 现代 Android ART 内存 Dump DEX 修复与抽取壳还原手册
- [`07-packer/02-self-extracting-payload.md`](07-packer/02-self-extracting-payload.md) — 自解压 Payload 与脚本嵌入
- [`07-packer/03-vmp-dex2c-detection.md`](07-packer/03-vmp-dex2c-detection.md) — VMP/dex2c 加固识别与形态判定
- [`07-packer/04-vmp-dump-trace-recovery.md`](07-packer/04-vmp-dump-trace-recovery.md) — VMP 脱壳与语义还原（Dump/Trace/Recovery）
- [`07-packer/05-vmp-anti-debug-bypass.md`](07-packer/05-vmp-anti-debug-bypass.md) — Android 反调试检测与绕过（VMP 场景）

### 08-patch-repack — 补丁/重打包（2）

- [`08-patch-repack/01-so-injection-repack.md`](08-patch-repack/01-so-injection-repack.md) — Native SO 注入与 APK 重打包
- [`08-patch-repack/02-signature-integrity-bypass.md`](08-patch-repack/02-signature-integrity-bypass.md) — 签名与完整性检查绕过
