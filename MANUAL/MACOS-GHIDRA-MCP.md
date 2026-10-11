# macOS：Ghidra MCP 代替 IDA Pro

> 背景：随包分发的 `~/Downloads/IDA Pro 9.3.zip` 是 **Windows 专用绿色版**（629 个 `.exe|.dll`，0 个 Mach-O/.app），macOS 上无法运行。
> 本机改用 **Ghidra 12.1.4 + GhidraMCP 6.0.0 headless** 补上"反编译器"这一环，作为 IDA 的功能代位。

## 1. 已部署组件

| 组件 | 路径 | 说明 |
|---|---|---|
| Ghidra 12.1.4 | `~/tools/ghidra_12.1.4_PUBLIC` | macOS 原生；`decompile`/`sleigh` 原生组件缺失，已现场自编补齐 |
| GhidraMCP 6.0.0 扩展 | `.../Ghidra/Extensions/GhidraMCP/lib/GhidraMCP-6.0.0.jar` | 提供 **245 个 REST 端点** |
| headless HTTP 服务 | `~/tools/bin/ghidra-mcp-headless.sh` | 监听 `127.0.0.1:8089`（仅回环） |
| LaunchAgent | `~/Library/LaunchAgents/com.seep.ghidramcp.plist` | `RunAtLoad` + `KeepAlive`，登录自启、崩溃自拉 |
| MCP 桥（stdio） | `python3 -m bridge_mcp_ghidra` | 暴露 **222 个工具**，由 `~/.pi/agent/mcp.json` 的 `ghidra` 条目拉起 |

## 2. 服务管理

```bash
curl -s http://127.0.0.1:8089/health                 # {"status":"healthy",...}
launchctl print  gui/$(id -u)/com.seep.ghidramcp     # 查看状态
launchctl kickstart -k gui/$(id -u)/com.seep.ghidramcp   # 重启
launchctl bootout gui/$(id -u)/com.seep.ghidramcp    # 停止
tail -f ~/tools/bin/ghidra-mcp-headless.log          # 日志
```

`JAVA_HOME` 必须是 **JDK 21+**（Ghidra 12.1.4 要求），本机用 `~/homebrew/opt/openjdk`（26.0.1），已写死在包装脚本里。

## 3. HTTP API 的绑定约定（易踩坑）

参数绑定的来源由服务端 `@Param(source=...)` 注解决定，**不是** 统一按 form/query 解析：

| 端点 | 参数 | 正确传法 |
|---|---|---|
| `POST /load_program` | `file`（source=**BODY**） | `-H 'Content-Type: application/json' -d '{"file":"/abs/path"}'` |
| `POST /switch_program` | `program`（默认→**query**） | `POST "/switch_program?program=NAME"` |
| `POST /run_analysis` | 无 | `-d '{}'` + JSON 头 |

用 `file=...` 的 form 体或 query 传 `load_program` 都会返回 `{"error":"file path required"}`。

**加载 ≠ 切换**：`load_program` 只导入，当前上下文不变。要操作新程序必须再 `switch_program`（或用 `list_open_programs` 确认 `is_current`）。

```bash
API=http://127.0.0.1:8089
curl -s -X POST -H 'Content-Type: application/json' -d '{"file":"/abs/app.exe"}' "$API/load_program"
curl -s -X POST "$API/switch_program?program=app.exe"
curl -s "$API/list_functions?limit=20"
curl -s "$API/decompile_function?address=0x140001f80"
```

MCP 侧由桥接层完成同样的绑定，直接 `tools/call {"name":"decompile_function","arguments":{"address":"0x140001f80"}}` 即可。

## 4. 能力边界（重要）

- **Ghidra 只适合原生代码**（`.so` / `.elf` / Mach-O / 原生 PE）。
  .NET 程序集在 Ghidra 里走的是原生 PE 视图，真实逻辑全在 IL 字节码里 —— 实测 `BoosterX.exe`（39.6 MB，PE32 .NET/Eazfuscator）自动分析后**只识别出 2 个函数**（`.cctor` / `entry`），没有可用的 C 伪代码。
  项目N 这类 .NET 目标请走 **dnSpy / ILSpy** 路线（Mono 6.12.0.206 已安装；Windows WPF 仍不受支持，Mono 不等于现代 .NET SDK），或用工作台自己的 `bx_patch.py` 做 RVA 级微创补丁。
- 与 `seep` MCP 的分工：`seep_r2_*` 负责侦察/字符串/差分/APK；`ghidra` 负责**出 C 伪代码**（Radare2 只有 pdc，质量弱一档）。

## 5. 验收记录

| 项 | 结果 |
|---|---|
| headless 端点注册 | 245 ✅ |
| MCP `tools/list`（桥接） | 222 ✅ |
| 原生 PE 导入 + 自动分析 | `rasm2.exe` PE32+ → 357 函数 ✅ |
| C 伪代码产出 | `sdb_atoi` / `sdb_itoa` 含栈金丝雀恢复 `_DAT_140023018 ^ auStack_98` ✅ |
| 服务跨会话持久 | LaunchAgent `state=running`，pid 稳定 ✅ |
| 工作台 `setup/verify.sh` | 38 PASS / 0 FAIL / 1 OPTN ✅ |
