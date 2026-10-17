#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vmp_selfheal_run.py — VMP 无真机仿真（自愈式内存管理）
======================================================
策略转变: 不再"精确复刻真机环境", 而是**让仿真自动自愈**:
  遇到未映射访问 -> 自动映射页 -> 继续执行
  遇到读未初始化 -> 返回 0 并记录
  遇到 rdtsc/cpuid -> 返回确定值

理由: 
  - VMP 的 VM context 依赖此前执行的副作用, 难以静态预测
  - 无真机场景下, "能跑完"比"精确复刻"更有价值
  - 类似 Qiling/SPEKE 的 "environment lift" 思路

目标: 尽力跑到 VM 退出 (VMEXIT) 或壳跳转到 OEP, 拿到**完整执行轨迹**。
"""
import sys, os, struct, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vmp_headless_run import VMPEnv, STACK_BASE, STACK_SIZE

from unicorn import *
from unicorn.x86_const import *
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

md = Cs(CS_ARCH_X86, CS_MODE_64)
PAGE = 0x1000


class SelfHealingEmu:
    """自愈式仿真：自动映射缺失页，记录所有事件"""

    def __init__(self, sample, max_insn=5_000_000, verbose=False):
        self.env = VMPEnv(sample, verbose=verbose)
        self.env.load().setup_env().stub_libc()
        self.mu = self.env.mu
        self.ld = self.env.ld
        self.max_insn = max_insn
        self.verbose = verbose

        self.auto_pages = set()          # 自愈映射的页
        self.unmapped_events = []        # 未映射访问记录
        self.rw_events = []              # 读写事件（用于 dump 分析）
        self.trace = []
        self.hist = collections.Counter()
        self.dispatch = []               # (opcode, handler_rva)
        self.stopped = None
        self.vmexit_seen = False

        self._install_hooks()

    # ---------- 自动映射 ----------
    def _map_page(self, addr):
        page = addr & ~(PAGE - 1)
        if page in self.auto_pages:
            return False
        try:
            self.mu.mem_map(page, PAGE, UC_PROT_ALL)
            self.auto_pages.add(page)
            return True
        except UcError:
            return False

    def _install_hooks(self):
        mu = self.mu

        # --- 读未映射: 自愈 ---
        def on_read_unmapped(uc, access, addr, size, value, ud):
            self.unmapped_events.append(('R', addr, size,
                                         uc.reg_read(UC_X86_REG_RIP)))
            if self._map_page(addr):
                return True          # 已映射，Unicorn 重试
            return True              # 映射失败也重试(可能已在别处)
        mu.hook_add(UC_HOOK_MEM_READ_UNMAPPED, on_read_unmapped)

        # --- 写未映射: 自愈 ---
        def on_write_unmapped(uc, access, addr, size, value, ud):
            self.unmapped_events.append(('W', addr, size,
                                         uc.reg_read(UC_X86_REG_RIP)))
            self._map_page(addr)
            return True
        mu.hook_add(UC_HOOK_MEM_WRITE_UNMAPPED, on_write_unmapped)

        # --- 取指未映射: 自愈 ---
        def on_fetch_unmapped(uc, access, addr, size, value, ud):
            self.unmapped_events.append(('X', addr, size,
                                         uc.reg_read(UC_X86_REG_RIP)))
            if self._map_page(addr):
                return True
            # 映射失败 -> 当作 ret/无效，填入 int3
            try:
                uc.mem_write(addr, b'\xf4')
            except UcError:
                pass
            return True
        mu.hook_add(UC_HOOK_MEM_FETCH_UNMAPPED, on_fetch_unmapped)

        # --- 记录读写（分析内存布局） ---
        def on_write(uc, access, addr, size, value, ud):
            return True
        def on_read(uc, access, addr, size, value, ud):
            return True

        # --- 指令级追踪 + dispatch 捕获 ---
        def on_code(uc, addr, size, ud):
            self.trace.append(addr)
            self.hist[addr - self.ld.load_base] += 1
            try:
                code = bytes(uc.mem_read(addr, min(size, 15)))
                ins = next(md.disasm(code, addr))
            except Exception:
                return True
            # 捕获 jmp/call [base+index*8]
            if ins.mnemonic in ('jmp', 'call') and '[' in ins.op_str:
                op = ins.op_str
                inner = op[op.index('[') + 1:op.rindex(']')].replace(' ', '')
                if '*' in inner and inner.split('*')[1].startswith('8'):
                    parts = inner.split('+')
                    regs = {}
                    for p in parts:
                        if '*' in p:
                            regs['idx'] = p.split('*')[0]
                        elif p and not p.isdigit():
                            regs['base'] = p
                    try:
                        b = uc.reg_read(getattr(UC_X86_REG, regs['base'].upper()))
                        i = uc.reg_read(getattr(UC_X86_REG, regs['idx'].upper()))
                        tgt = struct.unpack('<Q', uc.mem_read(b + i * 8, 8))[0]
                        if self.ld.load_base <= tgt < self.ld.load_base + 0x3000000:
                            self.dispatch.append((i & 0xFF, tgt - self.ld.load_base))
                    except Exception:
                        pass
            # 检测 VMEXIT 迹象: 大跨度 jmp 回到非 VMP 节区
            if ins.mnemonic == 'jmp' and ins.op_str.startswith('0x'):
                try:
                    t = int(ins.op_str, 16)
                    if t < self.ld.load_base and self.ld.load_base <= addr:
                        self.vmexit_seen = True
                except ValueError:
                    pass
            return len(self.trace) < self.max_insn
        mu.hook_add(UC_HOOK_CODE, on_code)

    def run(self, timeout=120_000_000):
        ep = self.ld.load_base + self.ld.ep
        try:
            self.mu.emu_start(ep, 0xFFFFFFFFFFFFFFFF,
                              count=self.max_insn, timeout=timeout)
        except UcError as e:
            self.stopped = str(e)
        return self

    def report(self):
        mu = self.mu
        print(f"    执行指令数  : {len(self.trace):,}")
        print(f"    唯一地址数  : {len(self.hist):,}")
        print(f"    停止原因    : {self.stopped}")
        print(f"    自愈映射页  : {len(self.auto_pages)} 页 "
              f"({len(self.auto_pages)*PAGE//1024} KB)")
        print(f"    未映射事件  : {len(self.unmapped_events)}")
        if self.unmapped_events:
            c = collections.Counter(e[0] for e in self.unmapped_events)
            print(f"      类型分布  : {dict(c)}")
            addrs = [e[1] for e in self.unmapped_events]
            print(f"      地址范围  : 0x{min(addrs):x} .. 0x{max(addrs):x}")
        print(f"    dispatch 次数: {len(self.dispatch)}")
        if self.dispatch:
            ops = collections.Counter(o for o, _ in self.dispatch)
            print(f"      opcode 种类: {len(ops)}")
        print(f"    VMEXIT 迹象 : {'✅ 检测到' if self.vmexit_seen else '❌ 未检测到'}")
        rip = mu.reg_read(UC_X86_REG_RIP)
        print(f"    最终 RIP    : 0x{rip:x} (RVA 0x{rip - self.ld.load_base:x})")

        print(f"\n    热点 Top10:")
        for pc, c in self.hist.most_common(10):
            try:
                b = mu.mem_read(self.ld.load_base + pc, 16)
                ins = next(md.disasm(b, self.ld.load_base + pc))
                txt = f"{ins.mnemonic} {ins.op_str}"
            except Exception:
                txt = "?"
            print(f"      RVA 0x{pc:08x} {c:8,d}  {txt}")


def main():
    sample = sys.argv[1] if len(sys.argv) > 1 else \
        '/root/逆向测试/windows/vmp-samples/3.0.0/math.3.0.0-virt.exe'
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 5_000_000
    print("=" * 78)
    print(f"VMP 无真机自愈仿真: {os.path.basename(sample)}")
    print("=" * 78)
    e = SelfHealingEmu(sample, max_insn=n).run()
    e.report()
    # 落盘
    outdir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'out')
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, os.path.basename(sample) + '.selfheal.json')
    json.dump(dict(sample=sample, insns=len(e.trace), unique=len(e.hist),
                   stopped=e.stopped, auto_pages=len(e.auto_pages),
                   unmapped=len(e.unmapped_events),
                   dispatch=len(e.dispatch),
                   vmexit=e.vmexit_seen,
                   final_rip=hex(e.mu.reg_read(UC_X86_REG_RIP)),
                   hot=[(hex(pc), c) for pc, c in e.hist.most_common(30)]),
              open(out, 'w'), indent=2)
    print(f"\n[+] {out}")


if __name__ == '__main__':
    main()
