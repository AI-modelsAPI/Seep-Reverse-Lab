# 2026-10-16 two_ring_vow (两枚魔戒) 攻坚手记：防诱导走廊识破、双环互锁拆解与确定性状态机提取

## 场景分类

二进制逆向 / 对抗诱导陷阱 / 双环互锁 / 确定性状态机提取 / Unicorn 切片仿真

## 目标概述

对 `windows/vmp-crackmes/LvArshu-Flag/two_ring_vow.exe`（纪念日定制双环 Crackme）执行全流程逆向审计：
识破其布置的虚假通关提示（`[SYNTHETIC SUCCESS]` / `[FAKE SUCCESS]`）与伪 Token 矩阵（`AI{...}` / `SEAL{...}`），
拆解其四重独立状态机（哈希机、栈式解释器、64 位散列、非线性置换）同态比对架构，
定位底层的确定性黄金标准发生器（`sub_1400019A0`），用 Unicorn 切片仿真瞬间提取真凭据并达成 Exit Code 0 闭环。

## Scope 摘要（脱敏）

- auth_basis: 授权沙箱样本（CTF/Crackme 评估目标，`windows/vmp-crackmes/LvArshu-Flag/`）
- network_profile: offline（全程离线，无网络交互）
- asset_types: ["PE32+ x86-64 可执行文件", "MinGW mcfgthread 模型", "双环互锁防逆向架构"]

## 角色

- lead_role: lead
- specialists: ["逆向分析副官", "Headless 仿真工程师"]

## 完整执行链路

### 阶段一：资产初探与反调试/诱导侦察

1. 基础信息：PE32+ x86-64，MinGW-w64 + `mcfgthread` 线程模型，依赖 `libmcfgthread-2.dll`。
2. 提示分析：
   - 提示 *“Every message printed by the verifier is untrusted data”*；
   - 错误输入时输出 `> The machine remembers every shortcut you took.` 并随机构造 `REHEARSAL TOKEN: SEAL{...}`。
3. 反调试侦察：
   - 发现导入了 `IsDebuggerPresent`、`CheckRemoteDebuggerPresent`、`QueryPerformanceCounter`。
   - 函数 `sub_140002420` 包含高频 QPC 时钟差值探测，判定是否存在调试器挂载。

### 阶段二：反编译与双环控制流拆解

1. 定位主输入入口 `sub_1400C2640`：
   - 读取输入行并剔除末尾 `\r`；
   - 调用核心核验器 `sub_140003290`；
   - 以其返回值第一字节 `v41[0] ^ 1` 作为进程最终退出码。
2. 深入核心核验器 `sub_140003290`：
   - **门禁 1**：输入长度必须为 15 字节（`v23 == 15`），且全在 `[0x20, 0x7E]` 之间。
   - **诱导分支**：若长度不符，程序并不报错，而是跳转生成带有 `[SYNTHETIC SUCCESS]` 或 `[FAKE SUCCESS]` 的伪回显，专门诱捕符号执行与字符串断点。
   - **真放行分支**：
     ```c
     if ( v114 == -339837343 && Srcb && v48 != 0 && v162 && v49 != 0 && v55 ) {
         *(_BYTE *)a1 = 1; // 仅此处将 success 置为 1
         sub_1400027A0(a1 + 8); // 动态解密释放通关字符串
         return a1;
     }
     ```

### 阶段三：破局——定位确定性黄金标准发生器

1. 四重核验机特征：
   - `sub_140001DC0` (Hash Machine)
   - `sub_140001F90` (VM Stack Machine)
   - `sub_140002210` (64-bit Rolling Hash)
   - `sub_140001B90` (1024-Round State Permutation)
2. **关键发现**：每个核验机都以“参考流”和“用户流”做同态对比，而参考流的唯一输入是函数 **`sub_1400019A0(index)`**。
3. 审查 `sub_1400019A0`：完全由内置静态查表数组与参数 `a1 \in [0, 14]` 决定，是一个**自包含的确定性黄金输入发生器**。

### 阶段四：Unicorn 切片执行与验证

1. 编写 Unicorn 切片执行脚本，直接映射 PE 节区，配置独立调用栈；
2. 循环传参 `RCX = 0 .. 14` 执行 `sub_1400019A0`，提取 RAX 返回值；
3. 输出结果：
   $$[76, 118, 89, 48, 117, 65, 114, 115, 104, 117, 49, 51, 48, 40, 84] \Rightarrow \mathbf{LvY0uArshu130(T}$$
4. 真实交互执行验证：
   - `printf "LvY0uArshu130(T\n" | wine two_ring_vow.exe`
   - 成功捕获放行文本：`> You found it! Submit the flag.`，进程退出码为 `0`！

---

## 关键技术突破与经验教训

1. **“所有打印信息均为不可信数据”的心智建设**：
   - 面对复杂的现代逆向题目，程序在控制台打印的 `SUCCESS`、`CORRECT`、`FLAG{...}` 往往是防御方布置的重度蜜罐；
   - 绝不依赖字符串作为断点目标，紧盯函数真实返回值、内存状态置位以及底层 Exit Code 才是穿透迷雾的唯一路径。
2. **同态双调用的反客为主**：
   - 许多程序自以为“四重复杂数学变换”牢不可破，但如果在同一个二进制内既当“裁判”又当“出题人”（用同一份代码产生参考答案），逆向人员就可以直接把它的出题模块当作 Oracle 提取明文，实现零代数推导秒杀。

---

## 交付物清单

1. **技术方法论文档**：`pe-reverse/techniques/05-crypto-unpack/11-two-ring-vow-decoy-corridor-and-dual-verifier-reverse.md`
2. **一键自动化提取脚本**：`pe-reverse/techniques/05-crypto-unpack/solve_two_ring_vow.py`
3. **本地复现验证脚本**：`/root/逆向测试/work/two-ring-vow/scripts/solve_two_ring_vow.py`
4. **验证依据 (Evidence)**：`reproduced`
