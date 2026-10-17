# 2026-10-16 VAULT-Nested-Helix 攻坚手记：Aegis 壳内存转储、迷宫唯一解证明与双螺旋 VM 破译

## 场景分类

二进制逆向 / 自研加壳脱壳 / 迷宫约束求解 / 双螺旋嵌套虚拟机 / Unicorn 仿真求根

## 目标概述

对 `windows/vmp-crackmes/VAULT-Nested-Helix/VAULT.exe` 执行全流程逆向破译：
攻破其外层 Aegis 保护壳（Zero IAT / PEB 动态 API 解析 / ChaCha20 + LZSS 载荷加密），
利用 KB 06 解映射工具无损重构核心载荷 PE，
通过图搜索算法证明 8x8 迷宫寻路门禁的 16 步唯一解，
分析内嵌双螺旋嵌套虚拟机（.nexus 外层调度 + .helix 内层核验），
使用 Unicorn 切片仿真逆向求解唯一合法 Serial 并在实机释放 Flag。

## Scope 摘要（脱敏）

- auth_basis: 授权沙箱样本（CTF/Crackme 评估目标，`windows/vmp-crackmes/VAULT-Nested-Helix/`）
- network_profile: offline（全程离线，无网络交互）
- asset_types: ["PE32+ x86-64 可执行文件", "Aegis Packer 自研加壳", "双螺旋嵌套虚拟机 (Two-Tier VM)"]

## 角色

- lead_role: lead
- specialists: ["逆向分析副官", "Headless 仿真工程师"]

## 完整执行链路

### 阶段一：Aegis 保护壳逆向与无损载荷转储

1. **导入表分析**：发现样本导入表为空（Zero IAT），通过 `start` 函数反编译定位其 PEB 导出表遍历例程。
2. **API 还原**：通过 FNV-1a 哈希还原出 25 个敏感系统调用，发现其集成了 5 重反调试累加器（`BeingDebugged`, `IsDebuggerPresent`, `CheckRemoteDebuggerPresent`, `GetThreadContext` 硬件断点探测, `rdtscp` 耗时差）。
3. **载荷转储与重构**：
   - 壳内通过 `.text` 节区哈希与 HMAC 派生出 ChaCha20 密钥，解密并 LZSS 解压出 24,576 字节的 PE32+ 核心载荷；
   - 借助运行时内存转储捕获该载荷，并使用知识库工具 `pe_unmapper_tool.py` 成功修复解映射，生成可供反编译器完整分析的 `unmapped_vault.exe`。

### 阶段二：8x8 迷宫路径唯一性证明

1. 反编译核心函数 `sub_1C0003510`，捕获 8x8 网格寻路算法：
   - 输入要求为 16 字节大写字母与数字；
   - 每个字符的 `serial[i] & 3` 决定移动方向（0:上, 1:右, 2:下, 3:左）；
   - 必须从 $(0,0)$ 出发恰好用完 16 步到达终点 $(7,7)$。
2. **图搜索证明**：
   - 编写 DFS 脚本穷举全图，证明符合条件的 16 步路径**在数学上具有全局唯一解**：
     `[1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 1]`；
   - 这一发现直接锁定了全部 16 字符的最低 2 位，将每个字符的候选集从 36 压缩到 8~10 个！

### 阶段三：双螺旋虚拟机逆向与约束求解

1. **双层 VM 架构解析**：
   - **Tier-1 外层调度器（.nexus）**：350 字节字节码，21 项 Syscall；
   - **Tier-2 内层核验机（.helix）**：101 字节字节码，负责具体字符约束。
2. **Unicorn 切片求根**：
   - 外层调度器在 `Syscall 17` 中逐字节对内层核验机发起 16 轮约束判定；
   - 使用 Unicorn 配置轻量上下文，对 16 个位置的候选字符进行极速求根；
   - 14 个位置直接锁定唯一解；位置 5（`'Q'`）与位置 13（`'Z'`）通过结合 Flag 解密流的纯可见 ASCII 约束完成收敛。
3. **最终密钥与 Flag**：
   - **Serial**: `999U-EQMV-26JV-JZG5`
   - **Flag**: `FLAG{NESTED-HELIX-BYTE-BY-BYTE-WIPE-7K}`

### 阶段四：真实环境验证

- 在 Wine 环境下通过命令行直传验证：
  `wine VAULT.exe 999U-EQMV-26JV-JZG5`
- 成功捕获绿色 `UNLOCKED` 回显及 Flag 明文，进程退出码为 `0`！

---

## 关键技术突破与经验教训

1. **解映射工具的高效联动**：
   - 本次直接复用了此前在知识库中沉淀的 `pe_unmapper_tool.py`，瞬间解决了内存 Dump 载荷的节区偏移与对齐错位问题，使 IDA 反编译毫无阻碍。
2. **迷宫路径的代数剪枝威力**：
   - 当遇到“复杂逻辑前置了几何/迷宫约束”时，先对前置约束进行图搜索求解；一旦证明路径具有唯一性，往往能大幅削减后续搜索空间（本例中直接将搜索空间削减了 $4^{16}$ 倍）。

---

## 交付物清单

1. **技术方法论文档**：`pe-reverse/techniques/05-crypto-unpack/12-vault-nested-helix-aegis-packer-maze-and-vm-defeat.md`
2. **自动化破译脚本**：`pe-reverse/techniques/05-crypto-unpack/solve_vault.py`
3. **本地复现验证脚本**：`/root/逆向测试/work/vault-helix/scripts/solve_vault.py`
4. **验证依据 (Evidence)**：`reproduced`
