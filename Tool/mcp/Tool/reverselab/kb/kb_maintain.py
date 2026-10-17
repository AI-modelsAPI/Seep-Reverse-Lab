#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kb_maintain.py — ReverseLab 知识库维护工具
============================================
设计原则：只做确定性的事（生成/校验），不做内容改写。

命令:
  --check          只读诊断：漂移/孤儿/重复/证据缺失/时效
  --sync-index     重建 README + kb-index.json（幂等）
  --signals        生成 signals-master.md（信号 → 文档映射总表）
  --evidence-stats 证据等级统计
  --all            依次执行 sync-index + signals + check

用法:
  python3 kb_maintain.py --check
  python3 kb_maintain.py --all
"""
import os, re, sys, json, glob, argparse, hashlib
from collections import Counter, defaultdict
from datetime import datetime

KB = os.environ.get("KB_DIR",
      "/opt/Seep-Reverse-Lab/Tool/mcp/Tool/reverselab/kb")

# ── 分类目录 → 中文名（用于 README 生成） ──
CATEGORY_NAMES = {
    "01-triage": "初筛",
    "02-pe-structure": "PE 结构",
    "02-native": "Native",
    "03-static-analysis": "静态分析",
    "03-manifest": "Manifest",
    "04-dynamic-analysis": "动态分析",
    "04-crypto": "加密",
    "05-crypto-unpack": "加密/内存转储与还原解包",
    "05-network": "网络",
    "06-ioc-extraction": "IOC 提取",
    "06-dynamic": "动态",
    "07-yara-sigma": "YARA/Sigma",
    "07-packer": "壳",
    "08-patch": "Patch",
    "08-patch-repack": "补丁/重打包",
    "09-av-evasion": "AI 检测签名分析与规避",
    "01-dex-java": "DEX/Java",
    "27-js-reverse": "前端 JS/AST 逆向与补环境",
}

# ═══════════════════════════════════════════════
# 基础设施
# ═══════════════════════════════════════════════
def all_md():
    return sorted(glob.glob(os.path.join(KB, "**", "*.md"), recursive=True))

def read(f):
    return open(f, encoding="utf-8", errors="ignore").read()

def parse_fm(txt):
    """解析 YAML front-matter 为 dict（轻量，不依赖 pyyaml）"""
    if not txt.startswith("---"):
        return {}
    parts = txt.split("---", 2)
    if len(parts) < 3:
        return {}
    fm, out, cur_key, cur_list = parts[1], {}, None, None
    for line in fm.splitlines():
        if re.match(r'^\s*-\s+', line) and cur_key:
            cur_list = out.setdefault(cur_key, [])
            cur_list.append(re.sub(r'^\s*-\s+', '', line).strip().strip('"\''))
            continue
        m = re.match(r'^([A-Za-z_][\w-]*):\s*(.*)$', line)
        if m:
            cur_key, val = m.group(1), m.group(2).strip()
            if val in (">", "|", ">-", "|-"):
                out[cur_key] = ""
            elif val:
                out[cur_key] = val.strip('"\'')
            else:
                out[cur_key] = []
    return out

def title_of(f, txt):
    fm = parse_fm(txt)
    if fm.get("title"):
        return fm["title"]
    for line in txt.splitlines()[:60]:
        if line.startswith("# "):
            return line[2:].strip()
    return os.path.splitext(os.path.basename(f))[0]

def evidence_of(txt):
    fm = parse_fm(txt)
    return fm.get("evidence", "")

# ═══════════════════════════════════════════════
# --check : 只读诊断
# ═══════════════════════════════════════════════
def cmd_check():
    mds = all_md()
    print(f"KB: {KB}")
    print(f"文档总数: {len(mds)}\n")

    # 1) front-matter / evidence
    has_fm = ev = 0
    ev_vals = Counter()
    missing_ev = []
    for f in mds:
        txt = read(f)
        if txt.startswith("---"):
            has_fm += 1
            e = evidence_of(txt)
            if e:
                ev += 1; ev_vals[e] += 1
            else:
                missing_ev.append(f)
        else:
            missing_ev.append(f)
    print("=" * 56); print("1. FRONT-MATTER / EVIDENCE"); print("=" * 56)
    print(f"  front-matter : {has_fm}/{len(mds)}")
    print(f"  evidence     : {ev}/{len(mds)}  {dict(ev_vals)}")
    print(f"  缺 evidence  : {len(missing_ev)} 篇")

    # 2) 索引漂移
    print("\n" + "=" * 56); print("2. 索引漂移（README 声称 vs 实际）"); print("=" * 56)
    drift = False
    for d in ["apk-reverse", "pe-reverse", "ctf-website", "general", "windows"]:
        rp = os.path.join(KB, d, "README.md")
        if not os.path.exists(rp):
            print(f"  {d:14s} — 无 README"); continue
        txt = read(rp)
        nums = re.findall(r'(\d+)\s*篇', txt)
        claimed = int(nums[0]) if nums else -1
        actual = len(glob.glob(os.path.join(KB, d, "**", "*.md"), recursive=True))
        mark = "✅" if claimed == actual else "⚠️"
        if claimed != actual: drift = True
        print(f"  {mark} {d:14s} 声称={claimed:4d}  实际={actual:4d}  差={actual-claimed:+d}")
    print(f"  漂移状态: {'⚠️ 存在' if drift else '✅ 一致'}")

    # 3) kb-index.json 有效性
    print("\n" + "=" * 56); print("3. KB-INDEX 信号路由"); print("=" * 56)
    for idx in glob.glob(os.path.join(KB, "**", "kb-index.json"), recursive=True):
        try:
            j = json.load(open(idx, encoding="utf-8"))
            ents = j.get("entries", [])
            nsig = sum(len(e.get("signals", [])) for e in ents)
            base = os.path.dirname(idx)
            missing = [f for e in ents for f in e.get("files", [])
                       if not os.path.exists(os.path.join(base, f))]
            print(f"  {os.path.relpath(idx, KB)}: {len(ents)} 类, {nsig} 信号"
                  + (f"  ⚠️ 失效映射 {missing}" if missing else "  ✅"))
        except Exception as ex:
            print(f"  {idx}: ⚠️ 解析失败 {ex}")

    # 4) 潜在重复
    print("\n" + "=" * 56); print("4. 潜在重复（标题 Jaccard > 0.6）"); print("=" * 56)
    titles = [(f, title_of(f, read(f))) for f in mds]
    def toks(s): return set(re.findall(r'[a-zA-Z\u4e00-\u9fff]{2,}', s.lower()))
    dups = []
    for i in range(len(titles)):
        for j in range(i + 1, len(titles)):
            a, b = toks(titles[i][1]), toks(titles[j][1])
            if not a or not b: continue
            jac = len(a & b) / len(a | b)
            if jac > 0.6:
                dups.append((round(jac, 2), os.path.relpath(titles[i][0], KB),
                             os.path.relpath(titles[j][0], KB)))
    dups.sort(reverse=True)
    print(f"  相似标题对: {len(dups)}")
    for jac, a, b in dups[:12]:
        print(f"    {jac}  {a}")
        print(f"           {b}")

    # 5) 时效
    print("\n" + "=" * 56); print("5. 时效分布"); print("=" * 56)
    months = Counter()
    for f in mds:
        m = re.search(r'last_updated:\s*["\']?(\d{4})-(\d{2})', read(f))
        if not m:
            m = re.search(r'field_journal_(\d{4})-(\d{2})', os.path.basename(f))
        if m: months[f"{m.group(1)}-{m.group(2)}"] += 1
    for k in sorted(months):
        print(f"  {k}  {months[k]:3d}  {'█' * min(months[k], 60)}")
    if months:
        latest = max(months)
        stale = [f for f in mds
                 if (lambda mm: mm and mm.group(0) and mm.group(0) < "2026-04")(re.search(r'(\d{4})-(\d{2})', read(f)[:2000].replace(" ", "")))]
        print(f"  最新: {latest}   超过 6 个月未更新: {len(stale)} 篇")
    return 0

# ═══════════════════════════════════════════════
# --sync-index : 重建 README + kb-index
# ═══════════════════════════════════════════════
def cmd_sync_index():
    print("=" * 56); print("SYNC-INDEX: 重建分类 README"); print("=" * 56)
    for d in ["apk-reverse", "pe-reverse", "ctf-website", "general"]:
        tdir = os.path.join(KB, d, "techniques")
        if not os.path.isdir(tdir):
            continue
        # 收集分类子目录
        cats = {}
        for sub in sorted(os.listdir(tdir)):
            subp = os.path.join(tdir, sub)
            if not os.path.isdir(subp): continue
            files = sorted(glob.glob(os.path.join(subp, "*.md")))
            if files: cats[sub] = files
        total = sum(len(v) for v in cats.values())
        lines = [f"# {d} 技术库目录", "",
                 f"> 本目录由 `kb_maintain.py --sync-index` 自动生成（{datetime.now():%Y-%m-%d}）",
                 f"> 共 {len(cats)} 类 / {total} 篇", "",
                 "## 完整目录", ""]
        for sub, files in cats.items():
            name = CATEGORY_NAMES.get(sub, sub.split("-", 1)[-1])
            lines.append(f"### {sub} — {name}（{len(files)}）")
            lines.append("")
            for f in files:
                rel = os.path.relpath(f, tdir).replace("\\", "/")
                t = title_of(f, read(f))
                # 去掉文件名前缀数字
                t = re.sub(r'^\d+[-\s]*', '', t)
                lines.append(f"- [`{rel}`]({rel}) — {t}")
            lines.append("")
        out = os.path.join(tdir, "README.md")
        open(out, "w", encoding="utf-8").write("\n".join(lines))
        print(f"  ✅ {os.path.relpath(out, KB)}  ({len(cats)} 类 / {total} 篇)")

    # 更新各分类 README 的声称篇数
    print("\n  更新分类 README 篇数:")
    for d in ["apk-reverse", "pe-reverse", "ctf-website", "general", "windows"]:
        rp = os.path.join(KB, d, "README.md")
        if not os.path.exists(rp): continue
        actual = len(glob.glob(os.path.join(KB, d, "**", "*.md"), recursive=True))
        txt = read(rp)
        new = re.sub(r'(\d+)\s*篇', f'{actual} 篇', txt, count=1)
        if new != txt:
            open(rp, "w", encoding="utf-8").write(new)
            print(f"    ✅ {d}/README.md → {actual} 篇")
        else:
            print(f"    -  {d}/README.md 无变化")
    return 0

# ═══════════════════════════════════════════════
# --signals : 生成 signals-master.md
# ═══════════════════════════════════════════════
def cmd_signals():
    print("=" * 56); print("SIGNALS: 生成信号总表"); print("=" * 56)
    sig2docs = defaultdict(set)
    sig2cat = defaultdict(set)
    # 策略 A（精确）：文档自身 front-matter 的 signals → 该文档
    for f in all_md():
        txt = read(f)
        fm = parse_fm(txt)
        rel = os.path.relpath(f, KB).replace("\\", "/")
        board = rel.split("/")[0]
        sigs = fm.get("signals") or []
        if isinstance(sigs, str):
            sigs = [sigs]
        for s in sigs:
            k = s.strip().lower()
            if k:
                sig2docs[k].add(rel)
                sig2cat[k].add(board)
    # 策略 B（兜底）：kb-index.json 分类级映射（仅当文档无 signals 时补充）
    for idx in glob.glob(os.path.join(KB, "**", "kb-index.json"), recursive=True):
        board = os.path.relpath(idx, KB).split(os.sep)[0]
        try:
            j = json.load(open(idx, encoding="utf-8"))
        except Exception:
            continue
        base = os.path.dirname(idx)
        for e in j.get("entries", []):
            eid = e.get("id", "?")
            files = [os.path.relpath(os.path.join(base, f), KB).replace("\\", "/")
                     for f in e.get("files", [])]
            for s in e.get("signals", []):
                k = s.strip().lower()
                for rel in files:
                    if rel not in sig2docs.get(k, set()):
                        sig2docs[k].add(rel)
                        sig2cat[k].add(f"{board}/{eid}")
    print(f"  唯一信号数: {len(sig2docs)}")
    # 生成文档
    lines = ["# 逆向信号 → 文档映射总表（自动生成）", "",
             f"> 生成: {datetime.now():%Y-%m-%d %H:%M}  |  由 `kb_maintain.py --signals` 产生",
             f"> 唯一信号: {len(sig2docs)}  |  覆盖文档: {len(set().union(*sig2docs.values())) if sig2docs else 0}",
             "",
             "## 用法", "",
             "```",
             "seep_kb_search(query=\"<信号关键词>\")   # 检索",
             "seep_kb_read(\"<文档路径>\")             # 读全文",
             "# 或直接查本表 → 拿到文档路径",
             "```", "",
             "## 信号索引", "",
             "| 信号 | 分类 | 文档 |", "|---|---|---|"]
    for s in sorted(sig2docs):
        cats = ", ".join(sorted(sig2cat[s])[:3])
        docs = "<br>".join(sorted(sig2docs[s])[:3])
        lines.append(f"| `{s}` | {cats} | {docs} |")
    out = os.path.join(KB, "signals-master.md")
    open(out, "w", encoding="utf-8").write("\n".join(lines))
    print(f"  ✅ 写入 {os.path.relpath(out, KB)}  ({len(sig2docs)} 信号)")
    return 0

# ═══════════════════════════════════════════════
# --evidence-stats
# ═══════════════════════════════════════════════
def cmd_evidence_stats():
    mds = all_md()
    c = Counter()
    for f in mds:
        e = evidence_of(read(f)) or "MISSING"
        c[e] += 1
    print("证据等级统计:")
    for k, v in c.most_common():
        print(f"  {k:12s} {v:3d}")
    return 0

# ═══════════════════════════════════════════════
def main():
    ap = argparse.ArgumentParser(description="ReverseLab KB 维护工具")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--sync-index", action="store_true")
    ap.add_argument("--signals", action="store_true")
    ap.add_argument("--evidence-stats", action="store_true")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    if a.all:
        cmd_sync_index(); print(); cmd_signals(); print(); cmd_check()
    elif a.check: cmd_check()
    elif a.sync_index: cmd_sync_index()
    elif a.signals: cmd_signals()
    elif a.evidence_stats: cmd_evidence_stats()
    else:
        ap.print_help()

if __name__ == "__main__":
    sys.exit(main())
