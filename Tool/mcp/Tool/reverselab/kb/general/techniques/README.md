# general 技术库目录

> 本目录由 `kb_maintain.py --sync-index` 自动生成（2026-10-17）
> 共 5 类 / 17 篇

## 完整目录

### 01-kernel — kernel（5）

- [`01-kernel/01-page-cache-write-family.md`](01-kernel/01-page-cache-write-family.md) — Linux 内核 Page-Cache 写入家族：Copy Fail / Dirty Frag / Fragnesia
- [`01-kernel/02-slab-cross-cache.md`](01-kernel/02-slab-cross-cache.md) — Slab 跨缓存释放：KFENCE 精确大小报告导致 SKB head 释放到错误缓存
- [`01-kernel/03-mm-null-ptrace-bypass.md`](01-kernel/03-mm-null-ptrace-bypass.md) — 内核 FD Theft：mm-NULL ptrace check bypass
- [`01-kernel/04-cifswitch-nss-privesc.md`](01-kernel/04-cifswitch-nss-privesc.md) — CIFSwitch：cifs.spnego 身份混淆 → root 权限 NSS 加载
- [`01-kernel/05-pintheft-io-uring-page-cache.md`](01-kernel/05-pintheft-io-uring-page-cache.md) — RDS zcopy double-free + io_uring dangling struct page*：PinTheft 内核 LPE

### cheating — cheating（5）

- [`cheating/01-memory-hacking.md`](cheating/01-memory-hacking.md) — 内存搜索与修改
- [`cheating/02-packet-interception.md`](cheating/02-packet-interception.md) — 封包拦截与修改
- [`cheating/03-esp-wallhack-rendering.md`](cheating/03-esp-wallhack-rendering.md) — 透视/ESP 渲染技术
- [`cheating/04-anti-cheat-bypass.md`](cheating/04-anti-cheat-bypass.md) — 反作弊系统绕过
- [`cheating/05-speedhack-time-manipulation.md`](cheating/05-speedhack-time-manipulation.md) — 加速/时间操控

### crypto — crypto（3）

- [`crypto/01-algorithm-identification.md`](crypto/01-algorithm-identification.md) — 算法盲识别：从字节特征反推加密/哈希/压缩算法
- [`crypto/02-custom-obfuscation-reverse.md`](crypto/02-custom-obfuscation-reverse.md) — 自定义混淆/加密还原方法论
- [`crypto/03-prng-randomness-cracking.md`](crypto/03-prng-randomness-cracking.md) — 伪随机数生成器(PRNG)破解 — 从输出恢复内部状态与种子

### methodology — methodology（2）

- [`methodology/01-reverse-checklist-first-30-min.md`](methodology/01-reverse-checklist-first-30-min.md) — 拿到样本的前30分钟清单
- [`methodology/02-toolchain-decision-tree.md`](methodology/02-toolchain-decision-tree.md) — 按信号选工具决策树

### protocol — protocol（2）

- [`protocol/01-unknown-protocol-reverse.md`](protocol/01-unknown-protocol-reverse.md) — 未知协议逆向方法论
- [`protocol/02-protobuf-flatbuffers-reverse.md`](protocol/02-protobuf-flatbuffers-reverse.md) — Protobuf / FlatBuffers 无 Schema 逆向
