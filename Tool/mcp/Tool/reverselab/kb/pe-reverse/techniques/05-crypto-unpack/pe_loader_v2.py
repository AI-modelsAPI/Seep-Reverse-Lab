#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PE 加载器修复版：IAT 打桩页必须主动映射 + 支持 per-API 桩

原 bug:
  1. stub_page 在映像外 (load_base + sizeof_image + 0x10000)，但从未 mem_map
     -> 自愈把它映射成零页 -> jmp 到零页 -> 程序跑飞
  2. 所有导入共用一个桩，无法区分是哪个 API 被调用
  3. 未处理 Windows x64 的 __security_init_cookie / TLS callback

修复:
  1. 主动映射桩页
  2. 每个 API 独立桩地址，回调记录调用
  3. 处理常用 API 的返回语义（GetModuleHandleA/GetProcAddress 等）
"""
import sys, os, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe_headless_loader import PELoader, align_up, PAGE, STUB_XOR_EAX_RET

from unicorn import *
from unicorn.x86_const import *


# 常用 API 的桩返回语义（Windows x64 调用约定）
API_SEMANTICS = {
    'GetModuleHandleA': 'handle',      # 返回假模块句柄
    'GetModuleHandleW': 'handle',
    'GetProcAddress': 'proc',          # 返回桩地址
    'LoadLibraryA': 'handle',
    'LoadLibraryW': 'handle',
    'VirtualAlloc': 'heap',
    'VirtualAllocEx': 'heap',
    'HeapAlloc': 'heap',
    'malloc': 'heap',
    'calloc': 'heap',
    'GetProcessHeap': 'heap',
    'GetCurrentProcess': 'const',
    'GetCurrentThreadId': 'const',
    'GetCurrentProcessId': 'const',
    'GetLastError': 'zero',
    'Sleep': 'nop',
    'IsDebuggerPresent': 'zero',       # 反调试旁路
    'CheckRemoteDebuggerPresent': 'zero',
    'QueryPerformanceCounter': 'zero',
    'GetTickCount': 'tick',
    'GetTickCount64': 'tick',
    'GetSystemTimeAsFileTime': 'nop',
    'EnterCriticalSection': 'nop',
    'LeaveCriticalSection': 'nop',
    'InitializeCriticalSection': 'nop',
    'DeleteCriticalSection': 'nop',
    'TlsAlloc': 'const',
    'TlsFree': 'nop',
    'TlsSetValue': 'nop',
    'TlsGetValue': 'zero',
    'MultiByteToWideChar': 'const',
    'WideCharToMultiByte': 'const',
    'SetUnhandledExceptionFilter': 'zero',
    'UnhandledExceptionFilter': 'zero',
    'GetCPInfo': 'const',
    'GetStartupInfoA': 'nop',
    'GetStartupInfoW': 'nop',
}

STUB_SIZE = 0x20


class LoaderV2(PELoader):
    """修复版：桩页主动映射 + per-API 桩 + 调用记录"""

    def __init__(self, path, base=None):
        super().__init__(path, base)
        self.api_addrs = {}         # api_name -> stub_addr
        self.addr2api = {}          # stub_addr -> api_name
        self.call_log = []          # (api_name, retval)
        self.stub_page = None
        self.heap_ptr = None
        self.heap_base = None

    def prepare_stubs(self, mu, n_apis=None):
        """主动映射桩页，为每个 API 分配独立桩"""
        self.mu = mu
        n = n_apis or max(len(self.iat_stubs), len(API_SEMANTICS) + 16)
        need = align_up(n * STUB_SIZE + PAGE, PAGE)
        # 桩页放在映像之后的独立区域，主动映射
        self.stub_page = align_up(self.load_base + self.sizeof_image, 0x10000) + 0x100000
        try:
            mu.mem_map(self.stub_page, need, UC_PROT_ALL)
        except UcError:
            # 已映射
            pass
        # 堆
        self.heap_base = self.stub_page + need + 0x100000
        self.heap_ptr = self.heap_base
        mu.mem_map(self.heap_base, 0x4000000, UC_PROT_ALL)   # 64MB 堆
        return self

    def stub_for(self, api_fullname):
        """为某个 API 名字分配/复用桩地址"""
        short = api_fullname.split('!')[-1]
        if short in self.api_addrs:
            return self.api_addrs[short]
        idx = len(self.api_addrs)
        addr = self.stub_page + idx * STUB_SIZE
        # 默认桩: xor eax,eax; ret
        self.mu.mem_write(addr, STUB_XOR_EAX_RET)
        self.api_addrs[short] = addr
        self.addr2api[addr] = short
        return addr

    def install_hooks(self):
        """装 API 调用 hook，实现语义"""
        def hook(uc, address, size, ud):
            api = self.addr2api.get(address)
            if api is None:
                return True
            sem = API_SEMANTICS.get(api, 'zero')
            if sem == 'heap':
                sz = uc.reg_read(UC_X86_REG_RCX) or uc.reg_read(UC_X86_REG_R8) or 0x100
                alloc = align_up(max(sz, 16), 16)
                ret = self.heap_ptr
                self.heap_ptr += alloc
                uc.reg_write(UC_X86_REG_RAX, ret)
            elif sem == 'handle':
                uc.reg_write(UC_X86_REG_RAX, self.load_base)
            elif sem == 'proc':
                # GetProcAddress: 返回一个有效桩地址
                dummy = self.stub_page + (len(self.api_addrs) + 1) * STUB_SIZE
                if dummy not in self.addr2api:
                    self.mu.mem_write(dummy, STUB_XOR_EAX_RET)
                    self.addr2api[dummy] = f'<proc@{hex(dummy)}>'
                    self.api_addrs[f'<proc@{hex(dummy)}>'] = dummy
                uc.reg_write(UC_X86_REG_RAX, dummy)
            elif sem == 'const':
                uc.reg_write(UC_X86_REG_RAX, 1)
            elif sem == 'tick':
                uc.reg_write(UC_X86_REG_RAX, 0x100000)
            else:  # zero / nop
                uc.reg_write(UC_X86_REG_RAX, 0)
            self.call_log.append((api, uc.reg_read(UC_X86_REG_RAX)))
            # 模拟 ret
            rsp = uc.reg_read(UC_X86_REG_RSP)
            ra = struct.unpack('<Q', uc.mem_read(rsp, 8))[0]
            uc.reg_write(UC_X86_REG_RSP, rsp + 8)
            uc.reg_write(UC_X86_REG_RIP, ra)
            return True

        self.mu.hook_add(UC_HOOK_CODE, hook,
                         self.stub_page, self.stub_page + 0x10000)
        return self

    def stub_imports(self, stub_page=None, verbose=True):
        """覆盖：per-API 桩"""
        rva, size = self.dirs[1]   # IMPORT
        if not rva or not size:
            return 0
        off = self.rva2off(rva)
        if off is None:
            return 0
        names = []
        n = 0
        p = off
        while True:
            oft, tstamp, fwd, name_rva, first_thunk = struct.unpack_from('<IIIII', self.d, p)
            if name_rva == 0 and first_thunk == 0:
                break
            dll = self._read_cstr(self.rva2off(name_rva)) if name_rva else '?'
            thunk_rva = oft if oft else first_thunk
            toff = self.rva2off(thunk_rva)
            k = 0
            if toff:
                while True:
                    if self.is64:
                        t = struct.unpack_from('<Q', self.d, toff + k*8)[0]
                        step = 8
                    else:
                        t = struct.unpack_from('<I', self.d, toff + k*4)[0]
                        step = 4
                    if t == 0: break
                    if not (t & (1 << (63 if self.is64 else 31))):
                        fn_rva = t & 0x7FFFFFFF
                        fn_off = self.rva2off(fn_rva)
                        fname = self._read_cstr(fn_off + 2) if fn_off else f"ord_{t & 0xffff}"
                        full = f"{dll}!{fname}"
                    else:
                        fname = f"ord_{t & 0xffff}"
                        full = f"{dll}!{fname}"
                    stub = self.stub_for(full)
                    iat_va = self.load_base + first_thunk + k*step
                    if self.is64:
                        self.mu.mem_write(iat_va, struct.pack('<Q', stub))
                    else:
                        self.mu.mem_write(iat_va, struct.pack('<I', stub))
                    names.append(full); n += 1; k += 1
            p += 20
        self.iat_stubs = names
        if verbose:
            print(f"    [import] {n} 个导入 -> {len(self.api_addrs)} 个独立桩 "
                  f"@ 0x{self.stub_page:x}")
        return n
