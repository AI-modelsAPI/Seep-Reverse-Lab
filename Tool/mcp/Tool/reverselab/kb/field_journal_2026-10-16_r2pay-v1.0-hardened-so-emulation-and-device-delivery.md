# 2026-10-16 r2pay-v1.0 现代加固靶场：无真机仿真 → Smali 打桩 → 远程 MCP 真机交付

## 场景分类

Android 逆向 / OLLVM 加固 SO / 无真实环境模拟执行 / CWE-602 客户端决策旁路 / 远程 MCP 桥接真机部署

## 目标概述

对 OWASP MASTG L4 五星靶场 `r2pay-v1.0.apk`（核心校验下沉 `libnative-lib.so`，含 OLLVM 控制流平坦化、
全局数据段加密、JNI 动态注册、RootBeer 环境对抗）执行端到端白盒审计：
① 沙箱内无设备、无模拟器，用 Unicorn 纯软件仿真跑通被隐藏的加固 Native 函数并提取加密中间态；
② 对 Java 层 CWE-602 决策分支实施 Smali 微创打桩，生成签名合规补丁 APK；
③ 通过远程 MCP 桥接器把补丁 APK 推送到真实 Android 14 设备并完成安装验收。

## 完整执行链路

1. **侦察与形态判定**：`apktool`/`jadx` 解包 → 业务包 `re.pwnme`；`libnative-lib.so` 导出表满是 `.datadiv_decode*`
   （Hikari/OLLVM 数据段解密桩），目标函数 `gXftm3iswpkVgBNDUp` **不在导出表** → 判定 JNI 动态注册。
2. **动态注册内存转储与还原解包**：解析 `JNI_OnLoad`（x86_64 VA `0x1779d0`）→ 定位 `RegisterNatives`
   调用（JNIEnv 索引 215，偏移 `0x6b8`）；在 `0x177e1a` 解析出 `JNINativeMethod` 结构体物理址 `0x317020`
   → 提取真实业务入口 **`0x1780f0`**（arm64 版为 `0x9b41c`）。
3. **纯软件仿真（Unicorn）**：映射 SO → **自动应用 `.rela.dyn` + `.rela.plt` 共 279 处重定位**（模拟 ld.so）
   → 追加执行 `.init_array` 91 个构造函数解密数据段 → 构造虚拟 JNIEnv 表（`GetArrayLength`/`GetByteArrayElements`/
   `SetByteArrayRegion`）→ 打桩 `malloc/free/calloc/memset/memcpy/rand`（Bump Allocator）
   → 配置 `MSR_FS_BASE` 绕过 `fs:[0x28]` Canary 检查。
4. **仿真结果**：输入 `PIN=1234`+`Amount=1337`、标志位 `0xF0`，成功执行 **768 万条** OLLVM 平坦化指令无异常退出；
   捕获 1727 次堆内存写入，内存中直接提取出 AES 轮密钥与加密中间态（明文输入 `0000123400001337` 可见）。
5. **Smali 打桩（CWE-602）**：
   - `MainActivity.smali`：`if-nez v1, :cond_0` → `goto :cond_1`，**抹除 `div-int/lit8 v1,v1,0x0` 自杀与 `f508` 污染**；
   - `MainActivity$θ.smali`：同法跳过点击时的 RootBeer 崩溃路径；把 `if-ne v6, 0x51, :cond_3`
     改为**无条件 `goto :cond_3`**，强制走绿色放行分支（`Color.parseColor("#10b010")`）。
6. **重打包签名**：`apktool b` → `zipalign -p 4` → `apksigner`（v1/v2/v3 全开）→
   `r2pay-v1.0-patched.apk`（3,842,488 字节，sha256 `ba8b4978...`）；反编译产物 dex 复核补丁确实落盘。
7. **远程 MCP 真机交付**：
   - 握手 `initialize` → `tools/list`（171 工具 / 4 设备：hub·android·host·mac·vps）；
   - `android__sysinfo` 确认 Android 14 / arm64 / Termux 宿主；`android__shizuku_status` 探测权限；
   - `android__write_file_base64` 推送 → `/sdcard/Download/r2pay-patched.apk`（字节数一致）；
   - `android__open` 拉起系统安装器（`via: termux-open`）→ 机主确认安装 → 打开 `re.pwnme`
     → 任意 PIN/金额点击 PAY → **绿色放行，真机验收通过**。

## 踩坑记录

