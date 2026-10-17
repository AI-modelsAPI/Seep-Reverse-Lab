#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V3_selfconsistency.py — 自洽性验证（零真机）
==============================================
原理: 三条独立数据应互相自洽
  A) 仿真捕获的 dispatch 序列 (opcode_trace)
  B) 静态解码的表 (V2 结果)
  C) 仿真观测的 opcode 集合

判据:
  1. dispatch 中出现的每个 opcode, 都应在表索引范围内 (0-255)
  2. 静态解出的表项数 (256) >= dispatch 用到的 opcode 数
  3. 每个用到的 opcode, 其静态表项目标 应该 是合法代码
  4. 字节码流中出现的字节 应 >= dispatch 用到的 opcode 数
"""
import sys, os, struct, json, collections
from capstone import *
md = Cs(CS_ARCH_X86, CS_MODE_64)


def parse_pe(path):
    d = open(path, 'rb').read()
    lfa = struct.unpack_from('<I', d, 0x3c)[0]
    _, ns, _, _, _, osz, _ = struct.unpack_from('<HHIIIHH', d, lfa + 4)
    opt = lfa + 24
    ib = struct.unpack_from('<Q', d, opt + 24)[0]
    sec = opt + osz
    secs = []
    for i in range(ns):
        b = sec + i * 40
        n = d[b:b+8].rstrip(b'\0').decode('latin1')
        vs, va, rs, pr = struct.unpack_from('<IIII', d, b + 8)
        secs.append(dict(name=n, vsize=vs, rva=va, rsize=rs, paddr=pr))
    return d, ib, secs


def rva2off(secs, rva):
    for s in secs:
        if s['rva'] <= rva < s['rva'] + max(s['vsize'], s['rsize']):
            delta = rva - s['rva']
            if s['rsize'] and delta < s['rsize']:
                return s['paddr'] + delta
    return None


def main(sample, json_path):
    name = os.path.basename(sample)
    print("=" * 84)
    print(f"V3 自洽性验证: {name}")
    print("=" * 84)

    # 数据源 A: 仿真结果
    if not os.path.exists(json_path):
        print(f"  ❌ 缺少仿真结果 {json_path}"); return
    j = json.load(open(json_path))
    trace = j.get('opcode_trace') or []
    executed = set(j.get('executed_opcodes') or [])
    if not executed and trace:
        executed = set(trace)          # 从 trace 推导
        print(f"  [注意] 从 trace 推导 executed 集合")
    # 兼容两种 JSON 格式
    if j.get('table_base'):
        tbl_va = int(j['table_base'], 16)
    else:
        tbl_va = None      # 稍后用 ImageBase + table_rva 补
    tbl_rva_hint = int(j.get('table_rva', '0x0'), 16)
    print(f"  [A] 仿真 opcode_trace : {len(trace)} 项")
    print(f"  [A] 仿真 used opcodes : {len(executed)} 种")

    # 数据源 B: 静态解码
    d, ib, secs = parse_pe(sample)
    if tbl_va is None:
        tbl_va = ib + tbl_rva_hint
    tbl_rva = tbl_va - ib
    print(f"  [A] 表基址            : 0x{tbl_va:x}")
    off = rva2off(secs, tbl_rva)
    mech = str(j.get('mechanism', ''))
    width = 4 if ('rdx' in mech or 'r10*4' in mech) else 8
    print(f"  [B] 表静态定位        : 文件偏移 0x{off:x}, {width} 字节/项")

    static_targets = {}
    for i in range(256):
        raw = d[off + i*width: off + i*width + width]
        if len(raw) < width: continue
        if width == 8:
            tva = struct.unpack('<Q', raw)[0]
        else:
            tva = (tbl_va + struct.unpack('<i', raw)[0]) & 0xFFFFFFFFFFFFFFFF
        trva = tva - ib
        if 0 <= trva < 0x3000000:
            to = rva2off(secs, trva)
            if to is not None:
                insns = list(md.disasm(d[to:to+32], tva))
                static_targets[i] = dict(rva=trva, valid=len(insns) >= 3,
                                         first=f"{insns[0].mnemonic} {insns[0].op_str}" if insns else None)
    print(f"  [B] 静态解出目标      : {len(static_targets)}/256")

    # ── 判据检查 ──
    print(f"\n  === 自洽性判据 ===")
    checks = []

    # 1. opcode 范围
    ok1 = all(0 <= o <= 255 for o in executed)
    checks.append(("① opcode 全部落在 0-255 (8-bit)", ok1))
    print(f"    {'✅' if ok1 else '❌'} opcode 范围: "
          f"{min(executed)} .. {max(executed)}")

    # 2. 表项数 >= 用到的 opcode 数
    ok2 = len(static_targets) >= len(executed)
    checks.append(("② 静态表项数 >= 使用的 opcode 数", ok2))
    print(f"    {'✅' if ok2 else '❌'} {len(static_targets)} >= {len(executed)}")

    # 3. 每个用到的 opcode 都有静态表项
    missing = [o for o in executed if o not in static_targets]
    ok3 = len(missing) == 0
    checks.append(("③ 使用的 opcode 全部有静态表项", ok3))
    print(f"    {'✅' if ok3 else '⚠'} 缺失: {missing[:10] if missing else '无'}")

    # 4. 用到的 opcode 其表项都是合法代码
    bad = [o for o in executed if o in static_targets and not static_targets[o]['valid']]
    ok4 = len(bad) == 0
    checks.append(("④ 使用的 opcode 表项均为合法代码", ok4))
    print(f"    {'✅' if ok4 else '⚠'} 非法项: {bad[:10] if bad else '无'}")

    # 5. 仿真轨迹里的 opcode 与 executed 集合一致
    trace_set = set(trace)
    ok5 = trace_set.issubset(set(executed)) if executed else True
    checks.append(("⑤ trace 的 opcode ⊆ executed 集合", ok5))
    print(f"    {'✅' if ok5 else '❌'} trace 独有: {sorted(trace_set - executed)[:10]}")

    # 6. opcode 分布合理性: 高频 opcode 应有 handler
    freq = collections.Counter(trace)
    top10 = [o for o, _ in freq.most_common(10)]
    ok6 = all(o in static_targets for o in top10)
    checks.append(("⑥ 高频 opcode (Top10) 均有表项", ok6))
    print(f"    {'✅' if ok6 else '❌'} Top10: {[hex(o) for o in top10]}")

    passed = sum(1 for _, v in checks if v)
    print(f"\n  => V3 {'✅ 通过' if passed == len(checks) else '⚠ 部分通过'}: "
          f"{passed}/{len(checks)} 条自洽性判据成立")
    return passed == len(checks)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2
         else 'out/math.3.0.0-virt.exe.vmp_spec_final.json')
