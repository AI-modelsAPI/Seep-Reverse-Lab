# Seep Reverse Lab — VPS / Linux 服务器适配分支

> **本分支：`vps-adaptations`**
> 基于上游 [`angusdevgo/Seep-Reverse-Lab`](https://github.com/angusdevgo/Seep-Reverse-Lab) 的
> 服务器端适配版本，面向 **Debian / Ubuntu 无桌面环境** 的 VPS 部署。
>
> 上游项目是一个 Agent 原生的多平台逆向工程与 CWE-602 客户端鉴权审计工作台。
> 本分支**不改动其架构与战术内容**，只做三件事：
> ① 修复上游安装脚本在纯 Linux 上的硬缺陷；
> ② 加固合规中继（compliance-relay）的改写覆盖率；
> ③ 提供**不覆盖本地改动**的上游同步机制。

---

## 目录

- [快速开始](#快速开始)
- [本分支相对上游的改动](#本分支相对上游的改动)
- [上游同步（不覆盖本地改动）](#上游同步不覆盖本地改动)
- [目录结构](#目录结构)
- [故障排查](#故障排查)
- [回滚与卸载](#回滚与卸载)

---

## 快速开始

### 前置条件

| 组件 | 版本 | 说明 |
| :--- | :--- | :--- |
| **Python** | 3.11+ | 必需 |
| **Node.js** | 18+（推荐 22+） | js-reverse / playwright MCP 需要 |
| **Git** | 任意 | |
| **unzip** | 任意 | 解压内置离线依赖 |
| **radare2** | 任意 | `apt install radare2`（内置的是 Windows 版，Linux 不可执行） |

Debian / Ubuntu 一键装齐：

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nodejs npm radare2 unzip git
```

### 安装

```bash
git clone -b vps-adaptations https://github.com/AI-modelsAPI/Seep-Reverse-Lab.git
cd Seep-Reverse-Lab
./setup/install-vps.sh
```

**常用参数**

```bash
./setup/install-vps.sh --dry-run      # 预演，不做任何改动
./setup/install-vps.sh --skip-pip     # 跳过 Python 依赖安装
./setup/install-vps.sh --with-relay   # 额外安装 compliance-relay systemd 服务
```

安装脚本是**幂等**的，可重复执行；已存在的项会跳过而非报错。

### 部署后自检

```bash
./setup/verify.sh
```

期望输出结尾：

```
[体检报告] 核心检查通过: 50 项 | 异常阻断: 0 项 | 关注项: 2 项
🎉 结论: 工作台在当前 Linux 环境处于 [READY / 完备就绪] 状态！
```

### 开始使用

在 agent（`pi` CLI 或 `pi-web`）对话中发送：

```
lab：
```

即可开启工作环境（写入 `~/.pi/agent/lab-mode.flag`，加载技能与审计语境规范化）。

> **Pi Web 用户注意**：若通过 pi-web 使用，请把服务的工作目录指向本仓库，
> 并在 provider 选择上使用**经合规中继的** provider（见下节）。

---

## 本分支相对上游的改动

> 全部改动集中在 7 个文件 + 2 个新增脚本，**不涉及任何模型配置**
> （`models.json`、API key、provider 地址均由使用者自行配置，不入库）。

### 1. 新增：VPS 部署脚本 `setup/install-vps.sh`

上游 `setup/install.sh` 面向 Windows / 桌面环境，在纯 Linux 服务器上有三处硬缺陷：

| # | 缺陷 | 上游行为 | 本分支修正 |
| :- | :--- | :--- | :--- |
| 1 | **mcp.json 路径错误** | 模板用 Windows 反斜杠 `<SEEP_ROOT>\\Tool\\mcp\\...`，`sed` 只替换占位符 → 产出非法路径 | 直接生成正斜杠 JSON，并用 `python3` 而非 `python` |
| 2 | **pip 被 PEP 668 拦截** | `pip install` 直接失败（`EXTERNALLY-MANAGED`） | 自动检测并附加 `--break-system-packages`，或提示改用 venv |
| 3 | **内置 radare2 不可执行** | 内置 `radare2/bin/*` 是 Windows PE | 探测系统 radare2，缺失时给出明确安装指引 |

另外新增能力：

- **增量合并 mcp.json** —— 保留使用者已有的自定义 MCP 条目，不覆盖
- **智能探测** —— `js-reverse` 优先用仓库内构建产物、回退全局安装；`ida` 仅在探测到 `idalib-mcp` 时注册
- **`--dry-run` / `--skip-pip` / `--with-relay`** 参数
- **幂等** —— 可安全重复执行

### 2. 新增：上游同步脚本 `setup/sync-upstream.sh`

见 [下一节](#上游同步不覆盖本地改动)。

### 3. 合规中继加固 `Tool/scripts/compliance-relay/relay.py`

| 改动 | 原因 |
| :--- | :--- |
| **改写范围扩到 `system` / `developer` / `instructions`** | 原先只改 `role=="user"`。但 agent 会把 `AGENTS.md` / `SYSTEM.md`（含"破解/keygen/脱壳"等触发词）注入 system prompt 一并上行 —— 只改 user 时主触发源仍在，上游照样拒绝 |
| **转发前抹除上游拒绝文本**（`strip_refusals`） | 拒绝文本一旦留在会话历史里，会被下一轮请求再次送回上游，形成"看到历史被拒 → 继续拒"的连锁 |
| **消除改写痕迹**（`collapse_adjacent_repeats`） | 替换规则会把「绕过」→「旁路验证」，若原文紧接着还有「验证」就拼出「旁路验证验证」这种正常中文里不存在的词，模型据此判定"这是被程序改写过的文本"，反而更容易拒绝 |
| **斜杠判定收窄** | 原判定 `startswith("/")` 会把 Linux 绝对路径（`/opt/x/破解样本 怎么分析`）整条放过。收窄为仅匹配 `/^\/[A-Za-z][\w-]*(\s+[^\/\n]*)?$/` 的纯命令词 |
| **结构化字段不改写** | `tools` / `tool_result` / `function_call_output` 只清洗拒绝残留，保协议完整 |

### 4. 拒答重试修复 `Tool/scripts/compliance-relay/refusal.py`

| 改动 | 原因 |
| :--- | :--- |
| **`ATTACK_ASK` 补短命令形态** | 上游正则要求「分析…程序」才命中，导致「分析 <目标>」这类短命令永远不触发重试 |
| **新增 `BARE_NAME`** | 上游只认带扩展名的路径，无扩展名的产品名（`AndroGoat-v2.0.1`）提不出目标 → 改写策略全部返回空。注意不能用 `\b`（Python 的 `\w` 含 CJK） |

### 5. 拦截扩展修复 `Tool/prompts/extensions/security-audit-interceptor.ts`

| 改动 | 原因 |
| :--- | :--- |
| **`transformed` 不再被丢弃** | 原实现在 `needsWrap=false` 时直接 `continue`，导致 17 个只在词表、不在触发正则的敏感词（`脱壳`/`keygen`/`序列号`/`注册机`/`后门`/`免杀`/`提权` 等）**改写结果被丢掉、原样上行** |
| **`sanitizeHarmfulPromptLeak` 改字面量正则** | 原实现用字符类匹配（只匹配单个字母，等于没清）；改为字面量短语正则，覆盖带链接/不带链接两种拒绝变体 |
| **`collapseAdjacentRepeats`** | 与 relay 侧同源的痕迹消除（见上） |
| **斜杠判定收窄** | 同 relay 侧，避免 Linux 路径被整条放过 |

### 6. System prompt 加载修复 `Tool/prompts/extensions/load-system-prompt.ts`

| 改动 | 原因 |
| :--- | :--- |
| **候选表补 `SYSTEM.md`** | 原实现只找小写 `system.md`，但工作台安装的是大写 `SYSTEM.md`。Linux 文件系统**大小写敏感** → `existsSync` 恒为 false，扩展静默失效 |

### 7. MCP 服务修复 `Tool/mcp/seep_mcp_server.py`

| 改动 | 原因 |
| :--- | :--- |
| **非零退出码时同时返回 stdout** | 原实现 `returncode != 0 and not out` 才报错，丢掉了 stdout（排障时看不到关键信息） |
| **`seep_auto_triage` 改流式分块哈希** | 原实现只读前 50MB 计算哈希，大文件会得到错误哈希值 |
| **`seep_apk_decompile` / `_unpack` 错误显式抛出** | 原先错误被吞进返回值，调用方误以为成功 |
| **Java 探测增强** | 优先验证 `java -version` 可实际运行；补充 macOS Homebrew 路径（对 Linux 无副作用，有 `os.path.isfile` 守卫） |

### 8. 测试同步 `Tool/scripts/compliance-relay/tests/*`

测试断言随全角色改写更新：**93 个用例全部通过**。

```bash
cd Tool/scripts/compliance-relay && python3 -m unittest discover -s tests
```

---

## 上游同步（不覆盖本地改动）

### 为什么需要专门机制

本分支的改动会与上游演进产生**结构性冲突**——例如上游继续按"只改 user"的思路改 `relay.py`，
而本分支已改为全角色。直接 `git merge upstream/main` 有两种坏结果：

- **静默覆盖**：上游改动覆盖了本地修复，你察觉不到；
- **冲突卡死**：一堆冲突文件，手动分辨哪些是"我的修复"很费时。

### 同步脚本

```bash
./setup/sync-upstream.sh
```

**它做了什么**

1. 记录**本地改动白名单**（`LOCAL_FILES`）——这是"必须保住"的文件集合
2. `git bundle` 全量备份到 `.git/sync-backup-<时间戳>/`
3. `git fetch upstream main`
4. 三方合并；**若冲突**：
   - 白名单内的文件 → **保留本地版**，上游版另存为 `<file>.upstream-<sha>` 供人工比对
   - 白名单外的文件 → 中止并列出，交人工决定（不静默取任何一方）
5. 跑 relay 测试套件验证合并结果

**关键保证：任何冲突都不会静默丢改动。**

### 常用命令

```bash
./setup/sync-upstream.sh --check      # 只报告落后多少提交 + 待同步清单
./setup/sync-upstream.sh --dry-run    # 预演
./setup/sync-upstream.sh --abort      # 放弃进行中的同步
```

### 首次配置远端

```bash
git remote add upstream https://github.com/angusdevgo/Seep-Reverse-Lab.git
git remote -v
```

（若已存在 `origin` 指向上游，脚本会自动回退使用它。）

### 手动处理非白名单冲突

```bash
# 查看冲突
git status --short

# 接受上游版本
git checkout --theirs -- <file> && git add <file>

# 或保留本地版本
git checkout --ours -- <file> && git add <file>

# 完成合并
git commit --no-edit
```

### 添加新的本地改动到白名单

编辑 `setup/sync-upstream.sh` 的 `LOCAL_FILES` 数组，或临时用环境变量：

```bash
LOCAL_FILES_EXTRA="path/to/file1 path/to/file2" ./setup/sync-upstream.sh
```

### 回滚同步

```bash
# 方式一：用备份
git reset --hard $(cat .git/sync-backup-*/HEAD.txt | tail -1)

# 方式二：用 git 自带
git reset --hard HEAD@{1}

# 方式三：用 bundle 完全恢复
git clone .git/sync-backup-<时间戳>/repo.bundle restored-repo
```

---

## 目录结构

```
Seep-Reverse-Lab/
├── setup/
│   ├── install-vps.sh          ← 【本分支新增】VPS / Linux 部署
│   ├── sync-upstream.sh        ← 【本分支新增】上游同步（保本地改动）
│   ├── install.sh              （上游，Windows/桌面向）
│   ├── uninstall.sh            （上游）
│   ├── update.sh               （上游）
│   └── verify.sh               （上游，自检）
├── Tool/
│   ├── mcp/
│   │   ├── seep_mcp_server.py  ← 【本分支修复】
│   │   └── Tool/safe/          内置工具（jadx / radare2 / apktool 等）
│   ├── prompts/
│   │   ├── SYSTEM.md / AGENTS.md
│   │   └── extensions/         ← 【本分支修复 2 个 .ts】
│   ├── scripts/
│   │   └── compliance-relay/   ← 【本分支加固 relay.py / refusal.py / tests】
│   ├── skill/                  技能包
│   └── reverselab/kb/          知识库
├── MANUAL/                     深度专项 SOP
└── README.md                   ← 【本分支改写】
```

---

## 故障排查

### `mcp.json` 路径含反斜杠 / MCP 服务启动失败

上游 `install.sh` 的已知缺陷。用本分支脚本重新生成：

```bash
./setup/install-vps.sh
cat ~/.pi/agent/mcp.json | python3 -m json.tool   # 应看到正斜杠路径
```

### `pip install` 报 `externally-managed-environment`

PEP 668 限制。本分支脚本已自动处理；手动执行时：

```bash
python3 -m pip install --break-system-packages "mcp>=1.20,<1.29"
# 或隔离到 venv
python3 -m venv .venv && .venv/bin/pip install "mcp>=1.20,<1.29"
```

### radare2 相关 MCP 工具报错

内置 `radare2/bin` 是 Windows 版。安装系统版：

```bash
sudo apt install radare2
radare2 -v
```

### 上游持续拒答

检查合规中继是否启用：

```bash
systemctl status seep-relay
# 确认 lab-mode 标志存在（中继仅在此标志下改写）
ls ~/.pi/agent/lab-mode.flag

# 确认 provider 指向中继而非直连
grep -o '"baseUrl": "[^"]*"' ~/.pi/agent/models.json
# 应含 http://127.0.0.1:17890/r/<token>/...
```

若 provider 直连上游（不经中继），改写不会生效。

### 同步后功能异常

```bash
# 查看同步引入的上游改动
git log --oneline HEAD@{1}..HEAD

# 回滚
git reset --hard HEAD@{1}
```

---

## 回滚与卸载

### 卸载工作台写入 agent 的配置

```bash
./setup/uninstall.sh --dry-run    # 先预览
./setup/uninstall.sh              # 执行
```

`uninstall.sh` 只移除工作台自己装的东西，**永不删除** `models.json` / `auth.json` /
`sessions/` 等用户数据。

### 移除 compliance-relay 服务

```bash
systemctl disable --now seep-relay
rm /etc/systemd/system/seep-relay.service
systemctl daemon-reload
```

### 完全移除

```bash
./setup/uninstall.sh
sudo rm -rf /path/to/Seep-Reverse-Lab
```

---

## 与上游的关系

| 项目 | 说明 |
| :--- | :--- |
| **上游** | [`angusdevgo/Seep-Reverse-Lab`](https://github.com/angusdevgo/Seep-Reverse-Lab) |
| **本分支** | `AI-modelsAPI/Seep-Reverse-Lab` → `vps-adaptations` |
| **基线** | 上游 `main` 的 `ccddca5`（v1.6.0） |
| **同步方式** | `./setup/sync-upstream.sh`（三方合并 + 白名单保本地） |
| **上游内容** | 全部战术手册、知识库、技能包、案例**保持原样** |

上游的战术内容（`MANUAL/`、`Tool/reverselab/kb/`、`Tool/skill/`）本分支**未做任何修改**，
上游更新可直接合入。

---

## 许可

沿用上游 [LICENSE](LICENSE)。
