---
id: "general/methodology/02-remote-mcp-device-bridge-deployment"
title: "远程 MCP 桥接设备群真机部署与交付实战手册"
title_en: "Remote MCP Bridge Fleet Deployment and Real-Device Delivery Handbook"
summary: >
  打通"沙箱分析环境 → 远程 MCP 桥接器 → 多台真实设备(mac/host/android/vps)"的
  跨设备工程闭环。涵盖 MCP-over-HTTP 协议握手(initialize/tools/list/tools/call)、
  Cloudflare 403/1010 与 HTTP 406 排错、二进制文件 base64 分块推送、
  Shizuku/rish 权限申请、Telegram 审批门(Hub Approval)处理，
  以及补丁 APK 从分析机到安卓真机的端到端交付与验收流程。
summary_en: >
  End-to-end engineering workflow bridging a sandbox analysis host to a remote MCP device fleet
  (mac/host/android/vps). Covers MCP-over-HTTP handshake, Cloudflare 403/1010 and HTTP 406 troubleshooting,
  base64 binary push, Shizuku/rish authorization, Telegram Hub-Approval gate handling, and
  real-device APK delivery/verification.
board: "general"
category: "methodology"
signals:
  - "arena-bridge"
  - "远程MCP"
  - "MCP over HTTP"
  - "tools/call"
  - "Cloudflare 1010"
  - "HTTP 406 Not Acceptable"
  - "write_file_base64"
  - "Shizuku"
  - "rish"
  - "termux-open"
  - "Hub Approval"
  - "pendingApproval"
  - "真机部署"
  - "APK 推送安装"
mcp_tools:
  - "kb_router"
difficulty: "intermediate"
tags:
  - "methodology"
  - "mcp"
  - "remote-device"
  - "android"
  - "deployment"
  - "delivery"
evidence: "verified"
validated_by: "实测于 arena-bridge v1.1.0 远程设备群，完成 r2pay-v1.0-patched.apk 真机部署验收"
language: "zh-CN"
last_updated: "2026-10-16"
related_articles:
  - "general/methodology/01-headless-emulation-windows-android-handbook"
  - "apk-reverse/08-patch-repack/01-smali-patch-repack-sign"
---
# 远程 MCP 桥接设备群真机部署与交付实战手册

## 1. 适用场景（入口信号）

分析机（沙箱 / CI / 无 GUI 服务器）**没有真机、没有模拟器**，但需要把产物（补丁 APK、Dump 文件、
POC 脚本）推到**真实设备**上运行验证。此时若有远端 MCP 桥接器，可把"分析"与"验证"两段打通。

```text
信号:
  - 用户给出 https://<hub>/mcp + Bearer <token>
  - 需要用真机验证 patched APK / 动态 POC
  - 需要读取真机 logcat / 截图 / UI 树
  - 沙箱内无法 adb（无设备、无 USB 透传）
```

**核心价值**：把"我在沙箱里改完了"变成"我在你手机上装好并跑给你看了"。

---

## 2. MCP-over-HTTP 协议握手（必读）

远程 MCP 桥接器走 **JSON-RPC 2.0 over HTTP（Streamable HTTP）**。三步入场：

```python
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",   # ← 必需，否则 406
    "User-Agent": "Mozilla/5.0",                        # ← 必需，否则 Cloudflare 1010
}
```

| 步骤 | method | 作用 |
|---|---|---|
| 1 | `initialize` | 握手，返回 `serverInfo` / `capabilities` |
| 2 | `tools/list` | 列出全部可用工具及其 JSON Schema |
| 3 | `tools/call` | 调用工具（`params.name` + `params.arguments`） |

```python
import urllib.request, json

def mcp_call(method, params=None, timeout=90):
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}}
    req = urllib.request.Request(HUB_URL, data=json.dumps(payload).encode(),
                                 headers=HEADERS, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())
```

> **工具命名规律**：`<device>__<tool>`，例如 `android__adb_shell`、`mac__browser`、
> `host__bash`、`vps__screen_ask`。**前缀即目标设备**，先 `tools/list` 看清有哪几台。

---

## 3. 三类典型报错与排错（踩坑记录）

| 现象 | 根因 | 修复 |
|---|---|---|
| `HTTP 403 (error code: 1010)` | Cloudflare 拦截 Python 默认 UA（`Python-urllib/3.x`） | 加 `User-Agent: Mozilla/5.0 ...` |
| `HTTP 406 Not Acceptable` | 缺 `Accept`，服务端要求 SSE 兼容 | 加 `Accept: application/json, text/event-stream` |
| `TimeoutError` / 长时间无响应 | 真机侧操作需唤醒 Shizuku、建链或审批 | 提升 `timeout` 到 60~90s，或改用 `start_process` 异步 |
| `rish did not answer within 20 s` | Shizuku 服务未启动 / 未授权 | 手机端打开 Shizuku 并授权；先跑 `*_shizuku_status` |
| `Waiting for Shizuku authorization...` | 敏感操作（ui_tree/input）需 Shizuku 权限 | 手机通知栏点授权 |
| `PROTECTED: waiting for the owner's approval ... pendingApproval: <rid>` | Hub 审批门 | 通知机主在 Telegram 点批准，**然后用同一 rid 重发** |

