#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
headless_slice_emulator_tool.py — 无环境跨架构通用机器码切片仿真工装
====================================================================
作用：在无 Android 手机/模拟器、无 Windows 桌面沙箱的情况下，
      直接以切片方式运行并验证任意提取的 x86 / x64 / ARM64 算法函数机器码。
"""

import sys, struct, argparse
from unicorn import *
from unicorn.x86_const import *
from unicorn.arm64_const import *

DEFAULT_BASE = 0x400000
DEFAULT_STACK = 0x700000
STACK_SIZE = 0x100000
STOP_ADDRESS = 0x800000  # 哨兵返回地址

def emulate_x64(machine_code, args_list=None):
    mu = Uc(UC_ARCH_X86, UC_MODE_64)
    mu.mem_map(DEFAULT_BASE, 0x100000, UC_PROT_ALL)
    mu.mem_map(DEFAULT_STACK, STACK_SIZE, UC_PROT_ALL)
    mu.mem_map(STOP_ADDRESS, 0x1000, UC_PROT_ALL)

    mu.mem_write(DEFAULT_BASE, machine_code)
    # 在哨兵页写入一条 hlt 停机指令 (0xf4)
    mu.mem_write(STOP_ADDRESS, b"\xf4")

    # 栈顶压入返回哨兵地址
    rsp = DEFAULT_STACK + STACK_SIZE - 0x1000
    mu.mem_write(rsp, struct.pack("<Q", STOP_ADDRESS))
    mu.reg_write(UC_X86_REG_RSP, rsp)

    # Linux x64 ABI 参数注入: rdi, rsi, rdx, rcx, r8, r9
    arg_regs = [UC_X86_REG_RDI, UC_X86_REG_RSI, UC_X86_REG_RDX, UC_X86_REG_RCX, UC_X86_REG_R8, UC_X86_REG_R9]
    if args_list:
        for idx, val in enumerate(args_list[:6]):
            mu.reg_write(arg_regs[idx], val)

    print(f"[*] [x64 仿真] 起始 PC: 0x{DEFAULT_BASE:x}, 字节长度: {len(machine_code)}")
    try:
        mu.emu_start(DEFAULT_BASE, STOP_ADDRESS)
    except UcError:
        pass

    rax = mu.reg_read(UC_X86_REG_RAX)
    print(f"[🎉] 仿真执行完毕！返回值 RAX: 0x{rax:x} ({rax})")
    return rax

def emulate_arm64(machine_code, args_list=None):
    mu = Uc(UC_ARCH_ARM64, UC_MODE_ARM)
    mu.mem_map(DEFAULT_BASE, 0x100000, UC_PROT_ALL)
    mu.mem_map(DEFAULT_STACK, STACK_SIZE, UC_PROT_ALL)
    mu.mem_map(STOP_ADDRESS, 0x1000, UC_PROT_ALL)

    mu.mem_write(DEFAULT_BASE, machine_code)
    # 链接寄存器 LR (X30) 设置为哨兵返回地址
    mu.reg_write(UC_ARM64_REG_X30, STOP_ADDRESS)

    sp = DEFAULT_STACK + STACK_SIZE - 0x1000
    mu.reg_write(UC_ARM64_REG_SP, sp)

    # ARM64 ABI 参数注入: x0 ~ x7
    arg_regs = [
        UC_ARM64_REG_X0, UC_ARM64_REG_X1, UC_ARM64_REG_X2, UC_ARM64_REG_X3,
        UC_ARM64_REG_X4, UC_ARM64_REG_X5, UC_ARM64_REG_X6, UC_ARM64_REG_X7
    ]
    if args_list:
        for idx, val in enumerate(args_list[:8]):
            mu.reg_write(arg_regs[idx], val)

    print(f"[*] [ARM64 仿真] 起始 PC: 0x{DEFAULT_BASE:x}, 字节长度: {len(machine_code)}")
    try:
        mu.emu_start(DEFAULT_BASE, STOP_ADDRESS)
    except UcError:
        pass

    x0 = mu.reg_read(UC_ARM64_REG_X0)
    print(f"[🎉] 仿真执行完毕！返回值 X0: 0x{x0:x} ({x0})")
    return x0

def main():
    p = argparse.ArgumentParser(description="跨架构无环境机器码切片仿真工装")
    p.add_argument("--arch", choices=["x64", "arm64"], default="x64", help="目标架构 (x64 或 arm64)")
    p.add_argument("--hex", required=True, help="待仿真的机器码 Hex 字符串 (例如 '4883ec08b82a0000004883c408c3')")
    p.add_argument("--args", nargs="*", type=lambda x: int(x, 16) if x.startswith("0x") else int(x), default=[], help="传入的整型/指针参数列表")
    cmd_args = p.parse_args()

    clean_hex = cmd_args.hex.replace(" ", "").replace("\\x", "").strip()
    raw_code = bytes.fromhex(clean_hex)

    if cmd_args.arch == "x64":
        emulate_x64(raw_code, cmd_args.args)
    elif cmd_args.arch == "arm64":
        emulate_arm64(raw_code, cmd_args.args)

if __name__ == "__main__":
    main()
