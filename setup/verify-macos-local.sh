#!/usr/bin/env bash
# Local macOS verification wrapper: runs the upstream verifier, then probes the
# macOS-only extras (radare2 / Mono / Ghidra MCP health) that the upstream
# verifier does not know about. PATH is resolved dynamically so this file stays
# portable across machines.
set -euo pipefail

for d in "$HOME/homebrew/opt/openjdk/bin" "$HOME/homebrew/bin" "$HOME/.local/bin" \
         "/opt/homebrew/opt/openjdk/bin" "/opt/homebrew/bin" "/usr/local/bin" \
         "/Library/Frameworks/Mono.framework/Versions/Current/Commands"; do
  [ -d "$d" ] && PATH="$d:$PATH"
done
export PATH

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
bash "$ROOT/setup/verify.sh"

command -v radare2 >/dev/null && radare2 -v
command -v mono    >/dev/null && mono --version
curl --fail --silent --show-error --max-time 10 "http://127.0.0.1:${GHIDRA_MCP_PORT:-8089}/health" && echo
