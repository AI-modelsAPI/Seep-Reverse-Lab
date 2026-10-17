---
id: "apk-reverse/02-native/08-flutter-dart-aot-reconstruction"
title: "Dart / Flutter AOT 逆向还原与 Snapshot 特征提取指南"
title_en: "Dart / Flutter AOT Reverse Engineering and Snapshot Carving Guide"
summary: >
  针对采用 Flutter 开发的移动应用（无标准 DEX 业务逻辑，全在 libapp.so），建立基于 Dart AOT Snapshot
  的现代化逆向工作流。涵盖通过 libflutter.so 提取 Engine commit 与 Dart 版本号、从 libapp.so 的
  _kDartVmSnapshotData 解析 Snapshot Hash (32B) 与 VM Flags，以及自动化符号结构映射策略。
summary_en: >
  State-of-the-art reverse engineering playbook for Flutter Android apps (where core logic resides in stripped libapp.so).
  Covers Engine commit extraction from libflutter.so, Dart VM Snapshot Hash / VM Flags recovery from
  _kDartVmSnapshotData in libapp.so, and automated Object Pool / Function symbol mapping.
board: "apk-reverse"
category: "02-native"
signals:
  - "flutter app"
  - "libapp.so"
  - "libflutter.so"
  - "_kDartVmSnapshotData"
  - "_kDartIsolateSnapshotData"
  - "Dart AOT"
  - "snapshot_hash"
  - "blutter"
  - "Flutter Engine ID"
mcp_tools:
  - "kb_router"
difficulty: "advanced"
tags:
  - "apk"
  - "android"
  - "flutter"
  - "dart"
  - "aot"
  - "snapshot"
evidence: "verified"
validated_by: "实测于 GitHub 前沿项目 worawit/blutter 核心提取算法"
language: "zh-CN"
last_updated: "2026-10-15"
related_articles:
  - "apk-reverse/02-native/07-unidbg-native-emulation-pipeline"
  - "apk-reverse/02-native/01-il2cpp-offset-discovery"
---
# Dart / Flutter AOT 逆向还原与 Snapshot 特征提取指南

在现代 Android 逆向中，如果解包发现 `classes.dex` 极其单薄（只有 FlutterActivity 启动入口），
核心业务代码全部下沉在 `lib/arm64-v8a/libapp.so` 和 `libflutter.so` 中，且 `libapp.so` 剥离了所有符号。
直接将 `libapp.so` 拖入 IDA Pro，反编译出的几乎全是无名汇编函数（`sub_123456`），传统的 Java 反编译彻底失效。

**破局核心**：Dart 运行时会将全量类元数据、函数签名、常量字符串序列化在 AOT Snapshot 中。
只要拿到 **Engine ID** 和 **Snapshot Hash**，就能精准反序列化出所有的函数名与类拓扑！

---

## 一、 核心取证两步曲

### 1. 从 `libflutter.so` 提取 Engine Commit 与 Dart 版本
在 `libflutter.so` 的 `.rodata` 段中：
- 搜索 40 位十六进制字符串（Git Commit SHA-1），这是构建该 Flutter 引擎的官方 commit；
- 正则匹配 `\x00([\d\w\.-]+) \((stable|beta|dev)\)`，可直接提取 Dart SDK 版本号（如 `3.3.0`）。

### 2. 从 `libapp.so` 提取 Snapshot Hash 与 VM 标志
在 `libapp.so` 的导出表（`.dynsym`）中定位 `_kDartVmSnapshotData` 符号：
- 结构体偏移 `st_value + 20` 处固定存放 **32 字节的 Snapshot Hash**；
- 紧随其后为以 NULL 结尾的 **VM Flags 启动参数字符串**。

---

## 二、 自动化探针工装：`flutter_dart_probe_tool.py`

同目录下自带轻量级纯 Python 提取工具：

```bash
python3 flutter_dart_probe_tool.py --libapp libapp.so --libflutter libflutter.so
```
输出示例：
```text
[+] 架构: AArch64 (64-bit)
[+] 引擎 Engine ID: 235db3c109e973e34421572422146604b32ea29d
[+] Dart SDK 版本: 3.2.3 (stable)
[+] Snapshot Hash: 5bc983b6c7012b185ec160a28f804689
[+] VM Flags: --causal_async_stacks --lazy_async_stacks ...
[+] 官方 SDK 头文件匹配地址已生成，可直接使用 Blutter 恢复全量业务符号！
```
