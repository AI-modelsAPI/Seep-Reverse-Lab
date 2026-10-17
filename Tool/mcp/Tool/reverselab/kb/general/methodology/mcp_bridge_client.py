#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mcp_bridge_client.py — 远程 MCP 桥接设备群通用客户端
=====================================================================
作用：在无 adb / 无真机的沙箱里，通过远程 MCP 桥接器（arena-bridge 等）
      列设备、跑命令、推送二进制、安装 APK、抓日志/截图。

用法:
  # 1) 列出所有可用工具（看清有哪几台设备）
  python3 mcp_bridge_client.py --hub <URL> --token <TOKEN> list

  # 2) 调用任意工具
  python3 mcp_bridge_client.py --hub <URL> --token <TOKEN> call android__sysinfo
  python3 mcp_bridge_client.py --hub <URL> --token <TOKEN> call android__adb_shell \
      --args '{"command":"pm list packages | grep pwnme"}'

  # 3) 推送本地文件到真机（base64）
  python3 mcp_bridge_client.py --hub <URL> --token <TOKEN> push \
      ./patched.apk android__write_file_base64 /sdcard/Download/patched.apk

  # 4) 拉起安装器
  python3 mcp_bridge_client.py --hub <URL> --token <TOKEN> call android__open \
      --args '{"target":"/sdcard/Download/patched.apk"}'
"""

import sys, os, json, base64, argparse, urllib.request, urllib.error

DEFAULT_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"


class McpBridgeClient:
    def __init__(self, hub_url, token, timeout=90):
        self.url = hub_url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            # 关键：Accept 必须含 event-stream，否则 406
            "Accept": "application/json, text/event-stream",
            # 关键：UA 必须是正常浏览器，否则 Cloudflare 403/1010
            "User-Agent": DEFAULT_UA,
        }
        self.timeout = timeout
        self._inited = False

    def _rpc(self, method, params=None):
        payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}}
        req = urllib.request.Request(
            self.url, data=json.dumps(payload).encode("utf-8"),
            headers=self.headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.read().decode('utf-8', 'ignore')[:400]}"}
        except Exception as e:
            return {"error": str(e)}

    def initialize(self):
        if not self._inited:
            r = self._rpc("initialize", {
                "protocolVersion": "2024-11-05", "capabilities": {},
                "clientInfo": {"name": "pi-agent", "version": "1.0.0"}})
            self._inited = True
            return r
        return {"ok": True, "cached": True}

    def list_tools(self):
        self.initialize()
        return self._rpc("tools/list")

    def call(self, name, arguments=None):
        self.initialize()
        return self._rpc("tools/call", {"name": name, "arguments": arguments or {}})

    def push_file(self, local_path, tool_name="android__write_file_base64", remote_path=None):
        remote_path = remote_path or ("/sdcard/Download/" + os.path.basename(local_path))
        data = open(local_path, "rb").read()
        b64 = base64.b64encode(data).decode("ascii")
        print(f"[*] 推送 {local_path} ({len(data)} bytes) -> {remote_path}")
        return self.call(tool_name, {"path": remote_path, "data": b64})


def _print(res, maxlen=2000):
    text = json.dumps(res, indent=2, ensure_ascii=False)
    print(text[:maxlen])
    if len(text) > maxlen:
        print(f"... [truncated, total {len(text)} chars]")
    # 审批门友好提示
    if isinstance(res, dict) and res.get("pendingApproval"):
        print(f"\n⚠️  需要机主审批 (rid={res['pendingApproval']})：请在 Telegram 点批准后，"
              f"用完全相同的参数重发本条命令。")


def main():
    p = argparse.ArgumentParser(description="远程 MCP 桥接设备群客户端")
    p.add_argument("--hub", required=True, help="MCP 桥接 URL，如 https://host/mcp")
    p.add_argument("--token", required=True, help="Bearer Token")
    p.add_argument("--timeout", type=int, default=90)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="握手 + 打印 serverInfo")
    sub.add_parser("list", help="列出所有可用工具")

    c = sub.add_parser("call", help="调用工具")
    c.add_argument("tool")
    c.add_argument("--args", default="{}", help="JSON 参数")

    pu = sub.add_parser("push", help="推送本地文件到真机 (base64)")
    pu.add_argument("local")
    pu.add_argument("tool", nargs="?", default="android__write_file_base64")
    pu.add_argument("remote", nargs="?", default=None)

    a = p.parse_args()
    cli = McpBridgeClient(a.hub, a.token, a.timeout)

    if a.cmd == "init":
        _print(cli.initialize())
    elif a.cmd == "list":
        res = cli.list_tools()
        tools = res.get("result", {}).get("tools", [])
        if tools:
            from collections import defaultdict
            groups = defaultdict(list)
            for t in tools:
                nm = t.get("name", "")
                if "__" in nm:
                    dev, short = nm.split("__", 1)
                else:
                    dev, short = "(hub)", nm
                groups[dev].append(short)
            print(f"[+] 共 {len(tools)} 个工具，设备分组：")
            for dev, names in sorted(groups.items()):
                print(f"  [{dev}] ({len(names)}) {', '.join(sorted(names))}")
        else:
            _print(res)
    elif a.cmd == "call":
        _print(cli.call(a.tool, json.loads(a.args)))
    elif a.cmd == "push":
        _print(cli.push_file(a.local, a.tool, a.remote))


if __name__ == "__main__":
    main()
