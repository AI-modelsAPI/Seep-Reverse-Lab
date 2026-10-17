#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V2_static_decode_v2.py — 静态解码验证（零真机、零仿真）· 修正版
================================================================
v1 缺陷: 硬编码了 3.10 的表基址 0x106774, 对 3.0-3.4 用错地址。

v2: 从仿真导出的 JSON 读取各版本真实表基址与表项宽度,
    再完全静态地从 PE 文件解码验证。

各版本表结构 (来自仿真):
  3.0-3.4: 8 字节绝对地址表, 表基址 r12 = 0x1400ee688 / 0x14012ec58 / 0x140137d70
  3.10   : 4 字节相对偏移表, 表基址 r11 = 0x140106774
"""
import sys, os, struct, json, collections
from capstone import *

md = Cs(CS_ARCH_X86, CS_MODE_64)

# 各版本表信息 (由仿真独立捕获, 见 out/*.handler_map*.json)
TABLE_INFO = {
    '3.0.0':  dict(va=0x1400ee688, width=8, kind='absolute'),
    '3.2.0':  dict(va=0x14012ec58, width=8, kind='absolute'),
    '3.4.0':  dict(va=0x140137d70, width=8, kind='absolute'),
    '3.10.0': dict(va=0x140106774, width=4, kind='relative'),
}


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
                return s['paddr'] + delta, s['name']
    return None, None


def verify(sample, info):
    d, ib, secs = parse_pe(sample)
    tbl_va = info['va']; width = info['width']
    tbl_rva = tbl_va - ib
    off, secn = rva2off(secs, tbl_rva)
    if off is None:
        return dict(ok=False, reason='表不在文件中可定位')

    targets = []
    for i in range(256):
        raw = d[off + i*width: off + i*width + width]
        if len(raw) < width:
            continue
        if info['kind'] == 'absolute':
            tva = struct.unpack('<Q', raw)[0]
        else:
            rel = struct.unpack('<i', raw)[0]
            tva = (tbl_va + rel) & 0xFFFFFFFFFFFFFFFF
        trva = tva - ib
        if not (0 <= trva < 0x3000000):
            continue
        to, ts = rva2off(secs, trva)
        if to is None:
            continue
        code = d[to:to+32]
        insns = list(md.disasm(code, tva))
        if not insns:
            targets.append((i, trva, ts, None, 0)); continue
        first = f"{insns[0].mnemonic} {insns[0].op_str}"
        targets.append((i, trva, ts, first, len(insns[:8])))

    if not targets:
        return dict(ok=False, reason='无有效目标')

    valid = [t for t in targets if t[4] >= 3]
    ratio = len(valid) / len(targets)
    return dict(ok=True, table_sec=secn, located=len(targets),
                valid=len(valid), ratio=ratio, samples=valid[:6])


def main(sample):
    name = os.path.basename(sample)
    import re as _re
    m=_re.search(r'(\d+\.\d+\.\d+)', name); ver=m.group(1) if m else '?'
    info = TABLE_INFO.get(ver)
    print("=" * 84)
    print(f"V2 静态解码验证 · {ver}")
    print("=" * 84)
    if not info:
        print(f"  未知版本 {ver}"); return
    print(f"  仿真捕获的表基址: 0x{info['va']:x}  "
          f"({info['width']} 字节/{info['kind']})")
    r = verify(sample, info)
    if not r.get('ok'):
        print(f"  ❌ {r['reason']}"); return
    print(f"  静态定位节区    : {r['table_sec']}")
    print(f"  可解出目标      : {r['located']}/256")
    print(f"  其中合法代码    : {r['valid']}  ({r['ratio']*100:.1f}%)")
    print(f"\n  样例:")
    for i, trva, ts, first, n in r['samples']:
        print(f"    opcode=0x{i:02x} RVA=0x{trva:06x} [{ts}] {first}")
    print(f"\n  => V2 {'✅ 通过' if r['ratio']>0.8 else '⚠ 部分'}")
    return r


if __name__ == '__main__':
    for p in sys.argv[1:]:
        main(p); print()
