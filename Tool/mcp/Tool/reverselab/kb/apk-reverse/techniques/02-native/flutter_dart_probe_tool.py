#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
flutter_dart_probe_tool.py — Flutter AOT 镜像特征与 Snapshot Hash 提取工装
========================================================================
作用：从 libflutter.so 和 libapp.so 中直接提取 Flutter Engine ID、Dart SDK 版本、
      Snapshot Hash (32B) 与 VM 标志，为符号恢复与反编译建立前置锚点。
"""

import sys, os, re, struct, argparse

def extract_libflutter(path):
    data = open(path, "rb").read()
    # 查找 40 字节十六进制哈希
    hashes = re.findall(rb'\x00([a-f0-9]{40})\x00', data)
    engine_ids = [h.decode() for h in hashes]
    
    # 查找 Dart SDK 版本号
    m = re.search(rb'\x00([\d\w\.-]+) \((stable|beta|dev)\)', data)
    dart_ver = m.group(1).decode() if m else "未知"
    channel = m.group(2).decode() if m else "unknown"

    return {
        "engine_ids": list(set(engine_ids)),
        "dart_version": f"{dart_ver} ({channel})"
    }

def extract_libapp(path):
    data = open(path, "rb").read()
    # 查找 _kDartVmSnapshotData 或魔数特征
    # Snapshot 头部特征: 32字节十六进制哈希通常紧随魔数
    # 直接在文件前 1MB 搜索可能的 32 字节哈希字符串
    m = re.search(rb'([a-f0-9]{32})\x00', data)
    snap_hash = m.group(1).decode() if m else "未直接暴露(或被混淆)"

    # 提取启动标志字符串 (例如 --causal_async_stacks)
    flags = re.findall(rb'(--[\w_-]+)', data)
    flag_list = [f.decode() for f in flags[:8]]

    return {
        "snapshot_hash": snap_hash,
        "sample_flags": flag_list
    }

def main():
    p = argparse.ArgumentParser(description="Flutter AOT 镜像特征提取工具")
    p.add_argument("--libflutter", help="输入 libflutter.so 路径")
    p.add_argument("--libapp", help="输入 libapp.so 路径")
    args = p.parse_args()

    if not args.libflutter and not args.libapp:
        p.print_help()
        sys.exit(1)

    print("=== Flutter / Dart AOT 逆向取证分析 ===")
    if args.libflutter and os.path.exists(args.libflutter):
        print(f"[*] 分析 libflutter: {args.libflutter}")
        info = extract_libflutter(args.libflutter)
        print(f"    - Dart 版本: {info['dart_version']}")
        print(f"    - 引擎 Engine IDs: {info['engine_ids']}")
        if info['engine_ids']:
            print(f"    - 官方符号源: https://storage.googleapis.com/flutter_infra_release/flutter/{info['engine_ids'][0]}/dart-sdk-windows-x64.zip")

    if args.libapp and os.path.exists(args.libapp):
        print(f"[*] 分析 libapp: {args.libapp}")
        app_info = extract_libapp(args.libapp)
        print(f"    - Snapshot Hash: {app_info['snapshot_hash']}")
        print(f"    - 常见 VM Flags: {', '.join(app_info['sample_flags'])}")

if __name__ == "__main__":
    main()