| 问题 | 原因 | 解决方案 | 耗时 |
|---|---|---|---|
| Linux `ctypes.CDLL` 加载 SO 失败 `libm.so: invalid ELF header` | Debian 的 `libm.so` 是 GNU ld 文本链接脚本，非 ELF | 放弃宿主加载，改走 Unicorn 纯指令仿真 | 低 |
| 仿真崩在 `0x578118`（读 `fs:[0x28]`） | 未配置 TLS 段基址，Canary 检查触发 UNMAPPED | `mem_map(0x100000)` + `reg_write(UC_X86_REG_FS_BASE, ...)` | 低 |
| 仿真崩在 `0x6166`/`0x60a6`（PLT 桩） | GOT 未重定位，跳回 PLT resolver | 打桩 `memset/memcpy/malloc/free/calloc/rand` 到 GOT 条目 | 中 |
| 多次 `malloc` 返回同址导致结构体互踩（`rdx=0xfa92bd9d` 乱码） | 打桩用固定基址 | 改用 **Bump Allocator**（Python 钩子动态递增堆指针） | 中 |
| 崩在 `0x57874c` 读 `[0x28ba30]=0` | **漏了 `.rela.plt`**，只处理了 `.rela.dyn` | 同时遍历两段；`R_X86_64_GLOB_DAT(6)`/`JUMP_SLOT(7)` 填 `SO_BASE+sym.st_value` | 高 |
| `.init_array` 执行后全局变量仍未解密 | 重定位已把函数指针加了基数，代码又加一次 `SO_BASE`（双加） | `target_va = func_ptr` 直接用（勿重复加基址） | 中 |
| MCP `HTTP 403 (error code: 1010)` | Cloudflare 拦截 Python 默认 UA | 加 `User-Agent: Mozilla/5.0 ...` | 低 |
| MCP `HTTP 406 Not Acceptable` | 缺 SSE 兼容 Accept 头 | 加 `Accept: application/json, text/event-stream` | 低 |
| `PROTECTED: waiting for the owner's approval` | Hub 审批门（机主 Telegram 确认） | 等机主批准后**用同一 rid 重发**，不改参数 | 低 |
| `rish did not answer within 20 s` | Shizuku 未启动/未授权 | 手机端启动 Shizuku 并授权；先跑 `shizuku_status` | 低 |

## 工具链发现

- **Unicorn 是"无设备逆向"的终极兜底**：宿主 glibc 不兼容、无 Android 运行时，都能靠纯指令仿真绕开；
  前提是**自己实现动态链接器的三件事**——重定位（.rela.dyn + .rela.plt）、初始化（.init_array）、
  TLS/Canary（FS base）。
- **OLLVM 数据段加密（`.datadiv_decode`）靠 `.init_array` 解密**：跳过初始化就会读到密文假地址
  （如 `0xfa91b9cd`），必须按序执行全部构造函数。
- **JNI 动态注册 = 静态可解**：`RegisterNatives` 的 `JNINativeMethod*` 常以 `lea rdx,[rip+disp]` 直接给出
  静态地址，无需动态跑就能拿到真实函数指针。
- **MCP-over-HTTP 三件套**：`initialize`/`tools/list`/`tools/call`；`Accept` 与 `User-Agent` 两个头是
  Cloudflare 与 SSE 兼容的硬门槛。
- **没有 adb 也能装 APK**：`write_file_base64` 落到 `/sdcard/Download/` + `termux-open` 拉起系统安装器。

## 关键代码/命令

```python
# 1) 自动应用 ELF 重定位（.rela.dyn + .rela.plt），模拟 ld.so
for sec_name in ['.rela.dyn', '.rela.plt']:
    sec = elf.get_section_by_name(sec_name)
    for reloc in sec.iter_relocations():
        t, off, add = reloc['r_info_type'], reloc['r_offset'], reloc['r_addend']
        if t == 8:                      # R_X86_64_RELATIVE
            mu.mem_write(SO_BASE + off, struct.pack('<Q', SO_BASE + add))
        elif t in (6, 7):               # GLOB_DAT / JUMP_SLOT
            sym = dynsym.get_symbol(reloc['r_info_sym'])
            if sym['st_value']:
                mu.mem_write(SO_BASE + off, struct.pack('<Q', SO_BASE + sym['st_value'] + add))

# 2) 执行 .init_array 解密数据段（注意：重定位后指针已含基址，勿重复加）
for i in range(0x2d8 // 8):
    fp = struct.unpack('<Q', mu.mem_read(SO_BASE + 0x28b248 + i*8, 8))[0]
    if fp:
        mu.emu_start(fp, SENTINEL_RET, timeout=1_000_000)

# 3) TLS/Canary
mu.mem_map(0x100000, 0x1000); mu.reg_write(UC_X86_REG_FS_BASE, 0x100000)
mu.mem_write(0x100028, struct.pack('<Q', 0x1122334455667788))
```

```smali
# 4) CWE-602 决策分支强制放行
-    if-ne v6, v8, :cond_3
+    # [PATCH CWE-602] 强制特权放行
+    goto :cond_3
```

```python
# 5) 远程 MCP 推送 + 安装
mcp_call("tools/call", {"name": "android__write_file_base64",
    "arguments": {"path": "/sdcard/Download/patched.apk",
                  "data": base64.b64encode(open("patched.apk","rb").read()).decode()}})
mcp_call("tools/call", {"name": "android__open",
    "arguments": {"target": "/sdcard/Download/patched.apk"}})
```

## 产出与指标

- 补丁 APK：`r2pay-v1.0-patched.apk`（3,842,488 字节，sha256 `ba8b49783f8798b0...`），v1/v2/v3 签名全通过。
- 仿真规模：单次无异常执行 **768 万条** OLLVM 平坦化指令，捕获 1727 次堆加密写入。
- 真机结果：Android 14 / arm64 设备安装成功，任意输入点击 PAY → 绿色放行 ✅。
- 报告：`android/逆向r2pay-v1.0/patch_workspace/AUDIT_REPORT.md`（三栏：原理/复现/纵深防御）。

## 沉淀

- 通用技术 → `kb/general/methodology/02-remote-mcp-device-bridge-deployment.md`
  （MCP 握手 / 403·406 排错 / base64 推送 / 审批门 / 真机安装验收）
- 配套工具 → `kb/general/methodology/mcp_bridge_client.py`
  （一键 list/call/push；实测 171 工具、4 设备分组正确）
- 相关 → `kb/general/methodology/01-headless-emulation-windows-android-handbook.md`
  （Qiling/Unicorn 无环境仿真）、`kb/apk-reverse/techniques/02-native/r2pay_headless_emulator.py`
