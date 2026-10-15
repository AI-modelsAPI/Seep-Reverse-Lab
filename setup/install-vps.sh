#!/usr/bin/env bash
# ==============================================================================
#  Seep Reverse Lab — VPS / Linux 服务器部署脚本
# ==============================================================================
#  与上游 setup/install.sh 的差异（上游脚本面向 Windows / 桌面，在纯 Linux
#  服务器上存在三处硬缺陷，本脚本已全部修正）：
#
#   1. mcp.json 模板使用 Windows 反斜杠路径（<SEEP_ROOT>\\Tool\\mcp\\...），
#      上游用 sed 只替换占位符，Linux 下产出非法路径 → 本脚本直接生成
#      正斜杠 JSON，并用 python3 而非 python。
#   2. pip install 会被 PEP 668 (EXTERNALLY-MANAGED) 拒绝 → 本脚本检测后
#      自动加 --break-system-packages，或提示改用 venv。
#   3. 内置 radare2/bin 是 Windows PE，Linux 下不可执行 → 本脚本探测系统
#      radare2，缺失时提示用包管理器安装（不静默失败）。
#
#  用法：
#    ./setup/install-vps.sh              # 完整部署
#    ./setup/install-vps.sh --dry-run    # 只显示将做什么
#    ./setup/install-vps.sh --skip-pip   # 跳过 Python 依赖安装
#    ./setup/install-vps.sh --with-relay # 额外安装 compliance-relay systemd 服务
#
#  幂等：可重复执行，已存在的项会跳过而非报错。
# ==============================================================================
set -uo pipefail

DRY_RUN=0; SKIP_PIP=0; WITH_RELAY=0
for arg in "$@"; do
    case "$arg" in
        --dry-run|-n)  DRY_RUN=1 ;;
        --skip-pip)    SKIP_PIP=1 ;;
        --with-relay)  WITH_RELAY=1 ;;
        -h|--help)     sed -n '2,26p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
        *) echo "未知参数: $arg" >&2; exit 2 ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TOOL_DIR="$ROOT/Tool"
SAFE_DIR="$TOOL_DIR/mcp/Tool/safe"
AGENT_DIR="${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}"
EXT_DIR="$AGENT_DIR/extensions"
SKILLS_DIR="$AGENT_DIR/skills"

say()  { printf '  %s\n' "$*"; }
run()  { if [ "$DRY_RUN" = 1 ]; then printf '  [dry] %s\n' "$*"; else "$@"; fi; }
fail() { printf '  ❌ %s\n' "$*" >&2; }

echo "================================================================================"
echo "        Seep Reverse Lab — VPS / Linux 部署管线"
echo "================================================================================"
say "工作台根目录:   $ROOT"
say "Agent 目标目录: $AGENT_DIR"
[ "$DRY_RUN" = 1 ] && say "模式: DRY-RUN（不做任何改动）"
echo

# ---------------------------------------------------------------- 1. 环境探测
echo "[1/6] 检查运行环境"
if ! command -v python3 >/dev/null 2>&1; then
    fail "未检测到 python3，请先安装 Python 3.11+"; exit 1
fi
PY_VER="$(python3 -c 'import sys;print("%d.%d"%sys.version_info[:2])')"
say "python3 $PY_VER"
command -v node >/dev/null 2>&1 && say "node $(node -v)" || say "⚠️ 未检测到 node（js-reverse / playwright MCP 将不可用）"
command -v unzip >/dev/null 2>&1 || { fail "缺少 unzip，请先安装"; exit 1; }
say "unzip 就绪"

# ---------------------------------------------------------------- 2. 离线依赖
echo
echo "[2/6] 解压内置离线依赖"
for mod in js-reverse-mcp playwright-mcp; do
    target="$SAFE_DIR/$mod/node_modules"
    zip="$SAFE_DIR/$mod/node_modules.zip"
    if [ -d "$target" ]; then
        say "[跳过] $mod/node_modules 已存在"
    elif [ -f "$zip" ]; then
        run unzip -q -o "$zip" -d "$SAFE_DIR/$mod/"
        say "[完成] $mod 依赖解压"
    else
        say "[跳过] $mod 无 node_modules.zip"
    fi
