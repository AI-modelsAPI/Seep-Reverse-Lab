#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
r2pay_headless_emulator.py — r2pay-v1.0 现代加固 SO 无环境无设备模拟执行器
=============================================================================
适用场景：在无 Android 设备/无模拟器的情况下，纯软件模拟执行 x86_64 混淆 Native 库，
         打桩 JNIEnv，脱壳并直接验证算法返回值。
"""

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import sys, os, struct
from unicorn import *
from unicorn.x86_const import *
from elftools.elf.elffile import ELFFile

SO_PATH = "/tmp/r2pay1/unpacked/lib/x86_64/libnative-lib.so"
SO_BASE = 0x400000
STACK_BASE = 0x8000000
STACK_SIZE = 0x200000
JNI_ENV_ADDR = 0x200000
JNI_TABLE_ADDR = 0x201000
INPUT_BUFF_ADDR = 0x300000
OUTPUT_BUFF_ADDR = 0x301000
SENTINEL_RET = 0x9000000

def run_simulation(pin="1234", amount="00001337", check_flag=0xF0):
    # 格式化输入: 8位 PIN + 8位金额
    pin_str = f"{int(pin):08d}"
    amount_str = f"{int(amount):08d}"
    in_bytes = (pin_str + amount_str).encode('ascii')
    print(f"[*] 构造输入明文 (16 字节): {in_bytes!r}, 校验标志: 0x{check_flag:02x}")

    mu = Uc(UC_ARCH_X86, UC_MODE_64)

    # 1. 映射 SO 内存
    f = open(SO_PATH, "rb")
    elf = ELFFile(f)
    max_va = 0
    for seg in elf.iter_segments():
        if seg['p_type'] == 'PT_LOAD':
            max_va = max(max_va, seg['p_vaddr'] + seg['p_memsz'])
    
    map_size = (max_va + 0xFFF) & ~0xFFF
    mu.mem_map(SO_BASE, map_size + 0x10000, UC_PROT_ALL)

    for seg in elf.iter_segments():
        if seg['p_type'] == 'PT_LOAD':
            f.seek(seg['p_offset'])
            data = f.read(seg['p_filesz'])
            mu.mem_write(SO_BASE + seg['p_vaddr'], data)

    # 2. 映射栈空间
    mu.mem_map(STACK_BASE, STACK_SIZE, UC_PROT_ALL)
    # 映射哨兵返回页
    mu.mem_map(SENTINEL_RET, 0x1000, UC_PROT_ALL)
    mu.mem_write(SENTINEL_RET, b"\xf4") # hlt

    # 映射 TLS 页并配置 FS 寄存器基址 (绕过 fs:[0x28] 栈保护检查)
    TLS_ADDR = 0x100000
    mu.mem_map(TLS_ADDR, 0x1000, UC_PROT_ALL)
    mu.mem_write(TLS_ADDR + 0x28, struct.pack("<Q", 0x1122334455667788)) # 假 Canary
    mu.reg_write(UC_X86_REG_FS_BASE, TLS_ADDR)

    # 3. 自动执行 ELF 重定位 (.rela.dyn + .rela.plt) - 模拟标准动态链接器 ld.so
    print("[*] 自动执行 ELF 符号重定位 (.rela.dyn & .rela.plt)...")
    dynsym = elf.get_section_by_name('.dynsym')
    reloc_count = 0

    for section_name in ['.rela.dyn', '.rela.plt']:
        rela_sec = elf.get_section_by_name(section_name)
        if rela_sec:
            for reloc in rela_sec.iter_relocations():
                r_type = reloc['r_info_type']
                r_offset = reloc['r_offset']
                r_addend = reloc['r_addend']
                
                # R_X86_64_RELATIVE = 8
                if r_type == 8:
                    val = SO_BASE + r_addend
                    mu.mem_write(SO_BASE + r_offset, struct.pack("<Q", val))
                    reloc_count += 1
                # R_X86_64_GLOB_DAT = 6 或 R_X86_64_JUMP_SLOT = 7
                elif r_type in [6, 7]:
                    sym_idx = reloc['r_info_sym']
                    sym = dynsym.get_symbol(sym_idx)
                    if sym['st_value'] != 0:
                        val = SO_BASE + sym['st_value'] + r_addend
                        mu.mem_write(SO_BASE + r_offset, struct.pack("<Q", val))
                        reloc_count += 1
    print(f"    -> 成功应用了 {reloc_count} 处动态重定位项")

    # 4. 映射并构造 JNIEnv 与模拟函数表
    mu.mem_map(JNI_ENV_ADDR, 0x10000, UC_PROT_ALL)
    mu.mem_map(INPUT_BUFF_ADDR, 0x10000, UC_PROT_ALL)

    # JNIEnv* 就是指向 JNIInvokeInterface* 的指针
    mu.mem_write(JNI_ENV_ADDR, struct.pack("<Q", JNI_TABLE_ADDR))

    # 写入输入数据
    mu.mem_write(INPUT_BUFF_ADDR, in_bytes)

    # 在 JNI 函数表中打桩核心函数
    # 0x558 (GetArrayLength) -> 返回 16
    # 0x5c0 (GetByteArrayElements) -> 返回 INPUT_BUFF_ADDR
    # 0x560 (NewByteArray) -> 返回输出对象句柄
    # 0x600 (ReleaseByteArrayElements) -> 空操作
    # 0x628 (SetByteArrayRegion) -> 拷贝到 OUTPUT_BUFF_ADDR
    
    # 我们用一段通用的微型机器码作为桩函数 (Stub)
    STUB_BASE = 0x205000
    # Stub 1: return 16 (GetArrayLength: mov eax, 16; ret) -> 48c7c010000000c3
    mu.mem_write(STUB_BASE, bytes.fromhex("48c7c010000000c3"))
    mu.mem_write(JNI_TABLE_ADDR + 0x558, struct.pack("<Q", STUB_BASE))

    # Stub 2: return INPUT_BUFF_ADDR (GetByteArrayElements: mov rax, 0x300000; ret)
    mu.mem_write(STUB_BASE + 0x10, bytes.fromhex("48b80000300000000000c3"))
    mu.mem_write(JNI_TABLE_ADDR + 0x5c0, struct.pack("<Q", STUB_BASE + 0x10))

    # Stub 3: NewByteArray (mov rax, 0x400000; ret)
    mu.mem_write(STUB_BASE + 0x20, bytes.fromhex("48b80000400000000000c3"))
    mu.mem_write(JNI_TABLE_ADDR + 0x560, struct.pack("<Q", STUB_BASE + 0x20))

    # Stub 4: 默认桩函数 (xor eax, eax; ret)
    mu.mem_write(STUB_BASE + 0x30, bytes.fromhex("31c0c3"))
    for offset in range(0, 0x700, 8):
        if offset not in [0x558, 0x5c0, 0x560]:
            mu.mem_write(JNI_TABLE_ADDR + offset, struct.pack("<Q", STUB_BASE + 0x30))

    # 监听并拦截 JNI SetByteArrayRegion (偏移 0x628) 获取最终输出
    captured_output = None
    SET_BYTE_ARRAY_REGION_STUB = STUB_BASE + 0x200
    mu.mem_write(SET_BYTE_ARRAY_REGION_STUB, bytes.fromhex("90c3")) # 挂钩子
    
    def hook_set_byte_array_region(uc, address, size, user_data):
        nonlocal captured_output
        # x86_64 ABI: rdi=env, rsi=array, rdx=start, rcx=len, r8=buf
        buf_ptr = uc.reg_read(UC_X86_REG_R8)
        len_val = uc.reg_read(UC_X86_REG_RCX)
        if len_val > 0 and buf_ptr != 0:
            captured_output = uc.mem_read(buf_ptr, len_val)
            print(f"[🎉🎉🎉] 成功捕获 Native 函数最终加密输出 (长度 {len_val} 字节):")
            print(f"      Hex  : {captured_output.hex()}")
            print(f"      首字节状态码: {captured_output[0]} ({'0x51 红色失败' if captured_output[0] == 81 else '绿色校验成功！'})")
        # 模拟返回
        rsp = uc.reg_read(UC_X86_REG_RSP)
        ret_addr = struct.unpack("<Q", uc.mem_read(rsp, 8))[0]
        uc.reg_write(UC_X86_REG_RSP, rsp + 8)
        uc.reg_write(UC_X86_REG_RIP, ret_addr)

    mu.hook_add(UC_HOOK_CODE, hook_set_byte_array_region, None, SET_BYTE_ARRAY_REGION_STUB, SET_BYTE_ARRAY_REGION_STUB)
    mu.mem_write(JNI_TABLE_ADDR + 0x628, struct.pack("<Q", SET_BYTE_ARRAY_REGION_STUB))

    # 4. 为 PLT/GOT 表打桩常见 libc 函数 (避免未重定位跳回解析器)
    # 构造一个极简 memset 汇编桩: rep stosb (rdi=dest, rsi=val, rdx=count)
    # 4889d1 (mov rcx, rdx) + 88f0 (mov al, sil) + f3aa (rep stosb) + c3 (ret)
    MEMSET_STUB = STUB_BASE + 0x100
    mu.mem_write(MEMSET_STUB, bytes.fromhex("4889d188f0f3aac3"))
    mu.mem_write(SO_BASE + 0x28bcf8, struct.pack("<Q", MEMSET_STUB))

    # 构造一个极简 memcpy 汇编桩: rep movsb (rdi=dest, rsi=src, rdx=count)
    # 4889d1 (mov rcx, rdx) + f3a4 (rep movsb) + c3 (ret)
    MEMCPY_STUB = STUB_BASE + 0x120
    mu.mem_write(MEMCPY_STUB, bytes.fromhex("4889d1f3a4c3"))
    mu.mem_write(SO_BASE + 0x28bd28, struct.pack("<Q", MEMCPY_STUB))

    # malloc 打桩: 构造一个极简 Bump Allocator
    # 模拟分配在 0x900000 起始的堆内存中
    # 48b80000900000000000 (mov rax, 0x900000) + 4801f8 (add rax, rdi) ...
    # 极简: 每次返回预映射的堆页指针 HEAP_ADDR
    HEAP_ADDR = 0x900000
    mu.mem_map(HEAP_ADDR, 0x100000, UC_PROT_ALL)
    
    # 动态堆内存分配器 (Bump Allocator)
    current_heap_ptr = 0xA000000
    mu.mem_map(current_heap_ptr, 0x400000, UC_PROT_ALL) # 4MB 堆空间

    def hook_malloc(uc, address, size, user_data):
        nonlocal current_heap_ptr
        # x86_64 ABI: rdi 是请求大小
        rdi = uc.reg_read(UC_X86_REG_RDI)
        alloc_size = (rdi + 15) & ~15
        allocated = current_heap_ptr
        current_heap_ptr += alloc_size
        uc.reg_write(UC_X86_REG_RAX, allocated)
        # 直接执行 ret 模拟返回
        rsp = uc.reg_read(UC_X86_REG_RSP)
        ret_addr = struct.unpack("<Q", uc.mem_read(rsp, 8))[0]
        uc.reg_write(UC_X86_REG_RSP, rsp + 8)
        uc.reg_write(UC_X86_REG_RIP, ret_addr)

    # 在 MALLOC_STUB 处挂载 Python 钩子
    MALLOC_STUB = STUB_BASE + 0x160
    mu.mem_write(MALLOC_STUB, bytes.fromhex("90c3")) # nop, ret
    mu.hook_add(UC_HOOK_CODE, hook_malloc, None, MALLOC_STUB, MALLOC_STUB)
    mu.mem_write(SO_BASE + 0x28bc98, struct.pack("<Q", MALLOC_STUB))

    # memcpy 多条目打桩
    mu.mem_write(SO_BASE + 0x28bcb0, struct.pack("<Q", MEMCPY_STUB))

    # calloc 打桩: 每次同样分配清零内存并返回堆指针
    CALLOC_STUB = STUB_BASE + 0x1c0
    mu.mem_write(CALLOC_STUB, bytes.fromhex("90c3")) # 挂 Python 钩子
    
    def hook_calloc(uc, address, size, user_data):
        nonlocal current_heap_ptr
        # rdi = num, rsi = size
        num = uc.reg_read(UC_X86_REG_RDI)
        sz = uc.reg_read(UC_X86_REG_RSI)
        total = (num * sz + 15) & ~15
        allocated = current_heap_ptr
        current_heap_ptr += max(total, 64)
        # 清零内存
        uc.mem_write(allocated, b"\x00" * max(total, 64))
        uc.reg_write(UC_X86_REG_RAX, allocated)
        rsp = uc.reg_read(UC_X86_REG_RSP)
        ret_addr = struct.unpack("<Q", uc.mem_read(rsp, 8))[0]
        uc.reg_write(UC_X86_REG_RSP, rsp + 8)
        uc.reg_write(UC_X86_REG_RIP, ret_addr)

    mu.hook_add(UC_HOOK_CODE, hook_calloc, None, CALLOC_STUB, CALLOC_STUB)
    mu.mem_write(SO_BASE + 0x28be38, struct.pack("<Q", CALLOC_STUB))

    # 4. 配置栈顶与返回地址
    rsp = STACK_BASE + STACK_SIZE - 0x2000
    mu.mem_write(rsp, struct.pack("<Q", SENTINEL_RET))
    mu.reg_write(UC_X86_REG_RSP, rsp)
    mu.reg_write(UC_X86_REG_RBP, rsp)

    # 6. 执行 .init_array 中的构造函数进行全局数据解密 (OLLVM .datadiv_decode)
    INIT_ARRAY_VA = SO_BASE + 0x28b248
    INIT_ARRAY_COUNT = 0x2d8 // 8
    print(f"[*] 执行 .init_array 解码构造链 ({INIT_ARRAY_COUNT} 个函数)...")
    
    for i in range(INIT_ARRAY_COUNT):
        func_ptr = struct.unpack("<Q", mu.mem_read(INIT_ARRAY_VA + i * 8, 8))[0]
        if func_ptr != 0:
            target_va = func_ptr # 已经由重定位加上了 SO_BASE!
            # 为每个构造函数压入返回哨兵地址
            mu.mem_write(rsp, struct.pack("<Q", SENTINEL_RET))
            mu.reg_write(UC_X86_REG_RSP, rsp)
            try:
                mu.emu_start(target_va, SENTINEL_RET, timeout=1*1000*1000)
            except UcError:
                pass

    # 检查全局变量 0x319010 在执行构造函数后的真实解密值
    decrypted_base = struct.unpack("<I", mu.mem_read(SO_BASE + 0x319010, 4))[0]
    print(f"[+] 全局变量 0x319010 解密后状态: 0x{decrypted_base:08x}")

    # 6. 配置参数 (x86_64 ABI): rdi=env, rsi=thiz, rdx=inBuff, rcx=flag
    mu.reg_write(UC_X86_REG_RDI, JNI_ENV_ADDR)
    mu.reg_write(UC_X86_REG_RSI, 0)
    mu.reg_write(UC_X86_REG_RDX, INPUT_BUFF_ADDR)
    mu.reg_write(UC_X86_REG_RCX, check_flag)

    # 监控所有写入堆空间的操作 (捕获加密中间态)
    heap_writes = []
    def trace_heap_write(uc, access, address, size, value, user_data):
        if address >= 0xA000000 and address < 0xA100000:
            heap_writes.append((address, size, value))

    mu.hook_add(UC_HOOK_MEM_WRITE, trace_heap_write)

    target_func_va = SO_BASE + 0x1780f0
    print(f"[*] 开始纯软件仿真执行 Native 目标函数: 0x{target_func_va:x} ...")

    def hook_unmapped(uc, access, address, size, value, user_data):
        rip = uc.reg_read(UC_X86_REG_RIP)
        rdx = uc.reg_read(UC_X86_REG_RDX)
        rax = uc.reg_read(UC_X86_REG_RAX)
        print(f"[!] 触发未映射内存访问: Addr=0x{address:x}, Size={size}, RIP=0x{rip:x}, RDX=0x{rdx:x}, RAX=0x{rax:x}")
        return False

    mu.hook_add(UC_HOOK_MEM_READ_UNMAPPED, hook_unmapped)

    last_instructions = []
    executed_instructions = 0
    def trace_exec(uc, address, size, user_data):
        nonlocal executed_instructions
        executed_instructions += 1
        if len(last_instructions) >= 10:
            last_instructions.pop(0)
        last_instructions.append(address)

    mu.hook_add(UC_HOOK_CODE, trace_exec)

    try:
        mu.emu_start(target_func_va, SENTINEL_RET, timeout=10*1000*1000)
    except UcError as e:
        pc = mu.reg_read(UC_X86_REG_RIP)
        print(f"[!] 仿真捕获异常/停机: {e} @ PC=0x{pc:x}")

    print(f"[+] 仿真总计无异常执行了 {executed_instructions} 条指令！")
    print("[*] 退出前最后 10 条指令地址:")
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    for addr in last_instructions:
        try:
            ins = next(md.disasm(mu.mem_read(addr, 15), addr))
            print(f"    0x{addr:06x}: {ins.mnemonic:8s} {ins.op_str}")
        except Exception:
            print(f"    0x{addr:06x}: <disasm failed>")
    print(f"[+] 仿真执行阶段共捕获到 {len(heap_writes)} 次堆内存数据写入！")
    # 检查堆内存前 128 字节的内容
    dumped_heap = mu.mem_read(0xA000000, 128)
    print(f"[+] 堆内存头 128 字节 (Hex):")
    print(f"    {dumped_heap.hex()}")
    ascii_repr = ''.join(chr(b) if 32 <= b < 127 else '.' for b in dumped_heap)
    print(f"    ASCII: {ascii_repr}")

    rax = mu.reg_read(UC_X86_REG_RAX)
    print(f"[+] 函数执行结束，返回句柄 RAX: 0x{rax:x}")

if __name__ == "__main__":
    run_simulation()
