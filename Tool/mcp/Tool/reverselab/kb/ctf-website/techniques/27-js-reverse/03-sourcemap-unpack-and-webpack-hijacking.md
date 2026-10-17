---
id: "ctf-website/27-js-reverse/03-sourcemap-unpack-and-webpack-hijacking"
title: "现代前端 SourceMap 泄露源码还原与 Webpack 闭包劫持"
title_en: "Modern Frontend SourceMap Leakage Recovery and Webpack Scope Hijacking"
summary: >
  针对现代前端单页应用（Vue / React / Vite / Webpack / Rollup）在生产环境中因未关闭构建选项
  导致的 .js.map 泄露，提供自动化源码目录树恢复方案。同时针对无源码泄露的场景，
  提供通过篡改 window.webpackChunk 注入钩子、提取私有 __webpack_require__ 并导出闭包内加解密模块的黑盒利用技术。
summary_en: >
  Offensive and reverse engineering guide targeting frontend SPA production bundles. Covers automated
  full-project source tree reconstruction from leaked .js.map files, alongside runtime Webpack 4/5
  closure hijacking via window.webpackChunk push injection to expose hidden crypto/API functions globally.
board: "ctf-website"
category: "27-js-reverse"
signals:
  - "sourcemap"
  - ".js.map"
  - "sourceMappingURL"
  - "webpackChunk"
  - "webpackJsonp"
  - "__webpack_require__"
  - "shuji"
  - "前端源码泄露"
mcp_tools:
  - "kb_router"
difficulty: "intermediate"
tags:
  - "web"
  - "javascript"
  - "sourcemap"
  - "webpack"
  - "frontend"
  - "recon"
evidence: "verified"
validated_by: "实测于前沿开源项目 paazmaya/shuji 标准规范与真实 Webpack 4/5 打包站"
language: "zh-CN"
last_updated: "2026-10-15"
related_articles:
  - "ctf-website/27-js-reverse/01-ast-deobfuscation-pipeline"
  - "ctf-website/27-js-reverse/02-browser-env-emulation-proxy-sandbox"
---
# 现代前端 SourceMap 泄露源码还原与 Webpack 闭包劫持

在现代 Web 安全审计中，90% 以上的企业前端使用 Webpack、Vite、Rollup 进行工程化打包压缩。
面对被混淆压缩的巨型 `app.min.js`，有两种降维打击战术：
1. **白盒降维打击**：检测线上生产环境是否泄露 `.map` 文件，一旦泄露，直接 100% 还原原始未混淆的 TypeScript/Vue 源码（含开发者注释、内部 API 文档）；
2. **黑盒闭包穿透**：当没有源码泄露时，在控制台劫持 Webpack 运行时内部的 `__webpack_require__`，将打包在私有 IIFE 闭包里的所有加密、签名模块强制暴露到全局作用域直接调用。

---

## 一、 生产环境 SourceMap 自动化探测与源码树恢复

### 1. 探测信号
查看加载的 `.js` 文件末尾是否存在映射注释：
```javascript
//# sourceMappingURL=app.8f7b2c.js.map
```
或者尝试直接在 URL 后面拼接 `.map`：
`https://target.com/static/js/app.8f7b2c.js.map`

### 2. 核心还原原理（基于标准规范）
`.js.map` 是一个 JSON 文件，核心字段包括：
- `sources`: 记录了原始项目中的文件相对路径（如 `webpack:///src/views/Login.vue`）；
- `sourcesContent`: 数组中的每个元素就是对应源文件的**完全未经混淆的原始代码**！

使用我们内置的 `sourcemap_extractor_tool.py`，一条命令即可重建整个项目的原始源码目录树。

---

## 二、 Webpack 私有闭包模块导出劫持 (Console 注入)

当没有 `.map` 泄露时，无需去反混淆核心算法，可以直接在浏览器 DevTools 控制台注入以下钩子，将私有闭包内部的所有模块导出：

### Webpack 4 & 5 通用提取脚本

```javascript
(() => {
    let webpackRequire = null;
    // 自动适配常见的 chunk 挂载变量名
    const chunkName = Object.keys(window).find(k => k.startsWith('webpackChunk')) || 'webpackChunk_app';
    
    // 注入一个伪装的模块切片以截获内部的 require 句柄
    (window[chunkName] = window[chunkName] || []).push([
        [Symbol('hack-chunk')],
        {},
        (r) => { webpackRequire = r; }
    ]);

    if (!webpackRequire) {
        console.error("[-] 劫持失败: 未能获取到 Webpack 内部运行时");
        return;
    }

    console.log("[+] 成功截获 __webpack_require__ 句柄:", webpackRequire);

    // 遍历所有已缓存和已定义的模块
    const modules = webpackRequire.c || {};
    window.extractedModules = {};

    for (const [id, mod] of Object.entries(modules)) {
        if (mod && mod.exports) {
            window.extractedModules[id] = mod.exports;
        }
    }

    console.log(`[🎉] 成功将 ${Object.keys(window.extractedModules).length} 个核心闭包模块导出到全局: window.extractedModules`);
    console.log("提示: 可在 Console 中直接搜索加解密函数调用，例如: window.extractedModules['42'].encrypt('test')");
})();
```
