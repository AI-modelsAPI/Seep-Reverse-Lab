# 2026-10-16 Matryoshka-VM 5 层嵌套虚拟机逆向攻坚：层级剥离、约束求导与 Flag 提取

## 场景分类

二进制逆向 / 自定义代码虚拟化 / 多层嵌套 VM / 代数约束求解 / 无真机仿真核验

## 目标概述

对 `windows/vmp-crackmes/Matryoshka-VM/crackme.exe`（声称五层嵌套虚拟机架构）执行完整逆向分析与破译：
在 Linux Headless 环境下，通过反编译与反汇编逐层还原 VM 拓扑结构，提取分发逻辑与字节码解密链，
绕过蛮力搜索陷阱，逆向最内层核验逻辑并求解使全部虚拟机判定一致通过的正确 Flag。

## Scope 摘要（脱敏）

- auth_basis: 授权沙箱样本（CTF/Crackme 评估目标，`windows/vmp-crackmes/Matryoshka-VM/`）
- network_profile: offline（全程离线，无网络交互）
- asset_types: ["PE32+ x86-64 可执行文件", "自定义多层嵌套虚拟机 (5-Layer Nested VM)"]

## 角色

- lead_role: lead
- specialists: ["逆向分析副官", "Headless 仿真工程师"]

## 完整执行链路

### 阶段一：样本侦察与运行时行为画像

1. 基本信息确认：PE32+ for MS Windows x86-64，带控制台交互。
2. 运行提示定位：输出 "Crackme - five nested virtual machines", "Goal: find the password.", "Enter password: "。
3. 关键判定观察：
   - 错误时输出 `[-] Wrong password.`；
   - 成功时输出 `[+] Correct! All five virtual machines agree. You found the password.`。
4. 初始输入过滤规则：输入长度限制在 511 字节以内，且不能含有 `NUL` 字符，否则直接退出。

### 阶段二：拓扑拆解与逐层 VM 剥离

通过 IDA Pro 9.5 批处理反编译与深入跟踪定位主函数 `sub_140008B80`，还原出惊人一致的五层套娃解释器结构：

1. **VM-1（外层调度状态机）**：
   - 字节码 1720 字节（解密自 `unk_14000CF40`），采用 LCG（$1103515245 \times x + 12345$）密钥流解密。
   - 分发通过 `byte_14000C220` 查表映射，主路径中 `Case 12` 触发 VM-2。
2. **VM-2（寄存器机）**：
   - 字节码 974 字节（解密自 `unk_14000CB60`），采用 32 位 Xorshift 伪随机序列解密。
   - `Case 9` 触发下一层解密并调用 VM-3。
3. **VM-3（栈式虚拟机）**：
   - 字节码 608 字节（解密自 `unk_14000C8E0`），采用 128 位 SSE 矢量交错指令（`_mm_unpacklo/hi`）展开。
   - `Case 9` 触发二次解密并调用 VM-4。
4. **VM-4（寄存器混淆机）**：
   - 字节码 1075 字节（解密自 `unk_14000C440`），采用 SSE S-Box 打乱。
   - `Case 9` 触发解密并调用 VM-5。
5. **VM-5（核心核验虚拟机）**：
   - 字节码 269 字节，由 `byte_14000C320` 与 `byte_14000C207` 仿射变换解码。
   - 包含了真实的校验规则。

### 阶段三：避开蛮力搜索陷阱与精准代数求导

1. **早期弯路**：
   - 尝试直接在外层通过求解器跑 `cksum(v2, 0xffffffff) == 0x16607cc9`，发现全空间 $2^{32}$ 单线程迭代计算极度耗时，导致进程超时被终止。
2. **战术重定向**：
   - 深入 VM-5 虚拟指令集，发现仅有 9 个操作码。
   - 关键操作码 `0x88 0x18`：明确要求输入长度**必须严格等于 24 字节**。
   - 关键操作码 `0x66`：为单字节相等断言。
   - **发现致命密码学缺陷**：VM-5 对 24 个输入字符依次独立计算代数表达式并分别断言，字符之间没有任何扩散（Diffusion）或雪崩关联。
3. **毫秒级求导**：
   - 将求解复杂度由指数级彻底降维为 $24 \times 256 = 6144$ 次计算。
   - 编写 `matryoshka_vm_solver.py` 对 24 组单字节代数方程求根，瞬间求出全部 24 字节明文。

### 阶段四：成果落地与双重环境验证

1. **破译结果**：
   $$\text{Password} = \mathbf{WL7s3EU9i!bN!264!5qhx\_3q}$$
2. **Wine 环境实机核验**：
   - `printf "WL7s3EU9i!bN!264!5qhx_3q\n" | wine crackme.exe`
   - 成功捕获回显：`[+] Correct! All five virtual machines agree. You found the password.`。
3. **Linux Headless (Unicorn) 仿真核验**：
   - 使用自主编写的 `pe_loader_v2.py` 执行，在不依赖 Windows GUI 与任何动态调试器的纯模拟环境下，100% 成功触发通关回显。

---

## 关键技术突破与经验教训

1. **不要被表象的多层混淆迷惑**：
   - 样本虽然套了 5 层虚拟机，但前 4 层实际上是“确定性的无条件解密”（Deterministic Unconditional Decryption）。其解密密钥与输入无关，本质上只是代码展开器（Stager/Unpacker），真正的攻击面完全收敛在最内层 VM。
2. **蛮力搜索要设立熔断计时**：
   - 当单次探索计算量达到 $2^{32}$ 且超时被杀时，必须立即停止“盲目加大算力”，转而向底层深入逆向，寻找约束降维的可能。
3. **单字节断言是虚拟化保护的大忌**：
   - 缺乏密码学扩散与块混合（Block Mixing）的代数运算，即使套了 100 层虚拟机，也能被单字符爆破逐个击破。

---

## 交付物清单

1. **技术方法论文档**：`pe-reverse/techniques/05-crypto-unpack/10-nested-vm-matryoshka-reverse-and-defeat.md`
2. **一键破译工具**：`pe-reverse/techniques/05-crypto-unpack/matryoshka_vm_solver.py`
3. **本地复现验证脚本**：`/root/逆向测试/work/vmp-dump/scripts/matryoshka_vm_solver.py`
4. **验证依据 (Evidence)**：`reproduced`
