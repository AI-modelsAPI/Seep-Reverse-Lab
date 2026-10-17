---
id: "general/crypto/02-angr-symbolic-execution-solver"
title: "基于 Angr 符号执行的混淆二进制与复杂约束自动求解"
title_en: "Automated Obfuscated Binary Solving via Angr Symbolic Execution"
summary: >
  针对通过人工静态反编译面对上百层位运算、加减异或混合（OLLVM MBA 混淆）或多约束矩阵校验
  难以手算逆向的问题，建立基于 Angr 的自动化求解闭环。涵盖基于 entry_state / blank_state
  的符号输入注入、find / avoid 路径探索、局部 API 桩注入（防止状态爆炸）与 Z3 解向量提取。
summary_en: >
  Production workflow utilizing the Angr symbolic execution engine to bypass mixed boolean-arithmetic (MBA)
  and solve multi-constraint verification logic. Covers symbolic memory injection, explore find/avoid paths,
  function call hooking to prevent state explosions, and extracting solutions via SMT solvers.
board: "general"
category: "crypto"
signals:
  - "angr"
  - "claripy"
  - "symbolic execution"
  - "MBA 混淆"
  - "状态爆炸"
  - "solve license"
  - "SMT solver"
  - "Z3"
mcp_tools:
  - "kb_router"
difficulty: "advanced"
tags:
  - "crypto"
  - "angr"
  - "reverse"
  - "symbolic"
  - "z3"
evidence: "verified"
validated_by: "实测于官方 angr-examples 与 FLARE-On 经典题目"
language: "zh-CN"
last_updated: "2026-10-15"
related_articles:
  - "pe-reverse/05-crypto-unpack/05-high-entropy-compression-vs-crypto-routing"
---
# 基于 Angr 符号执行的混淆二进制与复杂约束自动求解

当在逆向分析中遇到：
1. 校验函数内部展开了数十个基本块，充斥着 OLLVM MBA（Mixed Boolean-Arithmetic）花指令（如 `(x ^ y) + 2*(x & y)`）；
2. 校验算法是不可逆的单向非线性变换，但输入长度有限（如 16~64 字节密钥）；
3. 手写逆运算数学推导过于耗时且容易出错。

**最优策略**：**放弃手算，使用 Angr 符号执行引擎！** 将输入标记为符号向量（Symbolic BitVector），设定“校验成功分支地址”为目标，交给 SMT 求解器（Z3）自动解方程。

---

## 一、 快速作战三板斧

### 1. 命令行参数型（CLI Input）极速求解
```python
import angr, claripy

p = angr.Project("./target_binary", auto_load_libs=False)
# 构造符号输入（例如 32 字节）
sym_arg = claripy.BVS("flag", 32 * 8)
state = p.factory.entry_state(args=["./target_binary", sym_arg])

sm = p.factory.simulation_manager(state)
# find: "Success" / "Correct" 的汇编地址; avoid: "Wrong" / "Failed" 的地址
sm.explore(find=0x401234, avoid=0x401250)

if sm.found:
    solution = sm.found[0].solver.eval(sym_arg, cast_to=bytes)
    print(f"[+] 自动求解成功: {solution}")
```

### 2. 标准输入（stdin）或局部内存注入（Blank State）
如果目标程序是在运行时通过 `scanf` 或从文件读取输入：
- 在 `main` 或校验函数入口建立 `blank_state(addr=0x401000)`；
- 直接在内存指针处绑定 `claripy.BVS`；
- 利用 `p.hook(api_addr, dummy_func, length=5)` 绕过无用的外部系统调用，防止**状态爆炸（State Explosion）**。

---

## 二、 自动化工装模板：`angr_solve_template.py`

同目录下附带通用参数化脚本，直接替换地址即可开工求解：

```bash
python3 angr_solve_template.py ./crackme --find 0x4011aa --avoid 0x4011cc --len 24
```
