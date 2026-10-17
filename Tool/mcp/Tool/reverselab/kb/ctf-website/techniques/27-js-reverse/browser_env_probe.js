/**
 * browser_env_probe.js — 现代前端风控环境模拟与全递归 Proxy 沙盒探针
 * 
 * 强化能力：
 * 1. Function.prototype.toString 原型链防伪覆盖；
 * 2. WebGL / Canvas / AudioContext 现代音频视频与渲染指纹模拟；
 * 3. Navigator 现代扩展（connection, hardwareConcurrency, permissions）；
 * 4. 深度递归 Proxy 自动捕获与缺失红黄告警（不抛崩溃异常）。
 */

// ── 1. Function.prototype.toString 防篡改保护 ──
(() => {
    const originalToString = Function.prototype.toString;
    const nativeSymbol = Symbol('native-code-tag');

    function setNative(fn, name) {
        const fnName = name !== undefined ? name : (fn.name || '');
        Object.defineProperty(fn, nativeSymbol, {
            value: `function ${fnName}() { [native code] }`,
            enumerable: false,
            writable: true,
            configurable: true
        });
        return fn;
    }

    Function.prototype.toString = function () {
        if (this && this[nativeSymbol]) {
            return this[nativeSymbol];
        }
        return originalToString.call(this);
    };

    setNative(Function.prototype.toString, 'toString');
    globalThis.setNative = setNative;
})();

// ── 2. 递归 Proxy 探针生成器 ──
function createProxy(target, name = 'window') {
    return new Proxy(target, {
        get(obj, prop, receiver) {
            if (typeof prop === 'symbol' || prop === 'inspect' || prop === '__proto__') {
                return Reflect.get(obj, prop, receiver);
            }

            const val = Reflect.get(obj, prop, receiver);
            const pathName = `${name}.${String(prop)}`;

            if (val !== undefined) {
                if (typeof val === 'function') {
                    setNative(val, String(prop));
                }
                return val;
            }

            console.warn(`\x1b[33m[PROXY MISSING]\x1b[0m 访问未定义环境: ${pathName}`);
            return undefined;
        },
        set(obj, prop, value, receiver) {
            console.log(`\x1b[36m[PROXY SET]\x1b[0m 写入环境属性: ${name}.${String(prop)}`);
            return Reflect.set(obj, prop, value, receiver);
        }
    });
}

// ── 3. 现代设备与多媒体指纹模拟器 ──
function mockWebGLContext() {
    return {
        getExtension: setNative(function (name) {
            if (name === 'WEBGL_debug_renderer_info') {
                return {
                    UNMASKED_VENDOR_WEBGL: 0x9245,
                    UNMASKED_RENDERER_WEBGL: 0x9246
                };
            }
            return null;
        }, 'getExtension'),
        getParameter: setNative(function (pname) {
            if (pname === 0x9245) return "Google Inc. (NVIDIA)";
            if (pname === 0x9246) return "ANGLE (NVIDIA, NVIDIA GeForce RTX 4070 Direct3D11 vs_5_0 ps_5_0, D3D11)";
            return 0;
        }, 'getParameter'),
        createBuffer: setNative(function() { return {}; }, 'createBuffer')
    };
}

const rawWindow = {
    name: "",
    innerWidth: 1920,
    innerHeight: 1080,
    outerWidth: 1920,
    outerHeight: 1080,
    devicePixelRatio: 1.25,
    addEventListener: setNative(function (type, listener) {}, 'addEventListener'),
    removeEventListener: setNative(function (type, listener) {}, 'removeEventListener'),
    setTimeout: setTimeout,
    clearTimeout: clearTimeout,
    setInterval: setInterval,
    clearInterval: clearInterval,
    // 现代音频指纹接口
    AudioContext: setNative(function() {
        return {
            createOscillator: setNative(function() { return { start: function(){}, stop: function(){} }; }),
            createAnalyser: setNative(function() { return { getFloatFrequencyData: function(){} }; }),
            destination: {}
        };
    }, 'AudioContext')
};

const rawNavigator = {
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    appVersion: "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    appName: "Netscape",
    platform: "Win32",
    language: "zh-CN",
    languages: ["zh-CN", "zh"],
    hardwareConcurrency: 16,
    deviceMemory: 16,
    maxTouchPoints: 0,
    webdriver: false, // 核心：坚决禁止为 true
    connection: {
        rtt: 50,
        downlink: 10,
        effectiveType: "4g"
    },
    plugins: []
};

const rawDocument = {
    title: "",
    referrer: "",
    cookie: "",
    readyState: "complete",
    documentElement: {},
    body: {},
    createElement: setNative(function (tag) {
        tag = String(tag).toLowerCase();
        if (tag === 'canvas') {
            return {
                getContext: setNative(function (type) {
                    if (type === 'webgl' || type === 'experimental-webgl') {
                        return mockWebGLContext();
                    }
                    return {
                        fillText: setNative(function () {}, 'fillText'),
                        getImageData: setNative(function () { return { data: new Uint8Array(16) }; }, 'getImageData')
                    };
                }, 'getContext'),
                toDataURL: setNative(function () { return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA"; }, 'toDataURL')
            };
        }
        return {};
    }, 'createElement'),
    getElementById: setNative(function (id) { return null; }, 'getElementById'),
    getElementsByTagName: setNative(function (name) { return []; }, 'getElementsByTagName')
};

rawWindow.window = rawWindow;
rawWindow.self = rawWindow;
rawWindow.top = rawWindow;
rawWindow.parent = rawWindow;
rawWindow.navigator = rawNavigator;
rawWindow.document = rawDocument;

const proxyWindow = createProxy(rawWindow, 'window');
const proxyNavigator = createProxy(rawNavigator, 'navigator');
const proxyDocument = createProxy(rawDocument, 'document');

global.window = proxyWindow;
global.self = proxyWindow;
global.top = proxyWindow;
global.parent = proxyWindow;
global.navigator = proxyNavigator;
global.document = proxyDocument;

module.exports = {
    window: proxyWindow,
    navigator: proxyNavigator,
    document: proxyDocument
};
