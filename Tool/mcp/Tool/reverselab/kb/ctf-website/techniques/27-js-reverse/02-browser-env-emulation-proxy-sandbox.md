---
id: "ctf-website/27-js-reverse/02-browser-env-emulation-proxy-sandbox"
title: "Node.js 浏览器补环境标准 Proxy 探针与防风控对抗手册"
title_en: "Node.js Browser Environment Emulation, Proxy Probe, and Anti-Fingerprinting Sandbox"
summary: >
  针对现代前端风控签名（如 Web 逆向、滑动验证码、电商接口 token 计算）在 Node.js 本地运行报错的标准化补环境作战手册。
  内置通用深度 Proxy 探针（自动记录代码访问了哪些未定义的环境属性与方法）、Function.prototype.toString 原型链防伪、
  以及 navigator.webdriver、Canvas、WebGL、screen、localStorage 等关键指纹对象的标准伪造模板。
summary_en: >
  Field manual for emulating browser DOM/BOM environments inside Node.js for frontend signature and token extraction.
  Ships a recursive Proxy monitor to log undefined attribute access, Function.prototype.toString spoofing,
  and mock objects for navigator, screen, Canvas, WebGL, and storage to defeat modern anti-crawler fingerprinting.
board: "ctf-website"
category: "27-js-reverse"
signals:
  - "window is not defined"
  - "document is not defined"
  - "navigator is not defined"
  - "Cannot read properties of undefined"
  - "toString() 防篡改"
  - "Proxy 探针"
  - "补环境"
  - "Canvas 指纹"
  - "WebGL 指纹"
  - "navigator.webdriver"
mcp_tools:
  - "kb_router"
difficulty: "advanced"
tags:
  - "web"
  - "javascript"
  - "node"
  - "emulation"
  - "proxy"
  - "fingerprint"
evidence: "verified"
validated_by: "实测于各类风控签名算法本地独立执行环境"
language: "zh-CN"
last_updated: "2026-10-15"
related_articles:
  - "ctf-website/27-js-reverse/01-ast-deobfuscation-pipeline"
  - "ctf-website/01-recon/captcha-bypass"
---
# Node.js 浏览器补环境标准 Proxy 探针与防风控对抗手册

在做 Web JS 逆向（如提取请求头 `_signature`、`sign`、`token`）时，直接把混淆代码复制到 Node.js 运行，
99% 会立即报 `window is not defined` 或 `Cannot read properties of undefined`。
传统的土办法是“报错一个补一个”，但现代风控脚本会：
1. **暗中探测属性**：`if (window.chrome && window.chrome.runtime)`，拿不到直接返回假签名；
2. **检测 `toString()`**：检测伪造函数的 `Function.prototype.toString.call(func)` 是不是返回 `"function () { [native code] }"`；
3. **检测 `navigator.webdriver`**：识别自动化测试工具；
4. **检测原型链一致性**：`Object.getPrototypeOf(window) === Window.prototype`。

最强的高效破局法是：**使用递归 Proxy 沙盒探针监控一切访问，自动按日志补全**。

---

## 一、 补环境核心三定律

1. **原型链必须闭环**：`window.__proto__` 必须指向 `Window.prototype`，`Window.prototype.__proto__` 指向 `EventTarget.prototype`；
2. **函数 `toString()` 防伪**：任何自定义的模拟函数，其 `toString()` 必须输出官方的 `[native code]`；
3. **未定义行为静默放行**：通过 Proxy 拦截未定义的 `get`，打印红字警告，但返回新的 Proxy 对象或 `undefined`，防止代码直接抛出异常崩溃。

---

## 二、 核心武器：Function.prototype.toString 防伪注入

```javascript
(() => {
    const $toString = Function.prototype.toString;
    const symbol = Symbol('original-code');

    function setNative(fn) {
        Object.defineProperty(fn, symbol, {
            value: `function ${fn.name || ''}() { [native code] }`,
            enumerable: false,
            writable: true,
            configurable: true
        });
        return fn;
    }

    Function.prototype.toString = function () {
        if (this && this[symbol]) {
            return this[symbol];
        }
        return $toString.call(this);
    };

    setNative(Function.prototype.toString);
    globalThis.setNative = setNative;
})();
```

---

## 三、 深度 Proxy 探针：`browser_env_probe.js`

同目录下内置完整自包含沙盒。只需在要逆向的目标代码头部引入该探针：

```javascript
// 在混淆代码最前一行引入探针沙盒
require('./browser_env_probe.js');

// 你的目标加密/签名混淆代码粘贴在下方:
// ...
```

运行后，控制台会自动以彩色日志输出混淆代码暗中访问了哪些属性：
```text
[PROXY GET] window.navigator.userAgent -> "Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."
[PROXY GET] document.createElement("canvas") -> [HTMLCanvasElement]
[PROXY MISSING] window.chrome.loadTimes -> 未定义! (请在此补桩)
```
根据探针的提示，缺什么补什么，几分钟即可在本地无风控完成签名算法复现！