### 审批门（Hub Approval）的正确处理方式

```json
{
  "result": {
    "content": [{"type": "text", "text": "PROTECTED: waiting for the owner's approval...（request #81f9e1b0, open for 10 min）"}],
    "isError": true
  },
  "pendingApproval": "81f9e1b0"
}
```

**关键**：这不是失败，是**等机主批准**。批准后用**完全相同的请求**再发一次即可通过。
**不要**改参数重试（rid 会变，等于重新排队）。**免费操作**（`sysinfo`、`list_dir` 白名单、`net_connections`、
`notify`）不需要审批，可用来先探活。

---

## 4. 二进制文件推送（交付核心）

**没有 adb push 也能传文件**：用 `<device>__write_file_base64`，参数 `path` + `data`(base64)。

```python
import base64
data = open("patched.apk", "rb").read()
b64 = base64.b64encode(data).decode("ascii")     # 3.66MB APK → ~5.1MB base64
mcp_call("tools/call", {
    "name": "android__write_file_base64",
    "arguments": {"path": "/sdcard/Download/patched.apk", "data": b64}
})
# → {"text": "wrote 3842488 bytes to /sdcard/Download/patched.apk"}
```

**要点**：
- 写入路径优先选 **`/sdcard/Download/`**（Termux / Shizuku / adb shell 三方都能访问）；
- 若目标工具以 `adb shell`(uid 2000) 执行，**不能直接读 Termux 私有目录**；
  先用 `write_file_base64` 落到 `/sdcard/`，再在命令里 `cp /sdcard/xxx /data/local/tmp/`；
- 单次 base64 上限通常 8MB（工具说明），更大文件需分块 `append` 或用 hub `transfer`；
- 大文件推送本身可能触发审批 → 见 §3。

---

## 5. 真机安装与验证闭环

```bash
# 方式 A：静默安装（需要 Shizuku/rish，走 adb_shell）
android__adb_shell({"command": "cp /sdcard/Download/patched.apk /data/local/tmp/ && pm install -r /data/local/tmp/patched.apk"})
# 注意：pm/am/cmd 的 stdout 不能是管道或 /sdcard 上的文件，否则报 "Failed transaction (2147483646)"

# 方式 B：拉起系统安装器（无需特权，走 termux-open）
android__open({"target": "/sdcard/Download/patched.apk"})
# → {"ok": true, "via": "termux-open"}  手机上弹出 PackageInstaller，机主点确认
```

**验证手段**：
| 目的 | 工具 |
|---|---|
| 确认已安装 & 当前前台应用 | `android__ui_tree`（返回 `app` 字段，如 `re.pwnme`） |
| 看界面文字（OCR，无需授权截图） | `android__screen_text` |
| 截图（需审批） | `android__screenshot` |
| 抓崩溃/校验日志 | `android__app_logs({"package":"re.pwnme","buffer":"crash"})` |
| 模拟点击/输入 | `android__screen_action({"action":"tap"/"type", ...})` |

---

## 6. 端到端交付样例（本项目实测路径）

```text
[沙箱] r2pay-v1.0.apk  ──apktool 解包→Smali 打桩（CWE-602 决策分支放行）
                       ──apktool b → zipalign -p 4 → apksigner(v1/v2/v3)
                       → r2pay-v1.0-patched.apk (3.66MB)
        │
        ▼
[MCP] initialize → tools/list（发现 mac/host/android/vps）
        │
        ▼
[MCP] android__sysinfo          → Android 14 / arm64 / Termux 宿主
      android__shizuku_status   → installed=true（rish 需授权）
        │
        ▼
[MCP] android__write_file_base64 → /sdcard/Download/r2pay-patched.apk（3,842,488 字节校验一致）
        │
        ▼
[MCP] android__open              → PackageInstaller 拉起（via=termux-open）
        │
        ▼
[真机] 机主确认安装 → 打开 re.pwnme → 任意 PIN/金额 → 绿色放行 ✅ 验收通过
```

**回报给用户的三件套**：① 落地路径 ② 字节数/哈希一致 ③ 建议的验收操作步骤。

---

## 7. 纪律与安全边界

1. **凭据处理**：Bearer Token **仅用于目标 Hub**，不写入报告、不外发、不硬编码进仓库；用完即弃。
2. **审批即授权**：Hub 的 `pendingApproval` 机制是机主的**最终同意权**，不得绕过；
   免费/白名单操作可先探活，敏感操作老实等批。
3. **最小影响**：推送文件优先放 `/sdcard/Download/`，避免覆盖系统目录；
   卸载测试包前先确认不影响机主其他 App。
4. **可回滚**：保留原始 APK 与 patched APK，注明卸载命令 `pm uninstall <pkg>`。
