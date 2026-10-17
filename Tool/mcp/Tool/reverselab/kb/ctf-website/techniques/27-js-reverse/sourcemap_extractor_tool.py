#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sourcemap_extractor_tool.py — 前端 SourceMap 源码目录树自动化还原引擎
====================================================================
作用：从 .js.map 文件或在线 URL 中直接还原出开发阶段的原始未编译前端源码 (Vue/React/TS/JS)。
"""

import sys, os, json, re, argparse
import urllib.request

def clean_source_path(raw_path):
    # 去除常见构建前缀
    p = raw_path.replace("webpack:///", "").replace("webpack://", "").replace("file://", "")
    p = p.replace("..", "__").lstrip("/\\")
    # 清洗掉不可见字符和跨平台非法符号
    p = re.sub(r'[\?\*\:\"<>\|]', '_', p)
    return p

def extract_sourcemap(content_or_path, output_dir):
    if content_or_path.startswith("http://") or content_or_path.startswith("https://"):
        print(f"[*] 正在下载在线 SourceMap: {content_or_path}")
        req = urllib.request.Request(content_or_path, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read().decode('utf-8', errors='ignore')
    else:
        print(f"[*] 读取本地 SourceMap 文件: {content_or_path}")
        data = open(content_or_path, "r", encoding="utf-8", errors="ignore").read()

    try:
        j = json.loads(data)
    except Exception as e:
        raise ValueError(f"[-] 不是合法的 JSON/SourceMap 格式: {e}")

    sources = j.get("sources", [])
    contents = j.get("sourcesContent", [])

    if not sources:
        print("[-] 未在 SourceMap 中发现任何 sources 路径字段")
        return

    if not contents:
        print("[!] 警告: 该 SourceMap 仅包含源文件索引路径，未内嵌 sourcesContent 源代码文本")
        return

    print(f"[+] 发现 {len(sources)} 个源码文件，正在还原目录树至: {output_dir}")
    os.makedirs(output_dir, exist_ok=True)

    extracted_count = 0
    for i, src_path in enumerate(sources):
        if i >= len(contents) or contents[i] is None:
            continue

        clean_path = clean_source_path(src_path)
        dest_file = os.path.join(output_dir, clean_path)

        # 保护：防止路径穿越
        if not os.path.abspath(dest_file).startswith(os.path.abspath(output_dir)):
            continue

        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
        open(dest_file, "w", encoding="utf-8", errors="ignore").write(contents[i])
        extracted_count += 1

    print(f"[🎉] 还原成功！共恢复了 {extracted_count} 个原始源码文件。")

def main():
    p = argparse.ArgumentParser(description="前端 SourceMap 自动化源码还原工具")
    p.add_argument("sourcemap", help="本地 .js.map 路径或在线 HTTP URL")
    p.add_argument("-o", "--output", default="restored_sources", help="输出还原源码的根目录 (默认: restored_sources)")
    args = p.parse_args()

    extract_sourcemap(args.sourcemap, args.output)

if __name__ == "__main__":
    main()
