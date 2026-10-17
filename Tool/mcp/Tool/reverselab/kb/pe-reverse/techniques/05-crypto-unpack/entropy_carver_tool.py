#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
entropy_carver_tool.py — 高熵二进制数据鉴别与无头解压路由工装
"""
import sys, os, zlib, math, argparse, struct
from collections import Counter

CRYPTO_SIGNATURES = {
    "AES_SBOX": bytes.fromhex("637C777BF26B6FC53001672BFED7AB76"),
    "AES_INV_SBOX": bytes.fromhex("52096AD53036A538BF40A39E81F3D7FB"),
    "AES_Te0_TABLE": bytes.fromhex("C66363A5F87C7C84EE777799F67B7B8D"),
    "SHA256_K_CONST": bytes.fromhex("428A2F9871374491B5C0FBCFE9B5DBA5"),
    "CHACHA20_SIGMA": b"expand 32-byte k",
    "SM4_SBOX": bytes.fromhex("D690E9FECCE13DB716B614C228FB2C05")
}

def calc_entropy(data):
    if not data: return 0.0
    c = Counter(data)
    n = len(data)
    return -sum((cnt / n) * math.log2(cnt / n) for cnt in c.values())

def probe_all_compressions(data, offset=0, max_read=10*1024*1024):
    sub = data[offset:offset+max_read]
    results = []

    # 1. raw deflate (wbits = -15)
    for probe in range(min(len(sub), 64)):
        try:
            d = zlib.decompressobj(-15)
            out = d.decompress(sub[probe:probe+4*1024*1024])
            if len(out) > 2048:
                results.append(("raw-deflate", offset + probe, len(out)))
                break
        except Exception:
            pass

    # 2. standard zlib (wbits = 15)
    for probe in range(min(len(sub), 64)):
        try:
            d = zlib.decompressobj(15)
            out = d.decompress(sub[probe:probe+4*1024*1024])
            if len(out) > 2048:
                results.append(("zlib", offset + probe, len(out)))
                break
        except Exception:
            pass

    # 3. gzip (wbits = 31)
    for probe in range(min(len(sub), 64)):
        try:
            d = zlib.decompressobj(31)
            out = d.decompress(sub[probe:probe+4*1024*1024])
            if len(out) > 2048:
                results.append(("gzip", offset + probe, len(out)))
                break
        except Exception:
            pass

    # 4. lzma
    try:
        import lzma
        for probe in range(min(len(sub), 32)):
            try:
                out = lzma.decompress(sub[probe:probe+2*1024*1024])
                if len(out) > 2048:
                    results.append(("lzma", offset + probe, len(out)))
                    break
            except Exception:
                pass
    except ImportError:
        pass

    return results

def scan_crypto_signatures(data):
    hits = []
    for name, sig in CRYPTO_SIGNATURES.items():
        idx = 0
        while True:
            idx = data.find(sig, idx)
            if idx == -1: break
            hits.append((name, idx))
            idx += len(sig)
    return hits

def main():
    p = argparse.ArgumentParser(description="高熵数据鉴别与无头解压工具")
    p.add_argument("file", help="目标二进制或 dump 文件")
    p.add_argument("--outdir", default="carved_outputs", help="解压导出目录")
    args = p.parse_args()

    data = open(args.file, "rb").read()
    total_ent = calc_entropy(data)
    print(f"[*] 样本: {args.file} (大小: {len(data)} 字节, 全局熵: {total_ent:.2f})")

    # 密码学结构扫描
    crypto_hits = scan_crypto_signatures(data)
    if crypto_hits:
        print("[+] 密码学特征命中 (加密逻辑迹象):")
        for name, off in crypto_hits:
            print(f"    - {name:16s} @ 偏移 0x{off:x}")
    else:
        print("[-] 未命中已知标准对称加密 S 盒 / 常量")

    # 寻找高熵段
    window = 4096
    high_segs = []
    cur = None
    for off in range(0, len(data) - window, window):
        ent = calc_entropy(data[off:off+window])
        if ent > 7.4:
            if cur is None: cur = [off, off+window]
            else: cur[1] = off+window
        elif cur:
            high_segs.append(tuple(cur))
            cur = None
    if cur: high_segs.append(tuple(cur))

    print(f"[*] 检测到 {len(high_segs)} 个高熵连续段:")
    os.makedirs(args.outdir, exist_ok=True)
    for i, (s, e) in enumerate(high_segs):
        seg_ent = calc_entropy(data[s:e])
        print(f"    段 #{i}: 0x{s:x} - 0x{e:x} (长度: {e-s} 字节, 熵: {seg_ent:.2f})")
        # 尝试无头解压
        decomp_results = probe_all_compressions(data, offset=s)
        for algo, hit_off, out_len in decomp_results:
            out_file = os.path.join(args.outdir, f"seg{i}_{algo}_0x{hit_off:x}.bin")
            print(f"        🎉 命中无头压缩流: {algo} @ 0x{hit_off:x} -> 解出 {out_len} 字节")
            # 写出
            if algo == "raw-deflate":
                res = zlib.decompressobj(-15).decompress(data[hit_off:hit_off+8*1024*1024])
                open(out_file, "wb").write(res)
            elif algo == "zlib":
                res = zlib.decompressobj(15).decompress(data[hit_off:hit_off+8*1024*1024])
                open(out_file, "wb").write(res)
            print(f"        -> 已落地至: {out_file}")

if __name__ == "__main__":
    main()
