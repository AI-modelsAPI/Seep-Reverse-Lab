#!/usr/bin/env bash
# ==============================================================================
#  Seep Reverse Lab — 上游同步脚本（保本地改动不丢）
# ==============================================================================
#  设计目标
#  ---------
#  本分支（vps-adaptations）在上游基础上叠加了一批 Linux/VPS 适配与安全修复。
#  直接 `git merge upstream/main` 有可能被上游改动覆盖或产生冲突。本脚本用
#  **三方合并 + 本地改动白名单** 的方式同步，保证：
#
#    · 上游新增/修改的文件 → 正常合入
#    · 本分支的改动文件   → 冲突时**一律保留本地版本**，并把上游版本另存
#                          为 *.upstream-<sha> 供人工比对
#    · 任何冲突都不会静默丢改动
#
#  原理
#  ----
#  1. 记录本地改动清单（LOCAL_FILES）——这是「必须保住」的文件集合
#  2. 备份当前工作区
#  3. fetch 上游 → 尝试 merge
#  4. 若冲突：对 LOCAL_FILES 内的冲突，取本地版；其余冲突则中止并报告
#  5. 跑测试套件验证
#
#  用法
#  ----
#    ./setup/sync-upstream.sh                  # 同步（有冲突时按策略处理）
#    ./setup/sync-upstream.sh --dry-run        # 只看会同步什么
#    ./setup/sync-upstream.sh --check          # 只报告落后多少提交
#    ./setup/sync-upstream.sh --abort          # 放弃正在进行的同步
#
#  依赖：git；远端 `upstream`（或 `origin`）指向 angusdevgo/Seep-Reverse-Lab
# ==============================================================================
set -uo pipefail

UPSTREAM_REMOTE="${UPSTREAM_REMOTE:-upstream}"
UPSTREAM_BRANCH="${UPSTREAM_BRANCH:-main}"

DRY_RUN=0; CHECK_ONLY=0; ABORT=0
for arg in "$@"; do
    case "$arg" in
        --dry-run|-n) DRY_RUN=1 ;;
        --check)      CHECK_ONLY=1 ;;
        --abort)      ABORT=1 ;;
        -h|--help)    sed -n '2,30p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
        *) echo "未知参数: $arg" >&2; exit 2 ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT"

say()  { printf '  %s\n' "$*"; }
fail() { printf '  ❌ %s\n' "$*" >&2; }

# ---------------------------------------------------------------------------
# 本地改动白名单：这些文件是本分支的核心价值，冲突时一律保留本地版。
# 新增本地改动时，把路径加到这里（或用 LOCAL_FILES_EXTRA 环境变量追加）。
# ---------------------------------------------------------------------------
LOCAL_FILES=(
    "Tool/mcp/seep_mcp_server.py"
    "Tool/prompts/extensions/security-audit-interceptor.ts"
    "Tool/prompts/extensions/load-system-prompt.ts"
    "Tool/scripts/compliance-relay/relay.py"
    "Tool/scripts/compliance-relay/refusal.py"
    "Tool/scripts/compliance-relay/tests/test_relay.py"
    "Tool/scripts/compliance-relay/tests/test_refusal.py"
    "setup/install-vps.sh"
    "setup/sync-upstream.sh"
    "README.md"
    "README.zh.md"
)
if [ -n "${LOCAL_FILES_EXTRA:-}" ]; then
    # shellcheck disable=SC2206
    LOCAL_FILES+=( ${LOCAL_FILES_EXTRA} )
fi

is_local_file() {
    local f="$1"
    for lf in "${LOCAL_FILES[@]}"; do
        [ "$f" = "$lf" ] && return 0
    done
    return 1
}

echo "================================================================================"
echo "        Seep Reverse Lab — 上游同步（保本地改动）"
echo "================================================================================"

# ------------------------------------------------------------------ abort
if [ "$ABORT" = 1 ]; then
    if [ -d .git/MERGE_HEAD ] || git rev-parse -q --verify MERGE_HEAD >/dev/null 2>&1; then
        git merge --abort && say "已放弃合并，工作区恢复到同步前状态"
    else
        say "当前没有进行中的合并"
    fi
    exit 0
fi

# ------------------------------------------------------------------ 前置检查
if ! git rev-parse --git-dir >/dev/null 2>&1; then
    fail "当前目录不是 git 仓库"; exit 1
fi
if ! git remote | grep -qx "$UPSTREAM_REMOTE"; then
    # 回退到 origin
    if git remote | grep -qx "origin"; then
        say "⚠️ 无 '$UPSTREAM_REMOTE' 远端，改用 'origin'"
        UPSTREAM_REMOTE="origin"
    else
        fail "找不到远端 '$UPSTREAM_REMOTE'，请先添加："
        say "     git remote add upstream https://github.com/angusdevgo/Seep-Reverse-Lab.git"
        exit 1
    fi
fi

BRANCH="$(git branch --show-current)"
say "分支:        $BRANCH"
say "上游远端:    $UPSTREAM_REMOTE/$UPSTREAM_BRANCH"
say "本地改动文件: ${#LOCAL_FILES[@]} 个（冲突时保留本地版）"
echo

# ------------------------------------------------------------------ fetch
echo "[1/5] 拉取上游"
if [ "$DRY_RUN" = 1 ]; then
    say "[dry] git fetch $UPSTREAM_REMOTE $UPSTREAM_BRANCH"