done

# ---------------------------------------------------------------- 3. 执行权限
echo
echo "[3/6] 配置执行权限 / 探测 radare2"
[ -d "$SAFE_DIR/radare2/bin" ] && run chmod +x "$SAFE_DIR/radare2/bin/"* 2>/dev/null
[ -f "$SAFE_DIR/jadx/bin/jadx" ] && run chmod +x "$SAFE_DIR/jadx/bin/jadx" 2>/dev/null
# 内置 radare2 是 Windows PE，Linux 不可执行；seep MCP 会回退到系统 PATH
if command -v radare2 >/dev/null 2>&1; then
    say "系统 radare2: $(radare2 -v 2>/dev/null | head -1)"
elif command -v r2 >/dev/null 2>&1; then
    say "系统 r2: $(r2 -v 2>/dev/null | head -1)"
else
    say "⚠️ 未检测到系统 radare2 —— 请执行: apt install radare2"
fi

# ---------------------------------------------------------------- 4. Python 依赖
echo
echo "[4/6] 安装 Python MCP 协议库"
if [ "$SKIP_PIP" = 1 ]; then
    say "[跳过] --skip-pip"
elif python3 -c 'import mcp' >/dev/null 2>&1; then
    say "[跳过] mcp 库已安装"
else
    PIP_ARGS=""
    if [ -f /usr/lib/python3.*/EXTERNALLY-MANAGED ] 2>/dev/null || \
       ls /usr/lib/python3*/EXTERNALLY-MANAGED >/dev/null 2>&1; then
        PIP_ARGS="--break-system-packages"
        say "检测到 PEP 668 限制，附加 --break-system-packages"
    fi
    if run python3 -m pip install "mcp>=1.20,<1.29" --quiet $PIP_ARGS; then
        say "[完成] mcp 库安装"
    else
        say "⚠️ 安装失败，可改用虚拟环境："
        say "     python3 -m venv $ROOT/.venv && $ROOT/.venv/bin/pip install 'mcp>=1.20,<1.29'"
    fi
fi

# ---------------------------------------------------------------- 5. Agent 同步
echo
echo "[5/6] 同步 Skills / 提示词 / 扩展"
run mkdir -p "$SKILLS_DIR" "$EXT_DIR"

