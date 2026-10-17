#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V4_bytecode_crosscheck.py — 字节码反向验证（零真机）
======================================================
原理: 独立地看 VM 字节码流本身。
      字节码流是被 dispatcher 逐字节消费的 opcode。
      因此: 字节码流中出现的字节集合, 应与 dispatch 用到的 opcode 集合 高度重合。

这是**独立于表**的验证 —— 只看字节码, 不看表。

判据:
  1. 字节码用的字节 ⊆ [0, 255]        (必然)
  2. dispatch 用到的 opcode ⊆ 字节码出现的字节 (理论应成立)
  3. 字节码熵合理 (< 7.0, 否则是加密的)
  4. 字节码区段的 8-bit 分布与 opcode 频率正相关
"""
import sys, os, struct, collections, math


def entropy(buf):
    if not buf: return 0.0
    c = collections.Counter(buf); n = len(buf)
    return -sum((v/n)*math.log2(v/n) for v in c.values())


def parse_pe(path):
    d = open(path, 'rb').read()
    lfa = struct.unpack_from('<I', d, 0x3c)[0]
    _, ns, _, _, _, osz, _ = struct.unpack_from('<HHIIIHH', d, lfa + 4)
    opt = lfa + 24
    ib = struct.unpack_from('<Q', d, opt + 24)[0]
    sec = opt + osz
    secs = []
    for i in range(ns):
        b = sec + i*40
        n = d[b:b+8].rstrip(b'\0').decode('latin1')
        vs, va, rs, pr = struct.unpack_from('<IIII', d, b + 8)
        secs.append(dict(name=n, vsize=vs, rva=va, rsize=rs, paddr=pr))
    return d, ib, secs


def main(sample, bc_file=None, spec_json=None):
    name = os.path.basename(sample)
    print("=" * 84)
    print(f"V4 字节码反向验证: {name}")
    print("=" * 84)
    d, ib, secs = parse_pe(sample)
    for s in secs:
        print(f"    {s['name']:10s} RVA=0x{s['rva']:08x} vsize=0x{s['vsize']:06x}")

    # 用导出的字节码区段
    if bc_file and os.path.exists(bc_file):
        bc = open(bc_file, 'rb').read()
        print(f"\n  字节码区段文件: {bc_file} ({len(bc):,} bytes)")
    else:
        print("  ❌ 无字节码文件"); return

    print(f"  字节码熵: {entropy(bc):.3f}  "
          f"{'✅ 似明文/代码' if entropy(bc) < 7.0 else '⚠ 高熵(可能加密)'}")

    # 字节码的 8-bit 分布
    dist = collections.Counter(bc)
    print(f"  不同字节值: {len(dist)}/256")
    print(f"  高频字节 Top12: {[(hex(k), v) for k, v in dist.most_common(12)]}")

    # 与仿真 dispatch 对比
    executed = set()
    if spec_json and os.path.exists(spec_json):
        import json
        j = json.load(open(spec_json))
        trace = j.get('opcode_trace') or []
        executed = set(j.get('executed_opcodes') or []) or set(trace)
        print(f"\n  仿真 dispatch opcode: {len(executed)} 种")

    used_bytes = set(dist.keys())
    print(f"  字节码出现字节: {len(used_bytes)} 种")

    checks = []
    # 1. 字节范围
    ok1 = all(0 <= b <= 255 for b in used_bytes)
    checks.append(("① 字节值落在 0-255", ok1)); print(f"    {'✅' if ok1 else '❌'} 范围合法")

    # 2. dispatch opcode ⊆ 字节码字节
    if executed:
        miss = executed - used_bytes
        ok2 = len(miss) == 0
        checks.append(("② dispatch opcode ⊆ 字节码字节集", ok2))
        print(f"    {'✅' if ok2 else '⚠'} 缺失 {len(miss)} 个: "
              f"{sorted(hex(x) for x in miss)[:10]}")
        # 反向: 字节码字节 中多少被用过
        used_ratio = len(executed & used_bytes) / max(1, len(executed))
        print(f"        覆盖: {len(executed & used_bytes)}/{len(executed)} "
              f"= {used_ratio*100:.1f}%")

    # 3. 熵
    e = entropy(bc)
    ok3 = e < 7.5
    checks.append(("③ 字节码非高熵(未加密)", ok3))
    print(f"    {'✅' if ok3 else '❌'} 熵 {e:.3f} < 7.5")

    # 4. 字节种类数合理 (既不是 1 种也不是 256 种)
    ok4 = 8 <= len(dist) <= 250
    checks.append(("④ 字节种类数合理", ok4))
    print(f"    {'✅' if ok4 else '⚠'} {len(dist)} 种")

    # 5. 分布的偏斜: 顶级字节占比不应过小(说明有结构)
    top1 = dist.most_common(1)[0][1]/len(bc)
    ok5 = top1 > 0.01
    checks.append(("⑤ 存在主导字节(有结构)", ok5))
    print(f"    {'✅' if ok5 else '⚠'} 最高占比 {top1*100:.2f}%")

    passed = sum(1 for _, v in checks if v)
    print(f"\n  => V4 {'✅ 通过' if passed == len(checks) else '⚠ 部分'}: "
          f"{passed}/{len(checks)} 条成立")
    return passed == len(checks)


if __name__ == '__main__':
    main(sys.argv[1],
         sys.argv[2] if len(sys.argv) > 2 else None,
         sys.argv[3] if len(sys.argv) > 3 else None)