else
    if ! git fetch "$UPSTREAM_REMOTE" "$UPSTREAM_BRANCH" 2>&1 | tail -3; then
        fail "fetch 失败（检查网络 / 代理 / 远端地址）"; exit 1
    fi
fi

UP_REF="$UPSTREAM_REMOTE/$UPSTREAM_BRANCH"
if ! git rev-parse -q --verify "$UP_REF" >/dev/null 2>&1; then
    fail "找不到 $UP_REF"; exit 1
fi

BEHIND="$(git rev-list --count "HEAD..$UP_REF" 2>/dev/null || echo '?')"
AHEAD="$(git rev-list --count "$UP_REF..HEAD" 2>/dev/null || echo '?')"
say "本地落后上游: $BEHIND 个提交"
say "本地领先上游: $AHEAD 个提交（本分支的适配改动）"
echo

if [ "$CHECK_ONLY" = 1 ]; then
    if [ "$BEHIND" != "0" ] && [ "$BEHIND" != "?" ]; then
        echo "  待同步的上游提交："
        git log --oneline "HEAD..$UP_REF" | head -20 | sed 's/^/    /'
    else
        say "✓ 已是最新"
    fi
    exit 0
fi

if [ "$BEHIND" = "0" ]; then
    say "✓ 已是最新，无需同步"
    exit 0
fi

# ------------------------------------------------------------------ 工作区检查
echo "[2/5] 检查工作区"
if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
    fail "工作区有未提交改动，请先提交或 stash："
    git status --short --untracked-files=no | head -10 | sed 's/^/    /'
    exit 1
fi
say "工作区干净"
echo

# ------------------------------------------------------------------ 备份
echo "[3/5] 备份当前状态"
BK=".git/sync-backup-$(date +%Y%m%d-%H%M%S)"
if [ "$DRY_RUN" = 1 ]; then
    say "[dry] git bundle 备份到 $BK"
else
    mkdir -p "$BK"
    git bundle create "$BK/repo.bundle" --all >/dev/null 2>&1 && \
        say "已备份: $BK/repo.bundle" || say "⚠️ bundle 备份失败（继续，git 本身有 reflog）"
    git rev-parse HEAD > "$BK/HEAD.txt"
    say "HEAD: $(cat "$BK/HEAD.txt" | cut -c1-10)"
fi
echo

# ------------------------------------------------------------------ 合并
echo "[4/5] 三方合并"
if [ "$DRY_RUN" = 1 ]; then
    say "[dry] git merge $UP_REF（冲突时对白名单文件保留本地版）"
    exit 0
fi

if git merge --no-edit "$UP_REF" >/tmp/sync-merge.log 2>&1; then
    say "✓ 合并成功，无冲突"
else
    say "检测到冲突，按白名单策略处理…"
    CONFLICTS="$(git diff --name-only --diff-filter=U)"
    [ -z "$CONFLICTS" ] && { fail "合并失败但无冲突文件，见 /tmp/sync-merge.log"; exit 1; }

    KEPT_LOCAL=(); TAKEN_UP=(); UNRESOLVED=()
    for f in $CONFLICTS; do
        if is_local_file "$f"; then
            # 保留本地版；把上游版另存供比对
            UP_SHA="$(git rev-parse --short "$UP_REF")"
            git show "$UP_REF:$f" > "$f.upstream-$UP_SHA" 2>/dev/null || true
            git checkout --ours -- "$f" 2>/dev/null || true
            git add "$f"
            KEPT_LOCAL+=("$f")
        else
            UNRESOLVED+=("$f")
        fi
    done

    if [ "${#UNRESOLVED[@]}" -gt 0 ]; then
        fail "以下文件冲突且不在白名单，需人工处理："
        printf '    %s\n' "${UNRESOLVED[@]}"
        echo
        say "选项："
        say "  a) 人工解决后 git add <file> && git commit"
        say "  b) 放弃本次同步: ./setup/sync-upstream.sh --abort"
        say "  c) 若确认可接受上游版: git checkout --theirs -- <file> && git add <file>"
        exit 1
    fi

    # 白名单冲突全部按本地处理，完成提交
    if git commit --no-edit >/dev/null 2>&1; then
        say "✓ 合并完成（白名单文件已保留本地版）"
    else
        fail "提交失败，请检查 git status"; exit 1
    fi

    echo
    say "保留本地版的文件（上游版本已另存为 *.upstream-*）："
    for f in "${KEPT_LOCAL[@]}"; do
        echo "    $f"
        [ -f "$f.upstream-"* ] 2>/dev/null && ls "$f".upstream-* 2>/dev/null | sed 's/^/      上游版: /'
    done
fi
echo

# ------------------------------------------------------------------ 验证
echo "[5/5] 验证"
if [ -d Tool/scripts/compliance-relay/tests ]; then
    if (cd Tool/scripts/compliance-relay && python3 -m unittest discover -s tests >/tmp/sync-test.log 2>&1); then
        say "✓ relay 测试套件通过"
        tail -3 /tmp/sync-test.log | sed 's/^/    /'
    else
        fail "relay 测试失败，见 /tmp/sync-test.log"
        say "回滚: ./setup/sync-upstream.sh --abort 或 git reset --hard $BK/HEAD.txt"
        exit 1
    fi
fi

echo
echo "================================================================================"
say "✅ 同步完成"
echo "================================================================================"
say "备份位置: $BK"
say "查看本次同步的上游改动: git log --oneline HEAD@{1}..HEAD"
say "如需回退: git reset --hard \$(cat $BK/HEAD.txt)"
echo "================================================================================"
