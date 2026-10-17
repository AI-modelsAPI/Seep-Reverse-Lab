#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
angr_solve_template.py — 针对二进制复杂校验分支的 Angr 符号执行通用求解模板
"""

import sys, os, argparse

def solve_binary(binary_path, find_addr, avoid_addrs, input_len=32, is_stdin=True):
    try:
        import angr, claripy
    except ImportError:
        print("[-] 需要安装 angr 框架: pip install angr")
        sys.exit(1)

    print(f"[*] 加载二进制: {binary_path}")
    project = angr.Project(binary_path, auto_load_libs=False)

    sym_input = claripy.BVS("sym_input", input_len * 8)

    if is_stdin:
        # stdin 模式
        state = project.factory.full_init_state(
            stdin=sym_input,
            add_options={angr.options.LAZY_SOLVES}
        )
        # 添加只包含可打印 ASCII 字符的约束 (提升求解速度)
        for byte in sym_input.chop(8):
            state.solver.add(byte >= 0x20)
            state.solver.add(byte <= 0x7E)
    else:
        # CLI 参数模式
        state = project.factory.entry_state(args=[binary_path, sym_input])

    sm = project.factory.simulation_manager(state)
    print(f"[*] 开始探索路径 -> 目标: 0x{find_addr:x}, 规避: {[hex(a) for a in avoid_addrs]}")
    sm.explore(find=find_addr, avoid=avoid_addrs)

    if sm.found:
        found_state = sm.found[0]
        solution = found_state.solver.eval(sym_input, cast_to=bytes)
        print(f"[🎉] 成功求解目标输入: {solution!r}")
        print(f"     纯文本: {solution.decode('latin1', errors='ignore')}")
        return solution
    else:
        print("[-] 未能探索到目标分支，请检查 find/avoid 地址或是否存在反调试阻断。")
        return None

def main():
    p = argparse.ArgumentParser(description="Angr 符号执行通用约束求解工具")
    p.add_argument("binary", help="目标二进制文件路径")
    p.add_argument("--find", required=True, type=lambda x: int(x, 16), help="校验成功分支虚拟地址 (十六进制，如 0x401122)")
    p.add_argument("--avoid", nargs="*", type=lambda x: int(x, 16), default=[], help="校验失败分支地址列表 (十六进制，如 0x401133)")
    p.add_argument("--len", type=int, default=32, help="符号变量长度 (默认 32 字节)")
    p.add_argument("--argv", action="store_true", help="使用 argv 参数传参模式（默认为 stdin）")
    args = p.parse_args()

    solve_binary(args.binary, args.find, args.avoid, input_len=args.len, is_stdin=not args.argv)

if __name__ == "__main__":
    main()