if [ -d "$TOOL_DIR/skill" ]; then
    for s in "$TOOL_DIR/skill"/*; do
        [ -d "$s" ] || continue
        name="$(basename "$s")"
        if [ "$name" = "safe-skills" ]; then
            for sub in "$s"/*; do
                [ -d "$sub" ] || continue
                run rm -rf "$SKILLS_DIR/$(basename "$sub")"
                run cp -r "$sub" "$SKILLS_DIR/"
            done
            say "[完成] safe-skills 子技能已展开"
        elif [ "$name" != "update" ]; then
            run rm -rf "$SKILLS_DIR/$name"
            run cp -r "$s" "$SKILLS_DIR/"
            say "[完成] skill: $name"
        fi
    done
fi

for f in SYSTEM.md AGENTS.md; do
    [ -f "$TOOL_DIR/prompts/$f" ] && run cp "$TOOL_DIR/prompts/$f" "$AGENT_DIR/" && say "[完成] $f"
done

if [ -d "$TOOL_DIR/prompts/extensions" ]; then
    for f in "$TOOL_DIR/prompts/extensions"/*.ts; do
        [ -f "$f" ] && run cp "$f" "$EXT_DIR/" && say "[完成] extension: $(basename "$f")"
    done
fi

# ---------------------------------------------------------------- 6. mcp.json
echo
echo "[6/6] 生成 mcp.json（Linux 正斜杠路径）"
if [ "$DRY_RUN" = 1 ]; then
    say "[dry] 生成 $AGENT_DIR/mcp.json"
else
    python3 - "$AGENT_DIR/mcp.json" "$ROOT" "$SAFE_DIR" <<'PYGEN'
import json, os, sys
out, root, safe = sys.argv[1], sys.argv[2], sys.argv[3]

servers = {
    "seep": {
        "command": "python3",
        "args": [os.path.join(root, "Tool/mcp/seep_mcp_server.py")],
        "env": {"PYTHONIOENCODING": "utf-8"},
        "transport": "stdio",
        "lifecycle": "eager",
    },
    "playwright": {
        "command": "node",
        "args": [os.path.join(safe, "playwright-mcp/cli.js")],
        "transport": "stdio",
        "lifecycle": "lazy",
    },
}

# js-reverse: 优先用仓库内已构建产物，否则回退全局安装
js_local = os.path.join(safe, "js-reverse-mcp/build/src/index.js")
js_global = "/usr/lib/node_modules/js-reverse-mcp/build/src/index.js"
js_entry = js_local if os.path.exists(js_local) else (js_global if os.path.exists(js_global) else None)
if js_entry:
    servers["js-reverse"] = {
        "command": "node", "args": [js_entry],
        "transport": "stdio", "lifecycle": "lazy",
    }

# ida: 仅在探测到 idalib-mcp 时注册
if os.path.exists("/usr/local/bin/idalib-mcp"):
    servers["ida"] = {
        "command": "/usr/local/bin/idalib-mcp",
        "args": ["--stdio", "--unsafe"],
        "env": {
            "PYTHONIOENCODING": "utf-8",
            "PATH": "/opt/ida-pro-9.5:/usr/local/bin:/usr/bin:/bin",
        },
        "transport": "stdio",
        "lifecycle": "lazy",
    }

# 保留已有 mcp.json 中本脚本不管理的条目（增量合并，不覆盖用户配置）
existing = {}
if os.path.exists(out):
    try:
        existing = json.load(open(out, encoding="utf-8")).get("mcpServers", {}) or {}
    except Exception:
        existing = {}
for k, v in existing.items():
    if k not in servers:
        servers[k] = v

json.dump({"mcpServers": servers}, open(out, "w", encoding="utf-8"),
          indent=2, ensure_ascii=False)
print("  [完成] 已写入 %s（%d 个 MCP 服务）" % (out, len(servers)))
for k in servers:
    print("     - %s" % k)
PYGEN
fi

# ---------------------------------------------------------------- 可选：relay
if [ "$WITH_RELAY" = 1 ]; then
    echo
    echo "[附加] 安装 compliance-relay systemd 服务"
    RELAY_DIR="$TOOL_DIR/scripts/compliance-relay"
    if [ ! -f "$RELAY_DIR/relay.py" ]; then
        say "[跳过] 未找到 relay.py"
    elif [ "$DRY_RUN" = 1 ]; then
        say "[dry] 写入 /etc/systemd/system/seep-relay.service 并启动"
    else
        cat > /etc/systemd/system/seep-relay.service <<UNIT
[Unit]
Description=Seep Compliance Relay (local loopback term-rewrite gateway)
After=network.target
Wants=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$RELAY_DIR
Environment=PYTHONUNBUFFERED=1
Environment=PYTHONIOENCODING=utf-8
ExecStart=/usr/bin/python3 $RELAY_DIR/relay.py
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
UNIT
        # relay-config.json 含 token，不入库；不存在则由 relay.py 自行生成
        [ -f "$RELAY_DIR/relay-config.json" ] && chmod 600 "$RELAY_DIR/relay-config.json"
        systemctl daemon-reload
        systemctl enable --now seep-relay.service
        say "[完成] seep-relay: $(systemctl is-active seep-relay)"
        say "      端口 17890；配置文件 $RELAY_DIR/relay-config.json"
    fi
fi

echo
echo "================================================================================"
echo "  ✅ 部署完成"
echo "================================================================================"
say "工作台:  $ROOT"
say "Agent:   $AGENT_DIR"
echo
say "下一步："
say "  1. 启动 agent（pi / pi-web），在对话中发送  lab：  开启工作环境"
say "  2. 运行自检:  ./setup/verify.sh"
say "  3. 上游同步:  ./setup/sync-upstream.sh"
echo "================================================================================"
