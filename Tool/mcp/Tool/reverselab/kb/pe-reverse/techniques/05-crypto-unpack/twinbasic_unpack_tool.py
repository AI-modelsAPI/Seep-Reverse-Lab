#!/usr/bin/env python3
"""
TwinBasic/VB6 压缩资源还原工具
================================
用法:
    python3 twinbasic_unpack_tool.py <sample.exe> [outdir]

功能:
  1. 修复被破坏的 DOS 头
  2. 熵扫描定位高熵区
  3. 自动探测 raw-DEFLATE 描述符 [size0][size1][deflate] 并解压
  4. 提取内嵌 PNG / 字符串资源

适用场景: .data 段高熵区、twinBASIC/VB6 编译产物、DOS 头异常
"""
import sys, os, zlib, struct, math, hashlib
from collections import Counter

def entropy(b):
    if not b: return 0.0
    c = Counter(b); n = len(b)
    return -sum((v/n)*math.log2(v/n) for v in c.values())

def fix_dos_header(d):
    d = bytearray(d)
    for i, v in [(0,0x4D),(1,0x5A),(2,0x90),(3,0x00),(4,0x03),(5,0x00),
                 (10,0x00),(11,0x00),(26,0x00),(27,0x00)]:
        d[i] = v
    return bytes(d)

def find_high_entropy_segments(d, window=4096, thresh=7.5):
    segs, cur = [], None
    for off in range(0, len(d)-window, window):
        if entropy(d[off:off+window]) > thresh:
            if cur is None: cur = [off, off+window]
            else: cur[1] = off+window
        elif cur:
            segs.append(tuple(cur)); cur = None
    if cur: segs.append(tuple(cur))
    return segs

def try_deflate_at(d, off, max_try=65536):
    """在偏移 off 处尝试 raw/zlib deflate 解压"""
    for label, data, wbits in [
        ("raw(-15)", d[off:], -15),
        ("zlib(15)", d[off:], 15),
    ]:
        try:
            dec = zlib.decompressobj(wbits)
            out = dec.decompress(data[:8*1024*1024])
            if len(out) > 4096:
                return label, out
        except Exception:
            pass
    return None, None

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    src = sys.argv[1]
    outdir = sys.argv[2] if len(sys.argv) > 2 else "unpacked"
    os.makedirs(outdir, exist_ok=True)

    raw = open(src, "rb").read()
    print(f"[*] 样本: {src}")
    print(f"    sha256: {hashlib.sha256(raw).hexdigest()}")
    print(f"    DOS 头: {raw[:2].hex()} ({'需修复' if raw[:2]!=b'MZ' else 'OK'})")

    d = fix_dos_header(raw)
    open(os.path.join(outdir, "fixed.exe"), "wb").write(d)

    segs = find_high_entropy_segments(d)
    print(f"[*] 高熵区 (>{7.5}):")
    for a, b in segs:
        print(f"    0x{a:x} - 0x{b:x} ({b-a} bytes)")

    # 智能探测 deflate 描述符: 找形如 [size0][size1] 的两个相近大 dword，
    # 其后紧跟 deflate 流 (raw 首字节高 3 位常为 0x7x/0x4x/0x1x)
    found = False
    for a, b in segs:
        lo = max(8, a-0x4000)
        hi = min(len(d)-16, a+0x1000)
        candidates = []
        for off in range(lo, hi-8, 1):
            s0, s1 = struct.unpack_from("<II", d, off)
            # 两个大小字段: 都在 64KB~64MB, 且相差 < 5%
            if 0x10000 <= s0 <= 0x4000000 and 0x10000 <= s1 <= 0x4000000:
                if s1 and abs(s0-s1)/s1 < 0.05:
                    candidates.append((off, s0, s1))
        for off, s0, s1 in candidates:
            label, out = try_deflate_at(d, off+8)
            if out and len(out) > 100000:
                print(f"[+] 描述符 @0x{off:x}: size0={s0} size1={s1} (解出 {len(out)})")
                print(f"[+] 解压成功 ({label}): {len(out)} bytes")
                pay = os.path.join(outdir, "payload.bin")
                open(pay, "wb").write(out)
                # 提取内嵌 PNG
                p = out.find(b'\x89PNG\r\n\x1a\n', 0x100)
                if p >= 0:
                    ie = out.find(b'IEND', p)+8
                    png = os.path.join(outdir, "resource.png")
                    open(png, "wb").write(out[p:ie])
                    print(f"[+] 内嵌 PNG: {png} ({ie-p} bytes)")
                found = True
                break
        if found: break

    if not found:
        print("[!] 未自动定位 deflate 描述符 —— 请反编译入口附近找 inflate 调用链")
        print("    线索: lea eax,[0x4b09a8]; shl dword [eax],2 之后的初始化序列")

if __name__ == "__main__":
    main()
