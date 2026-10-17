#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mba_simplifier_tool.py — 混合布尔算术 (MBA) 混淆表达式自动模式化简器
===================================================================
作用：将 OLLVM / 虚拟化壳生成的复杂位运算/加减混合表达式，自动化简为最简原生算式，
      并利用 Z3 SMT 求解器进行严格的形式化数学等价证明。
"""

import sys, argparse
from z3 import BitVec, Solver, unsat

# 经典规则库字典 (Pattern -> Simplified)
MBA_CANONICAL_RULES = [
    ("(x ^ y) + 2 * (x & y)", "x + y"),
    ("(x | y) + (x & y)", "x + y"),
    ("(x | y) - (x & y)", "x ^ y"),
    ("(x + y) - 2 * (x & y)", "x ^ y"),
    ("(x & ~y) | (~x & y)", "x ^ y"),
    ("(x ^ ~y) + 2 * (x | ~y) + 1", "x - y"),
    ("(x ^ y) + 2 * (~x & y) + 1", "y - x"),
    ("~x + 1", "-x")
]

def verify_equivalence_z3(expr_str_a, expr_str_b, bit_width=32):
    """使用 Z3 验证两段算式在整个定义域内是否恒等 (形式化证明)"""
    x = BitVec('x', bit_width)
    y = BitVec('y', bit_width)
    
    # 构造安全 eval 命名空间，处理位运算符
    ns = {
        'x': x, 'y': y,
        'BitVec': BitVec
    }

    try:
        val_a = eval(expr_str_a, {"__builtins__": None}, ns)
        val_b = eval(expr_str_b, {"__builtins__": None}, ns)
    except Exception as e:
        return False, f"表达式解析失败: {e}"

    s = Solver()
    s.add(val_a != val_b)

    if s.check() == unsat:
        return True, "Z3 形式化验证通过 (定义域内 100% 恒等)"
    else:
        return False, "不恒等"

def simplify_mba(raw_expr):
    print(f"[*] 分析输入 MBA 表达式: {raw_expr}")
    
    cleaned = raw_expr.replace(" ", "")
    
    # 1. 尝试匹配经典库
    matched_candidates = [
        "x + y", "x - y", "y - x", "x ^ y", "x & y", "x | y",
        "-(x ^ y)", "~(x & y)", "-x", "-y"
    ]
    
    for cand in matched_candidates:
        ok, msg = verify_equivalence_z3(raw_expr, cand)
        if ok:
            print(f"[🎉] 成功命中并化简！")
            print(f"     原始表达式: {raw_expr}")
            print(f"     化简结果  : {cand}")
            print(f"     形式化证明: {msg}")
            return cand

    print("[-] 未能化简为单一经典初等算式，表达式可能包含多变量或深层嵌套。")
    return None

def main():
    p = argparse.ArgumentParser(description="混合布尔算术 (MBA) 混淆自动化简与 Z3 验证工装")
    p.add_argument("expr", help="需要化简的 Python 语法算术表达式 (例如: '(x ^ y) + 2 * (x & y)')")
    args = p.parse_args()

    simplify_mba(args.expr)

if __name__ == "__main__":
    main()
