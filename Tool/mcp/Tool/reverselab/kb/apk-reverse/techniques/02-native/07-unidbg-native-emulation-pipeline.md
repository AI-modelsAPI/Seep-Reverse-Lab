---
id: "apk-reverse/02-native/07-unidbg-native-emulation-pipeline"
title: "UniDbg 现代 Native 模拟执行与 JNI 自动化打桩手册"
title_en: "UniDbg Modern Native Emulation and JNI Mocking Pipeline"
summary: >
  针对移动端高难度 Native 加密（SO 混淆、OLLVM、JNI 动态注册与环境风控绑定），建立基于 UniDbg
  的跨架构（ARM32/ARM64）模拟执行流水线。包含 AndroidEmulator 初始化、虚拟文件系统与 libc 打桩、
  JNIEnv 动态调用拦截、以及 Hook 提取中间签名密钥的工程模板。
summary_en: >
  Industrial pipeline using UniDbg for ARM32/ARM64 Android native library emulation. Covers AndroidEmulator
  bootstrapping, virtual VFS/libc stubs, JNIEnv dynamic registration handling, and memory hook interception
  to bypass OLLVM obfuscation and extract native crypto signatures without real devices.
board: "apk-reverse"
category: "02-native"
signals:
  - "unidbg"
  - "libapp.so"
  - "JNIEnv"
  - "AndroidEmulator"
  - "OLLVM SO"
  - "Native 签名算法"
  - "JNI_OnLoad 崩溃"
  - "dlopen"
mcp_tools:
  - "kb_router"
difficulty: "advanced"
tags:
  - "apk"
  - "android"
  - "native"
  - "unidbg"
  - "emulation"
  - "arm64"
evidence: "verified"
validated_by: "实测于标准 Android ARM64 原生 SO 签名函数黑盒调用"
language: "zh-CN"
last_updated: "2026-10-15"
related_articles:
  - "apk-reverse/02-native/06-jni-register-natives-tracing"
  - "apk-reverse/02-native/01-il2cpp-offset-discovery"
---
# UniDbg 现代 Native 模拟执行与 JNI 自动化打桩手册

在移动安全审计与接口风控分析中，越来越多的核心签名算法（如 `sign`、`token`、`getDeviceToken`）
被转移到底层 C/C++ 编写的 `.so` 动态库中，并施加了 **OLLVM 控制流平坦化、虚假控制流、字符串加密与反调试检测**。
静态反编译出数万行混乱的汇编；而在真机上 Hook 又常受限于 root 检测、环境对抗或没有现成真机/模拟器。

**最优工程解法是 UniDbg**：在 CPU 指令级（Unicorn 引擎）纯软件模拟 ARM 指令执行，对 JNI 调用进行打桩，黑盒跑出签名！

---

## 一、 UniDbg 标准工程模板 (Java / Maven 骨架)

```java
package com.reverselab.unidbg;

import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.Module;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.*;
import com.github.unidbg.memory.Memory;

import java.io.File;

public class NativeSignEmulator extends AbstractJni {
    private final AndroidEmulator emulator;
    private final VM vm;
    private final Module module;
    private final DvmClass dvmClass;

    public NativeSignEmulator(File apkFile, File soFile, String targetClassName) {
        // 1. 初始化 64位 ARM 仿真器
        emulator = AndroidEmulatorBuilder.for64Bit()
                .setProcessName("com.target.app")
                .build();

        // 2. 绑定 Android 运行时解析器 (支持虚拟 /system/lib64 基础库)
        Memory memory = emulator.getMemory();
        memory.setLibraryResolver(new AndroidResolver(23));

        // 3. 构造虚拟 Dalvik 虚拟机
        vm = emulator.createDalvikVM(apkFile);
        vm.setVerbose(false); // 生产排错时可置为 true
        vm.setJni(this);

        // 4. 加载目标 SO 并自动执行 JNI_OnLoad
        DalvikModule dm = vm.loadLibrary(soFile, true);
        module = dm.getModule();
        dm.callJNI_OnLoad(emulator);

        // 5. 解析对应的 Java Class 包装器
        dvmClass = vm.resolveClass(targetClassName.replace(".", "/"));
    }

    // 核心调用接口
    public String calculateSign(String urlPath, byte[] postData) {
        // 调用 native 方法: public static native String getSign(String path, byte[] body);
        DvmObject<?> result = dvmClass.callStaticJniMethodObject(
                emulator,
                "getSign(Ljava/lang/String;[B)Ljava/lang/String;",
                new StringObject(vm, urlPath),
                new ByteArray(vm, postData)
        );
        return (String) result.getValue();
    }

    // ── JNI 模拟打桩：拦截 SO 对 Java 层方法的反向调用 ──
    @Override
    public DvmObject<?> callStaticObjectMethodV(BaseVM vm, DvmClass dvmClass, String signature, VaList vaList) {
        // 示例：拦截 SO 反射获取设备 Android ID
        if ("android/provider/Settings$Secure->getString(Landroid/content/ContentResolver;Ljava/lang/String;)Ljava/lang/String;".equals(signature)) {
            return new StringObject(vm, "3589410982341234");
        }
        return super.callStaticObjectMethodV(vm, dvmClass, signature, vaList);
    }

    public void destroy() {
        try { emulator.close(); } catch (Exception ignored) {}
    }
}
```

---

## 二、 现代 Native 避坑军规

1. **`JNI_OnLoad` 崩溃排查**：
   - 90% 的崩溃是因为 SO 初始化时通过 JNI 获取了 `Context`、`PackageManager` 或调用了签名校验。
   - 在 `AbstractJni` 子类中覆盖 `callObjectMethodV`，匹配 `getApplicationContext` 与 `getPackageInfo` 返回假签名证书哈希即可顺利放行。
2. **处理 JNI 动态注册（`RegisterNatives`）**：
   - 如果目标函数在导出表里找不到名字，可以在 UniDbg 启动时配置 `vm.setVerbose(true)`，日志会直接打印动态绑定的函数偏移地址：
     ```text
     [RegisterNatives] java/lang/Security->encode([B)[B => RX@0x4001a4e0[libtarget.so]0x1a4e0
     ```
3. **内存 Dump 中间态**：
   - 在模拟执行过程中，直接通过 `emulator.getMemory().pointer(address).getByteArray(0, length)` 读取寄存器或内存指针，提取明文哈希，无需手工逆向极其复杂的加密轮次。
