# 逆向信号 → 文档映射总表（自动生成）

> 生成: 2026-10-17 09:42  |  由 `kb_maintain.py --signals` 产生
> 唯一信号: 2156  |  覆盖文档: 213

## 用法

```
seep_kb_search(query="<信号关键词>")   # 检索
seep_kb_read("<文档路径>")             # 读全文
# 或直接查本表 → 拿到文档路径
```

## 信号索引

| 信号 | 分类 | 文档 |
|---|---|---|
| `$where javascript 注入` | ctf-website | ctf-website/techniques/24-database/03-nosql-injection.md |
| `%0d%0a` | ctf-website/hpp-crlf | ctf-website/techniques/03-injection/hpp-crlf.md |
| `../` | ctf-website/file-attacks | ctf-website/techniques/06-file-attacks/file-upload-xxe-lfi.md |
| `.env` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `.env key` | ctf-website/signature-key | ctf-website/techniques/13-signature/03-key-attacks.md |
| `.env 文件可读` | ctf-website | ctf-website/techniques/24-database/04-config-exposure.md |
| `.git/head git-dumper` | ctf-website | ctf-website/techniques/24-database/05-backup-log-leak.md |
| `.git/head 目录泄露` | ctf-website | ctf-website/techniques/24-database/04-config-exposure.md |
| `.js.map` | ctf-website | ctf-website/techniques/27-js-reverse/03-sourcemap-unpack-and-webpack-hijacking.md |
| `.proto skeleton` | general | general/techniques/protocol/02-protobuf-flatbuffers-reverse.md |
| `.so` | apk-reverse/native | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md<br>apk-reverse/techniques/02-native/02-pointer-chain-patterns.md<br>apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `.sql .dump 备份文件` | ctf-website | ctf-website/techniques/24-database/05-backup-log-leak.md |
| `.vmp` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md |
| `/proc/pid/mem` | apk-reverse/dynamic-frida | apk-reverse/techniques/06-dynamic/01-memory-rw-hook.md<br>apk-reverse/techniques/06-dynamic/02-overlay-rendering-hook.md<br>apk-reverse/techniques/06-dynamic/03-touch-input-hook.md |
| `0e` | ctf-website/payment-php, ctf-website/signature-implementation | ctf-website/techniques/12-payment/payment-php.md<br>ctf-website/techniques/13-signature/02-implementation.md |
| `15 5a` | pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `169.254` | ctf-website/ssrf | ctf-website/techniques/04-ssrf/ssrf.md |
| `169.254.169.254` | ctf-website/cloud-serverless | ctf-website/techniques/10-cloud/aws-iam-privesc.md<br>ctf-website/techniques/10-cloud/serverless-lambda.md |
| `24h` | ctf-website/24h-loop-orchestration | ctf-website/techniques/00-workflow/24h-loop-orchestration.md<br>ctf-website/techniques/attack-network.md |
| `24h loop` | ctf-website | ctf-website/techniques/00-workflow/24h-loop-orchestration.md |
| `24小时` | ctf-website/24h-loop-orchestration | ctf-website/techniques/00-workflow/24h-loop-orchestration.md<br>ctf-website/techniques/attack-network.md |
| `2captcha` | ctf-website/captcha-bypass | ctf-website/techniques/01-recon/captcha-bypass.md |
| `301` | ctf-website/open-redirect | ctf-website/techniques/04-ssrf/open-redirect.md |
| `302` | ctf-website/open-redirect | ctf-website/techniques/04-ssrf/open-redirect.md |
| `360免杀` | pe-reverse/av-evasion | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `389` | ctf-website/ldap | ctf-website/techniques/02-auth/ldap-injection.md |
| `5-bit` | pe-reverse | pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `511 字节` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/09-runtime-vm-detection-generic.md |
| `636` | ctf-website/ldap | ctf-website/techniques/02-auth/ldap-injection.md |
| `== vs ===` | ctf-website/signature-implementation | ctf-website/techniques/13-signature/02-implementation.md |
| `["alg:none", "none算法", "无签名", "签名绕过", "jwt", "jwt_tool"]` | ctf-website | ctf-website/techniques/02-auth/jwt/01-alg-none.md |
| `["algorithm downgrade", "算法降级", "alg none", "sign_type", "rs256 hs256", "jwt confusion", "md5签名", "签名编码"]` | ctf-website | ctf-website/techniques/13-signature/01-algorithm.md |
| `["androidmanifest", "entry point", "application", "attachbasecontext", "jni_onload", "exported components", "native loading", "loadlibrary"]` | apk-reverse | apk-reverse/techniques/03-manifest/01-entry-point-tracing.md |
| `["api discovery", "swagger", "openapi", "graphql", "source map", "端点发现", "信息泄露", "apk"]` | ctf-website | ctf-website/techniques/17-api-attacks/01-api-discovery-leak.md |
| `["api key leak", "github dorking", "firebase", "stripe", "aws", "密钥泄露", "云服务滥用", "硬编码凭据"]` | ctf-website | ctf-website/techniques/17-api-attacks/02-api-key-leak.md |
| `["aws", "iam", "sts", "assumerole", "passrole", "policy simulation", "irsa", "metadata", "云凭证", "权限提升"]` | ctf-website | ctf-website/techniques/10-cloud/aws-iam-privesc.md |
| `["bac", "broken access control", "访问控制缺失", "垂直越权", "隐藏端点", "方法覆写", "actuator", "步骤跳过", "cwe-862"]` | ctf-website | ctf-website/techniques/14-idor/02-bac-business-logic.md |
| `["blink uaf", "chrome sandbox escape", "cssfontfeaturevaluesmap", "hashmap rehash", "浏览器沙箱逃逸", "cve-2026-2441", "chromium"]` | ctf-website | ctf-website/techniques/09-cve/01-browser-sandbox-escape.md |
| `["canonicalization", "规范化绕过", "参数排序", "json规范化", "url编码", "hpp", "xml c14n", "签名差异"]` | ctf-website | ctf-website/techniques/13-signature/04-canonicalization.md |
| `["captcha", "验证码", "recaptcha", "滑块验证", "ocr", "ddddocr", "playwright", "打码平台"]` | ctf-website | ctf-website/techniques/01-recon/captcha-bypass.md |
| `["ci/cd", "jenkins", "github actions", "gitlab ci", "self-hosted runner", "pipeline injection", "groovy rce", "oidc", "artifact poisoning"]` | ctf-website | ctf-website/techniques/10-cloud/ci-cd-pipeline.md |
| `["claim", "exp", "aud", "iss", "token混用", "id token", "access token", "权限绕过"]` | ctf-website | ctf-website/techniques/02-auth/jwt/06-claim-missing.md |
| `["cloudflare", "cf-ray", "cdn", "源站ip", "origin ip", "dns history", "securitytrails", "censys"]` | ctf-website | ctf-website/techniques/01-recon/cloudflare-bypass.md |
| `["container", "docker", "containerd", "runc", "privileged", "hostpath", "docker.sock", "capabilities", "seccomp", "apparmor"]` | ctf-website | ctf-website/techniques/10-cloud/container-runtime-escape.md |
| `["cordova", "react native", "flutter", "electron", "ionic", "capacitor", "nodeintegration", "metro bundler", "nativemodules", "跨平台框架"]` | ctf-website | ctf-website/techniques/21-mobile-bridge/02-cordova-reactnative.md |
| `["cors", "csrf", "samesite", "跨域请求", "跨站请求伪造", "acao", "acac", "csrf token bypass", "preflight"]` | ctf-website | ctf-website/techniques/07-client/cors-csrf.md |
| `["cpanel", "caldav", "path traversal", "pre-auth", "路径穿越", "url编码绕过", "cve-2026-29205", "root file read"]` | ctf-website | ctf-website/techniques/09-cve/03-cpanel-caldav-traversal.md |
| `["credential spraying", "凭证喷洒", "mfa fatigue", "push bombing", "credential stuffing", "pass-the-hash", "kerberoasting", "用户枚举"]` | ctf-website | ctf-website/techniques/16-rate-limit/02-brute-force-tactics.md |
| `["csp bypass", "jsonp", "cdn gadget", "dom clobbering", "strict-dynamic", "nonce", "css injection", "csp绕过"]` | ctf-website | ctf-website/techniques/18-cors-csp-advanced/01-csp-bypass.md |
| `["cve chain", "multi-cve", "primitive mapping", "漏洞组合链", "info_leak to rce", "cve chaining", "exploit chain"]` | ctf-website | ctf-website/techniques/09-cve/multi-cve-chain-playbook.md |
| `["cve correlation", "cwe mapping", "epss", "kev", "vulnerability graph", "漏洞关联", "cve graph"]` | ctf-website | ctf-website/techniques/09-cve/cve-correlation-graph.md |
| `["cve workflow", "fingerprint", "applicability", "exploit adaptation", "漏洞验证流程", "nvd api", "cisa kev"]` | ctf-website | ctf-website/techniques/09-cve/cve-workflow.md |
| `["cve", "jsonwebtoken", "pyjwt", "python-jose", "jjwt", "node-jsonwebtoken", "库漏洞", "依赖库", "版本指纹"]` | ctf-website | ctf-website/techniques/02-auth/jwt/08-cve-library.md |
| `["dependency confusion", "内部包名枚举", "npm publish", "ci build", "preinstall script", "typosquatting", "pypi registry", "manifest tarball", "lockfile", "private registry"]` | ctf-website | ctf-website/techniques/11-supply-chain/dependency-confusion.md |
| `["deserialization", "反序列化", "pickle", "php unserialize", "java gadget chain", "ysoserial", "hessian", "viewstate", "yaml"]` | ctf-website | ctf-website/techniques/05-deserialization/deserialization.md |
| `["email spoofing", "spf", "dkim", "dmarc", "邮件伪造", "显示名伪造", "smtp injection", "邮件认证"]` | ctf-website | ctf-website/techniques/19-dns-email/02-email-spoofing.md |
| `["file upload", "xxe", "lfi", "path traversal", "文件上传", "路径穿越", "php wrapper", "盲xxe"]` | ctf-website | ctf-website/techniques/06-file-attacks/file-upload-xxe-lfi.md |
| `["fingerprint", "版本识别", "server header", "favicon hash", "js framework", "wappalyzer", "cve lookup", "technology stack"]` | ctf-website | ctf-website/techniques/01-recon/version-fingerprinting.md |
| `["fofa", "资产测绘", "网络空间测绘", "org", "app", "弱口令", "漏洞狩猎", "shodan"]` | ctf-website | ctf-website/techniques/01-recon/fofa-hunting.md |
| `["github actions", "pull_request_target", "github_token", "self-hosted runner", "workflow injection", "oidc", "cache poisoning", "artifact leak"]` | ctf-website | ctf-website/techniques/10-cloud/github-actions-abuse-paths.md |
| `["graphql", "introspection", "schema", "batch query", "alias", "fragment", "subscription", "field suggestion"]` | ctf-website | ctf-website/techniques/03-injection/graphql.md |
| `["grpc", "protobuf", "field injection", "wire type", "varint", "reflection", "grpc-web", "protoscope", "grpc-status"]` | ctf-website | ctf-website/techniques/03-injection/grpc-protobuf.md |
| `["header fuzzing", "路径绕过", "http method", "代理差异", "指纹识别", "参数发现", "dirsearch", "api schema"]` | ctf-website | ctf-website/techniques/01-recon/recon-routing.md |
| `["hmac", "弱密钥", "爆破", "hashcat", "hs256", "jwt cracker", "wordlist", "secret"]` | ctf-website | ctf-website/techniques/02-auth/jwt/03-weak-key-bruteforce.md |
| `["host header", "密码重置劫持", "host注入", "ssrf", "cache poisoning", "x-forwarded-host", "vhost"]` | ctf-website | ctf-website/techniques/02-auth/host-header.md |
| `["hpp", "参数污染", "crlf", "换行注入", "响应拆分", "waf bypass", "header注入", "email注入", "duplicate parameter"]` | ctf-website | ctf-website/techniques/03-injection/hpp-crlf.md |
| `["http/2", "h2", "hpack", "stream multiplexing", "memory exhaustion", "dos", "cve-2025-53020", "协议攻击"]` | ctf-website | ctf-website/techniques/08-infra/http2-attacks.md |
| `["iap", "内购", "receipt验证", "purchasetoken", "卡密", "虚拟货币", "license key", "数字商品", "铸币攻击"]` | ctf-website | ctf-website/techniques/12-payment/payment-digital-goods.md |
| `["idor", "越权", "枚举", "uuid预测", "graphql别名", "批量端点", "跨租户", "cwe-639", "多步链"]` | ctf-website | ctf-website/techniques/14-idor/01-idor-enumeration.md |
| `["il2cpp", "global-metadata.dat", "pointer chain", "libil2cpp.so", "module base", "offset discovery", "frida verification", "ghidra 静态分析"]` | apk-reverse | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md |
| `["implementation bugs", "实现缺陷", "strcmp绕过", "== vs ===", "timing attack", "异常绕过", "类型强制", "extract覆盖", "支付回调", "magic hash", "空签名"]` | ctf-website | ctf-website/techniques/13-signature/02-implementation.md |
| `["jku", "x5u", "jwk set url", "x.509", "密钥劫持", "rsa", "jwks", "jwt_tool"]` | ctf-website | ctf-website/techniques/02-auth/jwt/05-jku-x5u-abuse.md |
| `["js逆向", "ast去混淆", "webassembly", "runtime hook", "浏览器逆向", "babel", "cryptojs", "webpack"]` | ctf-website | ctf-website/techniques/07-client/js-runtime.md |
| `["jwt", "签名绕过", "算法混淆", "kid注入", "jku", "x5u", "弱密钥", "token窃取"]` | ctf-website | ctf-website/techniques/02-auth/jwt/00-overview.md |
| `["jwt_tool", "hashcat", "工具链", "攻击流程", "结果矩阵", "jwt", "jwt-cracker", "burp"]` | ctf-website | ctf-website/techniques/02-auth/jwt/09-toolchain-operations.md |
| `["kernel driver", "/proc node", "insmod", "ioctl", "proc_read", "proc_write", "dmesg clear", "multi-kernel adaptation"]` | apk-reverse | apk-reverse/techniques/02-native/04-kernel-procfs-driver.md |
| `["key attack", "密钥攻击", "弱密钥", "硬编码密钥", "hmac爆破", "source map", ".env泄露", "prng预测", "密钥重用"]` | ctf-website | ctf-website/techniques/13-signature/03-key-attacks.md |
| `["kid", "key id", "路径穿越", "sql注入", "命令注入", "kid injection", "jwt_tool", "jwt"]` | ctf-website | ctf-website/techniques/02-auth/jwt/04-kid-injection.md |
| `["kubernetes", "container escape", "sa token", "rbac", "privileged pod", "runc", "kubelet", "etcd", "容器逃逸", "hostpath", "pods/exec"]` | ctf-website | ctf-website/techniques/10-cloud/kubernetes-container.md |
| `["kubernetes", "rbac", "selfsubjectaccessreview", "rolebinding", "clusterrolebinding", "pods/exec", "secrets/get", "serviceaccounts/token"]` | ctf-website | ctf-website/techniques/10-cloud/k8s-rbac-attack-paths.md |
| `["ldap", "过滤器注入", "ldap injection", "jndi", "盲注", "anonymous bind", "openldap"]` | ctf-website | ctf-website/techniques/02-auth/ldap-injection.md |
| `["length extension", "长度扩展", "merkle-damgard", "hashpumpy", "h(secret||message)", "md5扩展", "sha256扩展", "hle", "支付回调", "裸hash签名"]` | ctf-website | ctf-website/techniques/13-signature/05-length-extension.md |
| `["license verification", "api signature", "rc4 encryption", "telegram channel", "httppost", "curl_easy_perform", "access hook", "bypass"]` | apk-reverse | apk-reverse/techniques/05-network/02-license-verification-bypass.md |
| `["litellm", "privilege escalation", "api key bypass", "权限提升", "internal_user to proxy_admin", "cve-2026-47101", "allowed_routes"]` | ctf-website | ctf-website/techniques/09-cve/05-litellm-privesc.md |
| `["lost update", "余额扣减", "竞态条件", "read-modify-write", "toctou", "quota", "并发一致性", "差分实验"]` | ctf-website | ctf-website/techniques/12-payment/payment-race-lost-update.md |
| `["mass assignment", "批量赋值", "属性注入", "$fillable", "strong_parameters", "extract", "parse_str", "serializer", "cwe-915"]` | ctf-website | ctf-website/techniques/15-mass-assignment/01-mass-assignment.md |
| `["native so injection", "apk repack", "loadlibrary", "jni_onload", "constructor", "apktool", "uber-apk-signer", "integrity bypass"]` | apk-reverse | apk-reverse/techniques/08-patch-repack/01-so-injection-repack.md |
| `["nezha monitoring", "path traversal", "jwt forgery", "hs256", "路径遍历", "jwt伪造", "cve-2026-53519", "hasprefix bypass"]` | ctf-website | ctf-website/techniques/09-cve/04-nezha-path-traversal-jwt.md |
| `["nginx", "rewrite", "heap overflow", "set directive", "堆溢出", "缓冲区长度错配", "cve-2026-42945", "uri escape"]` | ctf-website | ctf-website/techniques/09-cve/06-nginx-rewrite-heapoverflow.md |
| `["oauth", "oidc", "redirect_uri", "state", "pkce", "code reuse", "id token", "client_secret", "sso"]` | ctf-website | ctf-website/techniques/02-auth/oauth-sso.md |
| `["oauth", "pkce", "csrf", "redirect_uri", "scope escalation", "token theft", "授权码拦截", "sso"]` | ctf-website | ctf-website/techniques/20-oauth-deep/01-oauth-attack-chains.md |
| `["okhttp", "retrofit", "socket", "sendto", "recvfrom", "protobuf", "traffic redirection", "packet capture"]` | apk-reverse | apk-reverse/techniques/05-network/01-game-protocol-hook.md |
| `["open redirect", "开放重定向", "redirect chain", "oauth redirect", "url redirection bypass", "parser differential", "302"]` | ctf-website | ctf-website/techniques/04-ssrf/open-redirect.md |
| `["overlay", "anativewindow", "imgui", "opengl es", "vulkan", "eglswapbuffers", "vkqueuepresentkhr", "surfaceflinger"]` | apk-reverse | apk-reverse/techniques/06-dynamic/02-overlay-rendering-hook.md |
| `["oxorany", "ollvm", "upx", "control flow flattening", "string encryption", "xor", "die", "packer detection", ".init_array"]` | apk-reverse | apk-reverse/techniques/07-packer/01-obfuscation-detection.md |
| `["pagemap", "pfn", "page table", "virt_to_phys", "kpti", "kaslr", "hugepage", "/dev/mem"]` | apk-reverse | apk-reverse/techniques/02-native/05-virt-phys-memory.md |
| `["parameter tampering", "参数篡改", "价格操纵", "零元购", "优惠券竞态", "toctou", "currency bypass", "cwe-20"]` | ctf-website | ctf-website/techniques/15-mass-assignment/02-parameter-tampering.md |
| `["payment bypass", "支付绕过", "零元购", "type confusion", "参数篡改", "amount manipulation", "state machine", "mass assignment"]` | ctf-website | ctf-website/techniques/12-payment/payment-bypass.md |
| `["payment callback", "支付回调", "签名绕过", "notify_url", "webhook", "ssrf", "幂等绕过", "mq注入", "异步竞态"]` | ctf-website | ctf-website/techniques/12-payment/payment-callback-async.md |
| `["payment logic", "支付逻辑", "路由发现", "金额篡改", "状态机", "回调签名", "幂等", "并发", "订单idor", "支付sqli", "订单账本"]` | ctf-website | ctf-website/techniques/12-payment/payment-logic.md |
| `["php", "type juggling", "magic hash", "strcmp绕过", "反序列化", "laravel", "woocommerce", "支付"]` | ctf-website | ctf-website/techniques/12-payment/payment-php.md |
| `["platform fingerprint", "平台指纹", "发卡系统", "acg-faka", "dujiaoka", "xycms", "cms识别", "ready.js"]` | ctf-website | ctf-website/techniques/12-payment/platform-fingerprints.md |
| `["pointer chain", "process_vm_readv", "ioctl driver", "getzz macro", "array traversal", "memory read", "offset patterns"]` | apk-reverse | apk-reverse/techniques/02-native/02-pointer-chain-patterns.md |
| `["postmessage", "跨域通信", "null origin", "oauth token", "prototype pollution", "event.source", "structured clone", "iframe"]` | ctf-website | ctf-website/techniques/07-client/postmessage.md |
| `["process_vm_readv", "process_vm_writev", "/proc/pid/mem", "ioctl driver", "strace", "memory detection", "frida interceptor"]` | apk-reverse | apk-reverse/techniques/06-dynamic/01-memory-rw-hook.md |
| `["prototype pollution", "原型链污染", "__proto__", "constructor.prototype", "ejs", "pug", "child_process", "node.js", "qs"]` | ctf-website | ctf-website/techniques/03-injection/prototype-pollution.md |
| `["race condition", "cache poisoning", "request smuggling", "条件竞争", "缓存投毒", "cl.te", "te.cl", "h2.cl"]` | ctf-website | ctf-website/techniques/08-infra/race-cache-smuggling.md |
| `["rate limit bypass", "速率限制绕过", "x-forwarded-for", "ip轮换", "ipv6旋转", "并发绕过", "验证码绕过", "cdn bypass"]` | ctf-website | ctf-website/techniques/16-rate-limit/01-rate-limit-bypass.md |
| `["rc4", "ksa", "prga", "s-box", "256-byte loop", "xor swap", "stream cipher", "md5 signature"]` | apk-reverse | apk-reverse/techniques/04-crypto/02-rc4-custom-crypto.md |
| `["redis rce", "valkey", "restore", "zipmap", "heap overflow", "overlong encoding", "cve-2026-25243"]` | ctf-website | ctf-website/techniques/09-cve/02-redis-zipmap-rce.md |
| `["redos", "正则回溯", "catastrophic backtracking", "时序攻击", "timing attack", "waf超时", "event loop", "side channel"]` | ctf-website | ctf-website/techniques/03-injection/redos-timing.md |
| `["replay attack", "重放攻击", "nonce绕过", "nonce预测", "timestamp操纵", "重放窗口", "nonce耗尽", "跨用户重放", "支付回调重放", "幂等绕过"]` | ctf-website | ctf-website/techniques/13-signature/06-replay-nonce.md |
| `["saml", "xml signature wrapping", "xsw", "canonicalization", "sso", "assertion", "nameid", "xml"]` | ctf-website | ctf-website/techniques/02-auth/saml-attacks.md |
| `["self-extracting", "shell embedding", "gzip", "lineno", "sed boundary", "c header", "finit_module", "payload extraction"]` | apk-reverse | apk-reverse/techniques/07-packer/02-self-extracting-payload.md |
| `["serverless", "lambda", "iam credential", "runtime api", "event injection", "无服务器", "aws", "冷启动", "function url", "lambda layer"]` | ctf-website | ctf-website/techniques/10-cloud/serverless-lambda.md |
| `["session fixation", "sso hijacking", "jwt bypass", "redis session", "remember-me", "会话固定", "samesite", "session puzzling"]` | ctf-website | ctf-website/techniques/20-oauth-deep/02-session-fixation-attacks.md |
| `["signature forgery", "签名伪造", "算法降级", "alg none", "magic hash", "签名绕过", "sign_type", "hmac", "jwt"]` | ctf-website | ctf-website/techniques/13-signature/00-overview.md |
| `["smali injection", "dex 修改", "apk repack", "loadlibrary hook", "application.attachbasecontext", "register conflict", "apksigner 签名"]` | apk-reverse | apk-reverse/techniques/01-dex-java/01-smali-injection.md |
| `["sqli", "nosqli", "waf bypass", "盲注", "mongodb", "$regex", "oob", "宽字节", "支付sqli", "订单表", "账本错位"]` | ctf-website | ctf-website/techniques/03-injection/sqli-nosqli.md |
| `["ssl pinning", "aes-cbc", "cipher.init", "secretkeyspec", "xor obfuscation", "ivparameterspec", "key extraction", "crypto bypass"]` | apk-reverse | apk-reverse/techniques/04-crypto/01-game-encryption-patterns.md |
| `["ssrf", "server-side request forgery", "gopher协议", "dns rebinding", "内网穿透", "cloud metadata", "imdsv2 bypass"]` | ctf-website | ctf-website/techniques/04-ssrf/ssrf.md |
| `["ssti", "模板注入", "jinja2", "thymeleaf", "freemarker", "rce", "沙盒逃逸", "__class__"]` | ctf-website | ctf-website/techniques/03-injection/ssti.md |
| `["subdomain takeover", "cname", "dangling dns", "cloud service", "s3 bucket", "cloudfront", "子域名接管", "dns"]` | ctf-website | ctf-website/techniques/19-dns-email/01-subdomain-takeover.md |
| `["subscription", "订阅攻击", "试用绕过", "trial abuse", "proration", "自动续费", "metered billing", "seat管理", "stripe webhook"]` | ctf-website | ctf-website/techniques/12-payment/payment-subscription.md |
| `["terraform", "tfstate", "iac", "backend", "state file", "terraform plan", "cloud secret", "s3 backend", "ci artifact"]` | ctf-website | ctf-website/techniques/10-cloud/terraform-state-secrets.md |
| `["ticket rush", "抢票", "状态机", "token逆向", "ctoken", "prepare create", "风控参数", "jshook"]` | ctf-website | ctf-website/techniques/12-payment/ticket-rush-api-reversing.md |
| `["token窃取", "xss", "重放", "bearer token", "httponly", "referer泄露", "hsts", "cookie属性", "refresh token"]` | ctf-website | ctf-website/techniques/02-auth/jwt/07-theft-replay.md |
| `["touch injection", "/dev/input", "inputmanager", "motionevent", "accessibilityservice", "aimbot detection", "input_event", "getevent"]` | apk-reverse | apk-reverse/techniques/06-dynamic/03-touch-input-hook.md |
| `["ue4", "gworld", "gnames", "actor chain", "fname pool", "rootcomponent", "relativelocation", "frida fvector"]` | apk-reverse | apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `["valkey", "resp", "redis", "预认证", "pre-auth", "dos", "cve-2026-27623", "断言失败", "assertion failure"]` | ctf-website | ctf-website/techniques/11-dos/01-valkey-resp-dos.md |
| `["web cache deception", "缓存欺骗", "cdn", "静态文件缓存", "path delimiter", "x-cache"]` | ctf-website | ctf-website/techniques/08-infra/web-cache-deception.md |
| `["web crypto api", "math.random", "prng", "rsa", "cryptojs", "extractable", "v8 xorshift128", "jwk", "aes-gcm"]` | ctf-website | ctf-website/techniques/07-client/web-crypto-abuse.md |
| `["websocket", "cswsh", "socket.io", "mqtt", "消息注入", "race condition", "跨域websocket"]` | ctf-website | ctf-website/techniques/07-client/websocket.md |
| `["webview", "addjavascriptinterface", "wkwebview", "javascriptinterface", "deeplink", "url scheme", "桥接攻击", "file://"]` | ctf-website | ctf-website/techniques/21-mobile-bridge/01-webview-attacks.md |
| `["xs-leaks", "side-channel", "frame counting", "cache probing", "corp bypass", "timing attack", "侧信道", "浏览器"]` | ctf-website | ctf-website/techniques/18-cors-csp-advanced/02-xs-leaks-browser-sidechannels.md |
| `["xss", "admin bot", "csp bypass", "dom clobbering", "跨站脚本", "exfiltration", "sanitizer bypass", "headless chrome"]` | ctf-website | ctf-website/techniques/07-client/admin-bot-xss.md |
| `["算法混淆", "algorithm confusion", "rs256", "hs256", "公钥", "jwks", "hmac", "jwt_tool"]` | ctf-website | ctf-website/techniques/02-auth/jwt/02-algorithm-confusion.md |
| `["退信", "ndr", "bounce", "idor", "订单号", "卡密泄露", "order leak", "cwe-639", "cwe-862"]` | ctf-website | ctf-website/techniques/12-payment/payment-email-bounce-idor.md |
| `_0x` | ctf-website | ctf-website/techniques/27-js-reverse/01-ast-deobfuscation-pipeline.md |
| `__proto__` | ctf-website/prototype-pollution | ctf-website/techniques/03-injection/prototype-pollution.md |
| `__schema` | ctf-website/graphql | ctf-website/techniques/03-injection/graphql.md |
| `__typename` | ctf-website/graphql | ctf-website/techniques/03-injection/graphql.md |
| `__webpack_require__` | ctf-website | ctf-website/techniques/27-js-reverse/03-sourcemap-unpack-and-webpack-hijacking.md |
| `_kdartisolatesnapshotdata` | apk-reverse | apk-reverse/techniques/02-native/08-flutter-dart-aot-reconstruction.md |
| `_kdartvmsnapshotdata` | apk-reverse | apk-reverse/techniques/02-native/08-flutter-dart-aot-reconstruction.md |
| `_zn` | pe-reverse | pe-reverse/techniques/03-static-analysis/06-go-rust-binary-reconstruction.md |
| `aarch64` | apk-reverse/native | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md<br>apk-reverse/techniques/02-native/02-pointer-chain-patterns.md<br>apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `aca-header` | ctf-website/cors-csrf | ctf-website/techniques/07-client/cors-csrf.md |
| `access token` | ctf-website/oauth | ctf-website/techniques/02-auth/oauth-sso.md |
| `access-control` | ctf-website/cors-csrf | ctf-website/techniques/07-client/cors-csrf.md |
| `act=getcount 无认证` | ctf-website | ctf-website/techniques/24-database/06-card-platform.md |
| `act=order skey` | ctf-website | ctf-website/techniques/24-database/06-card-platform.md |
| `act=query idor` | ctf-website | ctf-website/techniques/24-database/06-card-platform.md |
| `activation` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `active directory` | ctf-website/ldap | ctf-website/techniques/02-auth/ldap-injection.md |
| `activity` | apk-reverse/manifest | apk-reverse/techniques/03-manifest/01-entry-point-tracing.md |
| `actuator/env spring boot` | ctf-website | ctf-website/techniques/24-database/04-config-exposure.md |
| `addjavascriptinterface` | ctf-website/mobile-bridge | ctf-website/techniques/21-mobile-bridge/01-webview-attacks.md<br>ctf-website/techniques/21-mobile-bridge/02-cordova-reactnative.md |
| `addressofcallbacks` | pe-reverse | pe-reverse/techniques/02-pe-structure/02-tls-callback-analysis.md |
| `adler32 checksum mismatch` | apk-reverse | apk-reverse/techniques/07-packer/02-modern-art-dex-dump-and-repair.md |
| `admin bot` | ctf-website/xss | ctf-website/techniques/07-client/admin-bot-xss.md |
| `adminer` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `adminer /adminer.php` | ctf-website | ctf-website/techniques/24-database/05-backup-log-leak.md |
| `aes` | apk-reverse/crypto, general/crypto | apk-reverse/techniques/04-crypto/01-game-encryption-patterns.md<br>apk-reverse/techniques/04-crypto/02-rc4-custom-crypto.md<br>general/techniques/crypto/01-algorithm-identification.md |
| `aes sbox / te0` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/05-high-entropy-compression-vs-crypto-routing.md |
| `agate` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `ai gateway` | ctf-website/race-lost-update | ctf-website/techniques/12-payment/payment-race-lost-update.md |
| `ai_manifest` | ctf-website | ctf-website/techniques/00-workflow/24h-loop-orchestration.md |
| `aimbot` | general/cheating | general/techniques/cheating/01-memory-hacking.md<br>general/techniques/cheating/02-packet-interception.md<br>general/techniques/cheating/03-esp-wallhack-rendering.md |
| `ajax.php csrf referer` | ctf-website | ctf-website/techniques/24-database/06-card-platform.md |
| `akamai` | ctf-website/cloudflare-bypass | ctf-website/techniques/01-recon/cloudflare-bypass.md |
| `alg:none` | ctf-website/signature-algorithm | ctf-website/techniques/13-signature/01-algorithm.md |
| `algorithm confusion` | ctf-website/signature-algorithm | ctf-website/techniques/13-signature/01-algorithm.md |
| `algorithm downgrade` | ctf-website/signature-algorithm | ctf-website/techniques/13-signature/01-algorithm.md |
| `alias` | ctf-website/graphql | ctf-website/techniques/03-injection/graphql.md |
| `alipay` | ctf-website/payment | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/12-payment/payment-digital-goods.md |
| `allowed_routes` | ctf-website/litellm-privesc | ctf-website/techniques/09-cve/05-litellm-privesc.md |
| `amount` | ctf-website/payment | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/12-payment/payment-digital-goods.md |
| `amount tampering` | ctf-website/payment-bypass | ctf-website/techniques/12-payment/payment-bypass.md |
| `amp amp-access` | ctf-website | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md |
| `amp paywall` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `amp-access` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `amp-access-hide` | ctf-website | ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `amplification` | ctf-website/dos | ctf-website/techniques/22-dos/01-application-layer-dos.md<br>ctf-website/techniques/22-dos/02-resource-exhaustion.md<br>ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `anativewindow` | apk-reverse/dynamic-frida | apk-reverse/techniques/06-dynamic/01-memory-rw-hook.md<br>apk-reverse/techniques/06-dynamic/02-overlay-rendering-hook.md<br>apk-reverse/techniques/06-dynamic/03-touch-input-hook.md |
| `androidemulator` | apk-reverse | apk-reverse/techniques/02-native/07-unidbg-native-emulation-pipeline.md |
| `angr` | general, pe-reverse | general/crypto/02-angr-symbolic-execution-solver.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `angr symbolic execution` | general | general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `anti debug` | pe-reverse/dynamic-analysis | pe-reverse/techniques/04-dynamic-analysis/01-dll-injection.md<br>pe-reverse/techniques/04-dynamic-analysis/02-trampoline-detour.md<br>pe-reverse/techniques/04-dynamic-analysis/03-external-memory-rw.md |
| `anti sandbox` | pe-reverse/av-evasion | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `anti-cheat` | general/cheating | general/techniques/cheating/01-memory-hacking.md<br>general/techniques/cheating/02-packet-interception.md<br>general/techniques/cheating/03-esp-wallhack-rendering.md |
| `anti-debug` | apk-reverse, apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `anti-debug bypass` | general | general/techniques/methodology/02-toolchain-decision-tree.md |
| `anti-debug detection` | general | general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `anti-sandbox` | pe-reverse | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `anticaptcha` | ctf-website/captcha-bypass | ctf-website/techniques/01-recon/captcha-bypass.md |
| `antivirus bypass` | pe-reverse/av-evasion | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `aob` | pe-reverse/triage | pe-reverse/techniques/01-triage/01-aob-signature-scan.md |
| `aob pattern` | pe-reverse | pe-reverse/techniques/07-yara-sigma/01-yara-rule-writing.md |
| `api` | apk-reverse/network, ctf-website/api-attacks | apk-reverse/techniques/05-network/01-game-protocol-hook.md<br>apk-reverse/techniques/05-network/02-license-verification-bypass.md<br>ctf-website/techniques/17-api-attacks/01-api-discovery-leak.md |
| `api hash` | pe-reverse | pe-reverse/techniques/03-static-analysis/05-dynamic-api-resolution.md |
| `api hooking` | pe-reverse | pe-reverse/techniques/03-static-analysis/03-x64dbg-breakpoints.md |
| `api key` | ctf-website/litellm-privesc | ctf-website/techniques/09-cve/05-litellm-privesc.md |
| `api key leak` | ctf-website/api-attacks, ctf-website/signature-key | ctf-website/techniques/13-signature/03-key-attacks.md<br>ctf-website/techniques/17-api-attacks/01-api-discovery-leak.md<br>ctf-website/techniques/17-api-attacks/02-api-key-leak.md |
| `api rate limit 绕过` | ctf-website | ctf-website/techniques/22-dos/10-api-abuse.md |
| `apk sign` | apk-reverse/patch-repack | apk-reverse/techniques/08-patch-repack/01-so-injection-repack.md |
| `apk 推送安装` | general | general/methodology/02-remote-mcp-device-bridge-deployment.md |
| `apktool` | apk-reverse/dex-java, apk-reverse/patch-repack | apk-reverse/techniques/01-dex-java/01-smali-injection.md<br>apk-reverse/techniques/08-patch-repack/01-so-injection-repack.md |
| `app store` | ctf-website/payment-digital-goods | ctf-website/techniques/12-payment/payment-digital-goods.md |
| `app_key` | ctf-website/signature-key | ctf-website/techniques/13-signature/03-key-attacks.md |
| `appinit_dlls` | pe-reverse | pe-reverse/techniques/06-ioc-extraction/02-persistence-startup-chain.md |
| `application-layer denial of service` | ctf-website | ctf-website/techniques/22-dos/01-application-layer-dos.md |
| `archive.is` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `archive.is text-block` | ctf-website | ctf-website/techniques/23-paywall-bypass/04-content-extraction.md |
| `arena-bridge` | general | general/methodology/02-remote-mcp-device-bridge-deployment.md |
| `argon2` | general/crypto | general/techniques/crypto/01-algorithm-identification.md<br>general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `arm` | apk-reverse/native | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md<br>apk-reverse/techniques/02-native/02-pointer-chain-patterns.md<br>apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `art` | apk-reverse/dex-java | apk-reverse/techniques/01-dex-java/01-smali-injection.md |
| `articlebody json-ld` | ctf-website | ctf-website/techniques/23-paywall-bypass/04-content-extraction.md |
| `aslr bypass` | pe-reverse | pe-reverse/techniques/01-triage/01-aob-signature-scan.md |
| `aslr 地址换算` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `aslr 绕过` | pe-reverse | pe-reverse/techniques/01-triage/01-aob-signature-scan.md |
| `asn.1` | general/protocol | general/techniques/protocol/01-unknown-protocol-reverse.md<br>general/techniques/protocol/02-protobuf-flatbuffers-reverse.md |
| `aspack` | pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `assemble` | pe-reverse/static-analysis | pe-reverse/techniques/03-static-analysis/01-struct-reconstruction.md<br>pe-reverse/techniques/03-static-analysis/02-disasm-jit-asm.md<br>pe-reverse/techniques/03-static-analysis/03-x64dbg-breakpoints.md |
| `assertion` | ctf-website/saml | ctf-website/techniques/02-auth/saml-attacks.md |
| `assertion failure` | ctf-website/valkey-resp-dos | ctf-website/techniques/11-dos/01-valkey-resp-dos.md |
| `asset discovery` | ctf-website/fofa | ctf-website/techniques/01-recon/fofa-hunting.md |
| `assume role` | ctf-website/cloud-serverless | ctf-website/techniques/10-cloud/aws-iam-privesc.md<br>ctf-website/techniques/10-cloud/serverless-lambda.md |
| `ast` | ctf-website/js-runtime | ctf-website/techniques/07-client/js-runtime.md |
| `async payment` | ctf-website/payment-callback | ctf-website/techniques/12-payment/payment-callback-async.md |
| `attach` | apk-reverse/dynamic-frida | apk-reverse/techniques/06-dynamic/01-memory-rw-hook.md<br>apk-reverse/techniques/06-dynamic/02-overlay-rendering-hook.md<br>apk-reverse/techniques/06-dynamic/03-touch-input-hook.md |
| `attachbasecontext` | apk-reverse/manifest | apk-reverse/techniques/03-manifest/01-entry-point-tracing.md |
| `attack chain` | ctf-website/attack-network | ctf-website/techniques/attack-network.md |
| `attack graph` | ctf-website/attack-network | ctf-website/techniques/attack-network.md |
| `attack network` | ctf-website/attack-network | ctf-website/techniques/attack-network.md |
| `attack path` | ctf-website/attack-network | ctf-website/techniques/attack-network.md |
| `authencesn` | ctf-website/page-cache-write | general/techniques/01-kernel/01-page-cache-write-family.md |
| `authorization bypass` | ctf-website/idor | ctf-website/techniques/14-idor/01-idor-enumeration.md<br>ctf-website/techniques/14-idor/02-bac-business-logic.md |
| `authorization code` | ctf-website/oauth | ctf-website/techniques/02-auth/oauth-sso.md |
| `authorization header` | ctf-website/jwt | ctf-website/techniques/02-auth/jwt/00-overview.md<br>ctf-website/techniques/02-auth/jwt/01-alg-none.md<br>ctf-website/techniques/02-auth/jwt/02-algorithm-confusion.md |
| `auto-renew` | ctf-website/payment-subscription | ctf-website/techniques/12-payment/payment-subscription.md |
| `automation` | ctf-website/captcha-bypass | ctf-website/techniques/01-recon/captcha-bypass.md |
| `autopilot` | ctf-website/24h-loop-orchestration | ctf-website/techniques/00-workflow/24h-loop-orchestration.md<br>ctf-website/techniques/attack-network.md |
| `av evasion` | pe-reverse/av-evasion | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `aws` | ctf-website/cloud-serverless | ctf-website/techniques/10-cloud/aws-iam-privesc.md<br>ctf-website/techniques/10-cloud/serverless-lambda.md |
| `aws key` | ctf-website/api-attacks | ctf-website/techniques/17-api-attacks/01-api-discovery-leak.md<br>ctf-website/techniques/17-api-attacks/02-api-key-leak.md |
| `axate` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `azure function` | ctf-website/cloud-serverless | ctf-website/techniques/10-cloud/aws-iam-privesc.md<br>ctf-website/techniques/10-cloud/serverless-lambda.md |
| `babel` | ctf-website/js-runtime | ctf-website/techniques/07-client/js-runtime.md |
| `babel ast` | ctf-website | ctf-website/techniques/27-js-reverse/01-ast-deobfuscation-pipeline.md |
| `backtracking` | ctf-website/redos-timing | ctf-website/techniques/03-injection/redos-timing.md |
| `backup` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `backup_20250101.sql` | ctf-website | ctf-website/techniques/24-database/05-backup-log-leak.md |
| `balance` | ctf-website/payment | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/12-payment/payment-digital-goods.md |
| `balance bypass` | ctf-website/race-lost-update | ctf-website/techniques/12-payment/payment-race-lost-update.md |
| `batch idor` | ctf-website/idor | ctf-website/techniques/14-idor/01-idor-enumeration.md<br>ctf-website/techniques/14-idor/02-bac-business-logic.md |
| `battleye` | general, general/cheating | general/techniques/cheating/01-memory-hacking.md<br>general/techniques/cheating/02-packet-interception.md<br>general/techniques/cheating/03-esp-wallhack-rendering.md |
| `bcpg` | pe-reverse | pe-reverse/techniques/10-license-keygen/04-signature-chain-pubkey-swap.md |
| `bcrypt` | general/crypto | general/techniques/crypto/01-algorithm-identification.md<br>general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `bearer` | ctf-website/jwt | ctf-website/techniques/02-auth/jwt/00-overview.md<br>ctf-website/techniques/02-auth/jwt/01-alg-none.md<br>ctf-website/techniques/02-auth/jwt/02-algorithm-confusion.md |
| `beehiiv` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `ber` | general/protocol | general/techniques/protocol/01-unknown-protocol-reverse.md<br>general/techniques/protocol/02-protobuf-flatbuffers-reverse.md |
| `berlekamp-massey` | general | general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `best practice` | general/methodology | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `billion laughs` | ctf-website/dos | ctf-website/techniques/22-dos/01-application-layer-dos.md<br>ctf-website/techniques/22-dos/02-resource-exhaustion.md<br>ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `binary protocol` | general/protocol | general/techniques/protocol/01-unknown-protocol-reverse.md<br>general/techniques/protocol/02-protobuf-flatbuffers-reverse.md |
| `binaryformatter` | ctf-website/deserialization | ctf-website/techniques/05-deserialization/deserialization.md |
| `bingbot` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `blackdex` | apk-reverse, apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-modern-art-dex-dump-and-repair.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md |
| `blind` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `blink` | ctf-website/chrome-uaf-blink | ctf-website/techniques/09-cve/01-browser-sandbox-escape.md |
| `block cipher` | general/crypto | general/techniques/crypto/01-algorithm-identification.md<br>general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `block_regex_general` | ctf-website | ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `bloomberg paywall` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `blutter` | apk-reverse | apk-reverse/techniques/02-native/08-flutter-dart-aot-reconstruction.md |
| `bounce` | ctf-website/payment-bounce-idor | ctf-website/techniques/12-payment/payment-email-bounce-idor.md |
| `bounce callback` | ctf-website/payment-bounce-idor | ctf-website/techniques/12-payment/payment-email-bounce-idor.md |
| `bouncycastle` | pe-reverse | pe-reverse/techniques/10-license-keygen/04-signature-chain-pubkey-swap.md |
| `bpf_prog_test_run` | general | general/techniques/01-kernel/02-slab-cross-cache.md |
| `breakpoint` | pe-reverse/static-analysis | pe-reverse/techniques/03-static-analysis/01-struct-reconstruction.md<br>pe-reverse/techniques/03-static-analysis/02-disasm-jit-asm.md<br>pe-reverse/techniques/03-static-analysis/03-x64dbg-breakpoints.md |
| `broadcast` | apk-reverse/manifest | apk-reverse/techniques/03-manifest/01-entry-point-tracing.md |
| `brute force` | ctf-website/rate-limit | ctf-website/techniques/16-rate-limit/01-rate-limit-bypass.md<br>ctf-website/techniques/16-rate-limit/02-brute-force-tactics.md |
| `bson 注入` | ctf-website | ctf-website/techniques/24-database/03-nosql-injection.md |
| `buffer overflow` | ctf-website/nginx-rewrite-heapoverflow | ctf-website/techniques/09-cve/06-nginx-rewrite-heapoverflow.md |
| `bypass` | general/cheating | general/techniques/cheating/01-memory-hacking.md<br>general/techniques/cheating/02-packet-interception.md<br>general/techniques/cheating/03-esp-wallhack-rendering.md |
| `byte patch` | pe-reverse/patch | pe-reverse/techniques/08-patch/01-code-patching.md |
| `byte pattern` | pe-reverse/triage | pe-reverse/techniques/01-triage/01-aob-signature-scan.md |
| `c14n` | ctf-website/signature-canonicalization | ctf-website/techniques/13-signature/04-canonicalization.md |
| `c2` | pe-reverse/ioc | pe-reverse/techniques/06-ioc-extraction/01-ioc-extraction.md |
| `c2 address` | pe-reverse | pe-reverse/techniques/06-ioc-extraction/01-ioc-extraction.md |
| `cache busting 随机查询参数` | ctf-website | ctf-website/techniques/22-dos/09-cache-cdn-dos.md |
| `cache deception` | ctf-website/cache-deception | ctf-website/techniques/08-infra/web-cache-deception.md |
| `cache hit` | ctf-website/cache-deception | ctf-website/techniques/08-infra/web-cache-deception.md |
| `cache hit rate 接近 0%` | ctf-website | ctf-website/techniques/22-dos/07-dns-dos.md |
| `cache poison 投毒` | ctf-website | ctf-website/techniques/22-dos/09-cache-cdn-dos.md |
| `cache poisoning` | ctf-website/race-smuggling | ctf-website/techniques/08-infra/race-cache-smuggling.md |
| `cached response` | ctf-website/cache-deception | ctf-website/techniques/08-infra/web-cache-deception.md |
| `caldav` | ctf-website/cpanel-caldav-traversal | ctf-website/techniques/09-cve/03-cpanel-caldav-traversal.md |
| `callback` | ctf-website/payment | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/12-payment/payment-digital-goods.md |
| `cannot read properties of undefined` | ctf-website | ctf-website/techniques/27-js-reverse/02-browser-env-emulation-proxy-sandbox.md |
| `canonicalization` | ctf-website/signature-canonicalization | ctf-website/techniques/13-signature/04-canonicalization.md |
| `canvas 指纹` | ctf-website | ctf-website/techniques/27-js-reverse/02-browser-env-emulation-proxy-sandbox.md |
| `capacitor` | ctf-website/mobile-bridge | ctf-website/techniques/21-mobile-bridge/01-webview-attacks.md<br>ctf-website/techniques/21-mobile-bridge/02-cordova-reactnative.md |
| `capsolver` | ctf-website/captcha-bypass | ctf-website/techniques/01-recon/captcha-bypass.md |
| `captcha` | ctf-website/captcha-bypass | ctf-website/techniques/01-recon/captcha-bypass.md |
| `capture group` | ctf-website/nginx-rewrite-heapoverflow | ctf-website/techniques/09-cve/06-nginx-rewrite-heapoverflow.md |
| `card key leak` | ctf-website/payment-bounce-idor | ctf-website/techniques/12-payment/payment-email-bounce-idor.md |
| `cashier` | ctf-website/payment-php | ctf-website/techniques/12-payment/payment-php.md |
| `catastrophic backtracking` | ctf-website/redos-timing | ctf-website/techniques/03-injection/redos-timing.md |
| `cbc` | apk-reverse/crypto | apk-reverse/techniques/04-crypto/01-game-encryption-patterns.md<br>apk-reverse/techniques/04-crypto/02-rc4-custom-crypto.md |
| `cdk` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `cdk 明文泄露` | ctf-website | ctf-website/techniques/24-database/06-card-platform.md |
| `cdkey` | ctf-website/payment-digital-goods | ctf-website/techniques/12-payment/payment-digital-goods.md |
| `cdn` | ctf-website/cloudflare-bypass | ctf-website/techniques/01-recon/cloudflare-bypass.md |
| `cdn bypass` | ctf-website/cloudflare-bypass | ctf-website/techniques/01-recon/cloudflare-bypass.md |
| `cdn cache` | ctf-website/cache-deception | ctf-website/techniques/08-infra/web-cache-deception.md |
| `cdn gadget` | ctf-website/csp-cors-advanced | ctf-website/techniques/18-cors-csp-advanced/01-csp-bypass.md<br>ctf-website/techniques/18-cors-csp-advanced/02-xs-leaks-browser-sidechannels.md |
| `cdn 边缘节点 cpu 异常` | ctf-website | ctf-website/techniques/22-dos/09-cache-cdn-dos.md |
| `censys` | ctf-website/cloudflare-bypass | ctf-website/techniques/01-recon/cloudflare-bypass.md |
| `certificate` | apk-reverse/crypto, apk-reverse/network | apk-reverse/techniques/04-crypto/01-game-encryption-patterns.md<br>apk-reverse/techniques/04-crypto/02-rc4-custom-crypto.md<br>apk-reverse/techniques/05-network/01-game-protocol-hook.md |
| `certificate pinning failure` | apk-reverse | apk-reverse/techniques/05-network/03-tls-pinning-unpinning.md |
| `certificate transparency` | ctf-website/cloudflare-bypass | ctf-website/techniques/01-recon/cloudflare-bypass.md |
| `cf-cache-status` | ctf-website/cloudflare-bypass | ctf-website/techniques/01-recon/cloudflare-bypass.md |
| `cf-ray` | ctf-website/cloudflare-bypass | ctf-website/techniques/01-recon/cloudflare-bypass.md |
| `chacha20 expand 32-byte k` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/05-high-entropy-compression-vs-crypto-routing.md |
| `chage` | ctf-website/fd-theft-pidfd | general/techniques/01-kernel/03-mm-null-ptrace-bypass.md |
| `channel verify` | apk-reverse/network | apk-reverse/techniques/05-network/01-game-protocol-hook.md<br>apk-reverse/techniques/05-network/02-license-verification-bypass.md |
| `cheat` | general/cheating | general/techniques/cheating/01-memory-hacking.md<br>general/techniques/cheating/02-packet-interception.md<br>general/techniques/cheating/03-esp-wallhack-rendering.md |
| `cheat engine` | pe-reverse | pe-reverse/techniques/03-static-analysis/04-reclass-reconstruction.md |
| `check sign` | ctf-website/signature | ctf-website/techniques/13-signature/00-overview.md<br>ctf-website/techniques/13-signature/01-algorithm.md<br>ctf-website/techniques/13-signature/02-implementation.md |
| `checkkey` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `checklist` | general/methodology | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `checkout` | ctf-website/payment | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/12-payment/payment-digital-goods.md |
| `checkpoint` | ctf-website, ctf-website/24h-loop-orchestration | ctf-website/techniques/00-workflow/24h-loop-orchestration.md<br>ctf-website/techniques/attack-network.md |
| `checksum` | general/protocol | general/techniques/protocol/01-unknown-protocol-reverse.md<br>general/techniques/protocol/02-protobuf-flatbuffers-reverse.md |
| `checksum bypass` | general | general/techniques/cheating/02-packet-interception.md |
| `chrome` | ctf-website/chrome-uaf-blink | ctf-website/techniques/09-cve/01-browser-sandbox-escape.md |
| `chromium` | ctf-website/chrome-uaf-blink | ctf-website/techniques/09-cve/01-browser-sandbox-escape.md |
| `ci/cd` | ctf-website/ci-cd | ctf-website/techniques/10-cloud/ci-cd-pipeline.md<br>ctf-website/techniques/10-cloud/github-actions-abuse-paths.md<br>ctf-website/techniques/10-cloud/terraform-state-secrets.md |
| `cifs` | ctf-website/cifswitch-nss | general/techniques/01-kernel/04-cifswitch-nss-privesc.md |
| `cifs.spnego` | general | general/techniques/01-kernel/04-cifswitch-nss-privesc.md |
| `cifs.upcall` | general | general/techniques/01-kernel/04-cifswitch-nss-privesc.md |
| `cifswitch` | ctf-website/cifswitch-nss | general/techniques/01-kernel/04-cifswitch-nss-privesc.md |
| `cipher` | apk-reverse/crypto, general/crypto | apk-reverse/techniques/04-crypto/01-game-encryption-patterns.md<br>apk-reverse/techniques/04-crypto/02-rc4-custom-crypto.md<br>general/techniques/crypto/01-algorithm-identification.md |
| `cl.te` | ctf-website/race-smuggling | ctf-website/techniques/08-infra/race-cache-smuggling.md |
| `claripy` | general | general/crypto/02-angr-symbolic-execution-solver.md |
| `class` | apk-reverse/dex-java | apk-reverse/techniques/01-dex-java/01-smali-injection.md |
| `classes.dex hash` | apk-reverse | apk-reverse/techniques/08-patch-repack/02-signature-integrity-bypass.md |
| `classloader` | apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `cldap rootdse 反射` | ctf-website | ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `clock interpolation` | general | general/techniques/cheating/05-speedhack-time-manipulation.md |
| `clock_gettime` | apk-reverse | apk-reverse/techniques/07-packer/05-vmp-anti-debug-bypass.md |
| `cloud function` | ctf-website/cloud-serverless | ctf-website/techniques/10-cloud/aws-iam-privesc.md<br>ctf-website/techniques/10-cloud/serverless-lambda.md |
| `cloudflare` | ctf-website/cloudflare-bypass | ctf-website/techniques/01-recon/cloudflare-bypass.md |
| `cloudflare 1010` | general | general/methodology/02-remote-mcp-device-bridge-deployment.md |
| `cloudfront` | ctf-website/cloudflare-bypass | ctf-website/techniques/01-recon/cloudflare-bypass.md |
| `cloudfront takeover` | ctf-website/dns-email | ctf-website/techniques/19-dns-email/01-subdomain-takeover.md<br>ctf-website/techniques/19-dns-email/02-email-spoofing.md |
| `cname takeover` | ctf-website/dns-email | ctf-website/techniques/19-dns-email/01-subdomain-takeover.md<br>ctf-website/techniques/19-dns-email/02-email-spoofing.md |
| `cobalt strike` | pe-reverse/av-evasion | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `code patch` | pe-reverse/patch | pe-reverse/techniques/08-patch/01-code-patching.md |
| `comdat 折叠` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `command injection` | windows | windows/techniques/notepadpp-config-injection.md |
| `commandlineinterpreter` | ctf-website/notepadpp-config-injection | windows/techniques/notepadpp-config-injection.md |
| `composer` | ctf-website/payment-php | ctf-website/techniques/12-payment/payment-php.md |
| `concurrent` | ctf-website/race-smuggling | ctf-website/techniques/08-infra/race-cache-smuggling.md |
| `concurrent bypass` | ctf-website/rate-limit | ctf-website/techniques/16-rate-limit/01-rate-limit-bypass.md<br>ctf-website/techniques/16-rate-limit/02-brute-force-tactics.md |
| `condition` | pe-reverse/yara-sigma | pe-reverse/techniques/07-yara-sigma/01-yara-rule-writing.md |
| `conditional bp` | pe-reverse/static-analysis | pe-reverse/techniques/03-static-analysis/01-struct-reconstruction.md<br>pe-reverse/techniques/03-static-analysis/02-disasm-jit-asm.md<br>pe-reverse/techniques/03-static-analysis/03-x64dbg-breakpoints.md |
| `conditional breakpoint` | pe-reverse | pe-reverse/techniques/03-static-analysis/03-x64dbg-breakpoints.md |
| `confidence labeling` | pe-reverse | pe-reverse/techniques/06-ioc-extraction/01-ioc-extraction.md |
| `config.php` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `config.php backup .bak .swp` | ctf-website | ctf-website/techniques/24-database/04-config-exposure.md |
| `config.xml` | windows | windows/techniques/notepadpp-config-injection.md |
| `configuration poisoning` | windows | windows/techniques/notepadpp-config-injection.md |
| `connection string` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `conntrack table full` | ctf-website | ctf-website/techniques/22-dos/06-tcp-state-exhaustion.md |
| `constructor.prototype` | ctf-website/prototype-pollution | ctf-website/techniques/03-injection/prototype-pollution.md |
| `container` | ctf-website/kubernetes | ctf-website/techniques/10-cloud/container-runtime-escape.md<br>ctf-website/techniques/10-cloud/k8s-rbac-attack-paths.md<br>ctf-website/techniques/10-cloud/kubernetes-container.md |
| `containerd` | ctf-website/kubernetes | ctf-website/techniques/10-cloud/container-runtime-escape.md<br>ctf-website/techniques/10-cloud/k8s-rbac-attack-paths.md<br>ctf-website/techniques/10-cloud/kubernetes-container.md |
| `content security policy` | ctf-website/csp-cors-advanced, ctf-website/xss | ctf-website/techniques/07-client/admin-bot-xss.md<br>ctf-website/techniques/18-cors-csp-advanced/01-csp-bypass.md<br>ctf-website/techniques/18-cors-csp-advanced/02-xs-leaks-browser-sidechannels.md |
| `contextisolation` | ctf-website/mobile-bridge | ctf-website/techniques/21-mobile-bridge/01-webview-attacks.md<br>ctf-website/techniques/21-mobile-bridge/02-cordova-reactnative.md |
| `continuation` | ctf-website/http2 | ctf-website/techniques/08-infra/http2-attacks.md |
| `continuation 帧无 end_headers` | ctf-website | ctf-website/techniques/22-dos/05-http2-continuation.md |
| `control flow flattening` | apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `cookie articlereads metercount` | ctf-website | ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md |
| `cookie paywall` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `copy fail` | ctf-website/page-cache-write | general/techniques/01-kernel/01-page-cache-write-family.md |
| `cordova` | ctf-website/mobile-bridge | ctf-website/techniques/21-mobile-bridge/01-webview-attacks.md<br>ctf-website/techniques/21-mobile-bridge/02-cordova-reactnative.md |
| `core::result::result` | pe-reverse | pe-reverse/techniques/03-static-analysis/06-go-rust-binary-reconstruction.md |
| `corrupt pe header in ida` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/06-modern-pe-unmapping-and-dump-reconstruction.md |
| `cors` | ctf-website/cors-csrf | ctf-website/techniques/07-client/cors-csrf.md |
| `couchdb _all_dbs` | ctf-website | ctf-website/techniques/24-database/03-nosql-injection.md |
| `coupon` | ctf-website/payment | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/12-payment/payment-digital-goods.md |
| `coupon abuse` | ctf-website/payment-bypass | ctf-website/techniques/12-payment/payment-bypass.md |
| `coupon stacking` | ctf-website/mass-assignment | ctf-website/techniques/15-mass-assignment/01-mass-assignment.md<br>ctf-website/techniques/15-mass-assignment/02-parameter-tampering.md |
| `cpanel` | ctf-website/cpanel-caldav-traversal | ctf-website/techniques/09-cve/03-cpanel-caldav-traversal.md |
| `cpdavd` | ctf-website/cpanel-caldav-traversal | ctf-website/techniques/09-cve/03-cpanel-caldav-traversal.md |
| `cpe` | ctf-website/cve | ctf-website/techniques/09-cve/cve-correlation-graph.md<br>ctf-website/techniques/09-cve/cve-workflow.md<br>ctf-website/techniques/09-cve/multi-cve-chain-playbook.md |
| `crashloopbackoff` | ctf-website | ctf-website/techniques/22-dos/11-cloud-container-dos.md |
| `crc` | general/protocol | general/techniques/protocol/01-unknown-protocol-reverse.md<br>general/techniques/protocol/02-protobuf-flatbuffers-reverse.md |
| `crc reverse` | general | general/techniques/protocol/01-unknown-protocol-reverse.md |
| `crc 校验` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `createremotethread` | pe-reverse, pe-reverse/dynamic-analysis | pe-reverse/techniques/04-dynamic-analysis/01-dll-injection.md<br>pe-reverse/techniques/04-dynamic-analysis/02-trampoline-detour.md<br>pe-reverse/techniques/04-dynamic-analysis/03-external-memory-rw.md |
| `createservice` | pe-reverse | pe-reverse/techniques/06-ioc-extraction/02-persistence-startup-chain.md |
| `credential spraying` | ctf-website/rate-limit | ctf-website/techniques/16-rate-limit/01-rate-limit-bypass.md<br>ctf-website/techniques/16-rate-limit/02-brute-force-tactics.md |
| `crlf` | ctf-website/hpp-crlf | ctf-website/techniques/03-injection/hpp-crlf.md |
| `crlf injection` | ctf-website/hpp-crlf | ctf-website/techniques/03-injection/hpp-crlf.md |
| `cronetengine` | apk-reverse | apk-reverse/techniques/05-network/03-tls-pinning-unpinning.md |
| `cross cache` | ctf-website/slab-cross-cache | general/techniques/01-kernel/02-slab-cross-cache.md |
| `cross origin` | ctf-website/cors-csrf | ctf-website/techniques/07-client/cors-csrf.md |
| `cross origin communication` | ctf-website/postmessage | ctf-website/techniques/07-client/postmessage.md |
| `cross site scripting` | ctf-website/xss | ctf-website/techniques/07-client/admin-bot-xss.md |
| `cross-site leak` | ctf-website/csp-cors-advanced | ctf-website/techniques/18-cors-csp-advanced/01-csp-bypass.md<br>ctf-website/techniques/18-cors-csp-advanced/02-xs-leaks-browser-sidechannels.md |
| `cross-site request forgery` | ctf-website/cors-csrf | ctf-website/techniques/07-client/cors-csrf.md |
| `crt.sh` | ctf-website/cloudflare-bypass | ctf-website/techniques/01-recon/cloudflare-bypass.md |
| `crt.sh 证书透明度` | ctf-website | ctf-website/techniques/22-dos/09-cache-cdn-dos.md |
| `crypt` | apk-reverse/crypto | apk-reverse/techniques/04-crypto/01-game-encryption-patterns.md<br>apk-reverse/techniques/04-crypto/02-rc4-custom-crypto.md |
| `crypto.subtle` | ctf-website/web-crypto | ctf-website/techniques/07-client/web-crypto-abuse.md |
| `cryptojs` | ctf-website/js-runtime | ctf-website/techniques/07-client/js-runtime.md |
| `cs_code 规则引擎` | ctf-website | ctf-website/techniques/23-paywall-bypass/05-dom-css-manipulation.md |
| `csp` | ctf-website/xss | ctf-website/techniques/07-client/admin-bot-xss.md |
| `csp bypass` | ctf-website/csp-cors-advanced | ctf-website/techniques/18-cors-csp-advanced/01-csp-bypass.md<br>ctf-website/techniques/18-cors-csp-advanced/02-xs-leaks-browser-sidechannels.md |
| `csp evaluator` | ctf-website/csp-cors-advanced | ctf-website/techniques/18-cors-csp-advanced/01-csp-bypass.md<br>ctf-website/techniques/18-cors-csp-advanced/02-xs-leaks-browser-sidechannels.md |
| `csp injection script-src` | ctf-website | ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `csrf` | ctf-website/cors-csrf | ctf-website/techniques/07-client/cors-csrf.md |
| `cssfontfeaturevalues` | ctf-website/chrome-uaf-blink | ctf-website/techniques/09-cve/01-browser-sandbox-escape.md |
| `cswsh` | ctf-website/websocket | ctf-website/techniques/07-client/websocket.md |
| `ctf_autopilot` | ctf-website | ctf-website/techniques/00-workflow/24h-loop-orchestration.md |
| `currency attack` | ctf-website/payment-bypass | ctf-website/techniques/12-payment/payment-bypass.md |
| `currency confusion` | ctf-website/mass-assignment | ctf-website/techniques/15-mass-assignment/01-mass-assignment.md<br>ctf-website/techniques/15-mass-assignment/02-parameter-tampering.md |
| `cursor 分页遍历` | ctf-website | ctf-website/techniques/22-dos/10-api-abuse.md |
| `custom crypto` | general/crypto | general/techniques/crypto/01-algorithm-identification.md<br>general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `custom encrypt` | apk-reverse/crypto | apk-reverse/techniques/04-crypto/01-game-encryption-patterns.md<br>apk-reverse/techniques/04-crypto/02-rc4-custom-crypto.md |
| `custom protocol` | general/protocol | general/techniques/protocol/01-unknown-protocol-reverse.md<br>general/techniques/protocol/02-protobuf-flatbuffers-reverse.md |
| `cve` | ctf-website/cve | ctf-website/techniques/09-cve/cve-correlation-graph.md<br>ctf-website/techniques/09-cve/cve-workflow.md<br>ctf-website/techniques/09-cve/multi-cve-chain-playbook.md |
| `cve-2011-1473 openssl` | ctf-website | ctf-website/techniques/22-dos/08-tls-exhaustion.md |
| `cve-2017-12635 couchdb` | ctf-website | ctf-website/techniques/24-database/03-nosql-injection.md |
| `cve-2023-44487` | ctf-website/dos | ctf-website/techniques/22-dos/01-application-layer-dos.md<br>ctf-website/techniques/22-dos/02-resource-exhaustion.md<br>ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `cve-2024-27316` | ctf-website | ctf-website/techniques/22-dos/05-http2-continuation.md |
| `cve-2026-2441` | ctf-website/chrome-uaf-blink | ctf-website/techniques/09-cve/01-browser-sandbox-escape.md |
| `cve-2026-25243` | ctf-website/redis-valkey-restore-zipmap | ctf-website/techniques/09-cve/02-redis-zipmap-rce.md |
| `cve-2026-27623` | ctf-website/valkey-resp-dos | ctf-website/techniques/11-dos/01-valkey-resp-dos.md |
| `cve-2026-29205` | ctf-website/cpanel-caldav-traversal | ctf-website/techniques/09-cve/03-cpanel-caldav-traversal.md |
| `cve-2026-31429` | ctf-website/slab-cross-cache | general/techniques/01-kernel/02-slab-cross-cache.md |
| `cve-2026-31431` | general | general/techniques/01-kernel/01-page-cache-write-family.md |
| `cve-2026-31635` | ctf-website/page-cache-write | general/techniques/01-kernel/01-page-cache-write-family.md |
| `cve-2026-42945` | ctf-website/nginx-rewrite-heapoverflow | ctf-website/techniques/09-cve/06-nginx-rewrite-heapoverflow.md |
| `cve-2026-43284` | general | general/techniques/01-kernel/01-page-cache-write-family.md |
| `cve-2026-43500` | general | general/techniques/01-kernel/01-page-cache-write-family.md |
| `cve-2026-46300` | general | general/techniques/01-kernel/01-page-cache-write-family.md |
| `cve-2026-46333` | ctf-website/fd-theft-pidfd | general/techniques/01-kernel/03-mm-null-ptrace-bypass.md |
| `cve-2026-47101` | ctf-website/litellm-privesc | ctf-website/techniques/09-cve/05-litellm-privesc.md |
| `cve-2026-48778` | windows | windows/techniques/notepadpp-config-injection.md |
| `cve-2026-53519` | ctf-website/nezha-path-traversal | ctf-website/techniques/09-cve/04-nezha-path-traversal-jwt.md |
| `cvss` | ctf-website/cve | ctf-website/techniques/09-cve/cve-correlation-graph.md<br>ctf-website/techniques/09-cve/cve-workflow.md<br>ctf-website/techniques/09-cve/multi-cve-chain-playbook.md |
| `cwe` | ctf-website/cve | ctf-website/techniques/09-cve/cve-correlation-graph.md<br>ctf-website/techniques/09-cve/cve-workflow.md<br>ctf-website/techniques/09-cve/multi-cve-chain-playbook.md |
| `cwe-200` | ctf-website/payment-bounce-idor | ctf-website/techniques/12-payment/payment-email-bounce-idor.md |
| `cwe-639` | ctf-website/idor, ctf-website/payment-bounce-idor | ctf-website/techniques/12-payment/payment-email-bounce-idor.md<br>ctf-website/techniques/14-idor/01-idor-enumeration.md<br>ctf-website/techniques/14-idor/02-bac-business-logic.md |
| `cwe-862` | ctf-website/payment-bounce-idor | ctf-website/techniques/12-payment/payment-email-bounce-idor.md |
| `cwe-915` | ctf-website/mass-assignment | ctf-website/techniques/15-mass-assignment/01-mass-assignment.md<br>ctf-website/techniques/15-mass-assignment/02-parameter-tampering.md |
| `d3d hook` | general/cheating | general/techniques/cheating/01-memory-hacking.md<br>general/techniques/cheating/02-packet-interception.md<br>general/techniques/cheating/03-esp-wallhack-rendering.md |
| `d810` | pe-reverse | pe-reverse/techniques/03-static-analysis/07-ida-microcode-mba-deobfuscation-d810.md |
| `d810-ng` | pe-reverse | pe-reverse/techniques/03-static-analysis/07-ida-microcode-mba-deobfuscation-d810.md |
| `dalvik` | apk-reverse/dex-java | apk-reverse/techniques/01-dex-java/01-smali-injection.md |
| `dangling dns` | ctf-website/dns-email | ctf-website/techniques/19-dns-email/01-subdomain-takeover.md<br>ctf-website/techniques/19-dns-email/02-email-spoofing.md |
| `dangling pointer` | general | general/techniques/01-kernel/05-pintheft-io-uring-page-cache.md |
| `dart aot` | apk-reverse | apk-reverse/techniques/02-native/08-flutter-dart-aot-reconstruction.md |
| `dashboard` | ctf-website/nezha-path-traversal | ctf-website/techniques/09-cve/04-nezha-path-traversal-jwt.md |
| `data obfuscation` | general | general/techniques/cheating/01-memory-hacking.md |
| `database` | ctf-website/database-attacks, ctf-website/sqli | ctf-website/techniques/03-injection/sqli-nosqli.md<br>ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md |
| `ddddocr` | ctf-website/captcha-bypass | ctf-website/techniques/01-recon/captcha-bypass.md |
| `ddos` | ctf-website/dos | ctf-website/techniques/22-dos/01-application-layer-dos.md<br>ctf-website/techniques/22-dos/02-resource-exhaustion.md<br>ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `decision tree` | general, general/methodology | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `declarativenetrequest` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `declarativenetrequest block` | ctf-website | ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `declarativenetrequest modifyheaders` | ctf-website | ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md |
| `decompile` | apk-reverse/dex-java | apk-reverse/techniques/01-dex-java/01-smali-injection.md |
| `decrypt` | apk-reverse/crypto, general/crypto | apk-reverse/techniques/04-crypto/01-game-encryption-patterns.md<br>apk-reverse/techniques/04-crypto/02-rc4-custom-crypto.md<br>general/techniques/crypto/01-algorithm-identification.md |
| `deep copy` | ctf-website/prototype-pollution | ctf-website/techniques/03-injection/prototype-pollution.md |
| `deeplink` | ctf-website/mobile-bridge | ctf-website/techniques/21-mobile-bridge/01-webview-attacks.md<br>ctf-website/techniques/21-mobile-bridge/02-cordova-reactnative.md |
| `default password` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `defender bypass` | pe-reverse/av-evasion | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `deflate` | pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `denial of service` | ctf-website/dos | ctf-website/techniques/22-dos/01-application-layer-dos.md<br>ctf-website/techniques/22-dos/02-resource-exhaustion.md<br>ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `deobfuscate` | ctf-website/js-runtime | ctf-website/techniques/07-client/js-runtime.md |
| `deobfuscation` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `dependency confusion` | ctf-website/supply-chain | ctf-website/techniques/11-supply-chain/dependency-confusion.md |
| `depth buffer manipulation` | general | general/techniques/cheating/03-esp-wallhack-rendering.md |
| `der` | general/protocol | general/techniques/protocol/01-unknown-protocol-reverse.md<br>general/techniques/protocol/02-protobuf-flatbuffers-reverse.md |
| `des` | apk-reverse/crypto, general/crypto | apk-reverse/techniques/04-crypto/01-game-encryption-patterns.md<br>apk-reverse/techniques/04-crypto/02-rc4-custom-crypto.md<br>general/techniques/crypto/01-algorithm-identification.md |
| `deserialization` | ctf-website/deserialization | ctf-website/techniques/05-deserialization/deserialization.md |
| `deserialize form` | pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `detection` | pe-reverse/yara-sigma | pe-reverse/techniques/07-yara-sigma/01-yara-rule-writing.md |
| `detour` | pe-reverse, pe-reverse/dynamic-analysis | pe-reverse/techniques/04-dynamic-analysis/01-dll-injection.md<br>pe-reverse/techniques/04-dynamic-analysis/02-trampoline-detour.md<br>pe-reverse/techniques/04-dynamic-analysis/03-external-memory-rw.md |
| `devirtualization` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `dex` | apk-reverse/dex-java | apk-reverse/techniques/01-dex-java/01-smali-injection.md |
| `dex 035 magic` | apk-reverse | apk-reverse/techniques/07-packer/02-modern-art-dex-dump-and-repair.md |
| `dex2c` | apk-reverse, apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `dex_fix` | apk-reverse | apk-reverse/techniques/07-packer/02-modern-art-dex-dump-and-repair.md |
| `dexclassloader` | apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `dexfile` | apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `dialogboxparama hook` | general | general/methodology/01-headless-emulation-windows-android-handbook.md |
| `dict:// gopher:// 协议走私` | ctf-website | ctf-website/techniques/22-dos/12-ssrf-dos.md |
| `die() exit() 缺失` | ctf-website | ctf-website/techniques/24-database/06-card-platform.md |
| `die缺失` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `differential analysis` | general | general/techniques/protocol/01-unknown-protocol-reverse.md |
| `diffie-hellman` | general/crypto | general/techniques/crypto/01-algorithm-identification.md<br>general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `digital goods` | ctf-website/payment-digital-goods | ctf-website/techniques/12-payment/payment-digital-goods.md |
| `direct syscall` | general, pe-reverse, pe-reverse/dynamic-analysis | general/techniques/cheating/04-anti-cheat-bypass.md<br>pe-reverse/techniques/04-dynamic-analysis/01-dll-injection.md<br>pe-reverse/techniques/04-dynamic-analysis/02-trampoline-detour.md |
| `directory` | ctf-website/recon | ctf-website/techniques/01-recon/recon-routing.md<br>ctf-website/techniques/01-recon/version-fingerprinting.md |
| `directory service` | ctf-website/ldap | ctf-website/techniques/02-auth/ldap-injection.md |
| `directx hook` | general | general/techniques/cheating/03-esp-wallhack-rendering.md |
| `dirty frag` | ctf-website/page-cache-write | general/techniques/01-kernel/01-page-cache-write-family.md |
| `dirtydecrypt` | ctf-website/page-cache-write | general/techniques/01-kernel/01-page-cache-write-family.md |
| `disassemble` | pe-reverse/static-analysis | pe-reverse/techniques/03-static-analysis/01-struct-reconstruction.md<br>pe-reverse/techniques/03-static-analysis/02-disasm-jit-asm.md<br>pe-reverse/techniques/03-static-analysis/03-x64dbg-breakpoints.md |
| `discount` | ctf-website/payment | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/12-payment/payment-digital-goods.md |
| `discount abuse` | ctf-website/payment-bypass | ctf-website/techniques/12-payment/payment-bypass.md |
| `dispatcher` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `dkim` | ctf-website/dns-email | ctf-website/techniques/19-dns-email/01-subdomain-takeover.md<br>ctf-website/techniques/19-dns-email/02-email-spoofing.md |
| `dll inject` | pe-reverse/dynamic-analysis | pe-reverse/techniques/04-dynamic-analysis/01-dll-injection.md<br>pe-reverse/techniques/04-dynamic-analysis/02-trampoline-detour.md<br>pe-reverse/techniques/04-dynamic-analysis/03-external-memory-rw.md |
| `dll 注入` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/01-dll-injection.md |
| `dllmain` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/01-dll-injection.md |
| `dlopen` | apk-reverse | apk-reverse/techniques/02-native/07-unidbg-native-emulation-pipeline.md |
| `dma attack` | general, general/cheating | general/techniques/cheating/01-memory-hacking.md<br>general/techniques/cheating/02-packet-interception.md<br>general/techniques/cheating/03-esp-wallhack-rendering.md |
| `dmarc` | ctf-website/dns-email | ctf-website/techniques/19-dns-email/01-subdomain-takeover.md<br>ctf-website/techniques/19-dns-email/02-email-spoofing.md |
| `dns amplification` | ctf-website/dos | ctf-website/techniques/22-dos/01-application-layer-dos.md<br>ctf-website/techniques/22-dos/02-resource-exhaustion.md<br>ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `dns amplification any 查询` | ctf-website | ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `dns cache poisoning` | ctf-website | ctf-website/techniques/22-dos/07-dns-dos.md |
| `dns history` | ctf-website/cloudflare-bypass | ctf-website/techniques/01-recon/cloudflare-bypass.md |
| `dns rebinding` | ctf-website/ssrf | ctf-website/techniques/04-ssrf/ssrf.md |
| `dns 权威服务器 qps 异常` | ctf-website | ctf-website/techniques/22-dos/07-dns-dos.md |
| `dnslog` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `dnssec any 查询放大` | ctf-website | ctf-website/techniques/22-dos/07-dns-dos.md |
| `docker` | ctf-website/kubernetes | ctf-website/techniques/10-cloud/container-runtime-escape.md<br>ctf-website/techniques/10-cloud/k8s-rbac-attack-paths.md<br>ctf-website/techniques/10-cloud/kubernetes-container.md |
| `docker.sock` | ctf-website/kubernetes | ctf-website/techniques/10-cloud/container-runtime-escape.md<br>ctf-website/techniques/10-cloud/k8s-rbac-attack-paths.md<br>ctf-website/techniques/10-cloud/kubernetes-container.md |
| `document is not defined` | ctf-website | ctf-website/techniques/27-js-reverse/02-browser-env-emulation-proxy-sandbox.md |
| `dom clobber` | ctf-website/csp-cors-advanced | ctf-website/techniques/18-cors-csp-advanced/01-csp-bypass.md<br>ctf-website/techniques/18-cors-csp-advanced/02-xs-leaks-browser-sidechannels.md |
| `dom clobbering` | ctf-website/xss | ctf-website/techniques/07-client/admin-bot-xss.md |
| `domain` | pe-reverse/ioc | pe-reverse/techniques/06-ioc-extraction/01-ioc-extraction.md |
| `dompurify` | ctf-website/xss | ctf-website/techniques/07-client/admin-bot-xss.md |
| `dompurify sanitize` | ctf-website | ctf-website/techniques/23-paywall-bypass/04-content-extraction.md |
| `dos` | ctf-website/dos | ctf-website/techniques/22-dos/01-application-layer-dos.md<br>ctf-website/techniques/22-dos/02-resource-exhaustion.md<br>ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `dos header` | pe-reverse/pe-structure | pe-reverse/techniques/02-pe-structure/01-pe-header-parsing.md |
| `dos header broken` | pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `dos 头非 mz (0x15 0x5a / 0x00 0x00)` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/04-twinbasic-compressed-resource-recovery.md |
| `double free` | ctf-website/pintheft-io-uring | general/techniques/01-kernel/05-pintheft-io-uring-page-cache.md |
| `double spend` | ctf-website/race-lost-update, ctf-website/race-smuggling | ctf-website/techniques/08-infra/race-cache-smuggling.md<br>ctf-website/techniques/12-payment/payment-race-lost-update.md |
| `double-free` | general | general/techniques/01-kernel/05-pintheft-io-uring-page-cache.md |
| `dpake` | general/crypto | general/techniques/crypto/01-algorithm-identification.md<br>general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `drdos` | ctf-website/dos | ctf-website/techniques/22-dos/01-application-layer-dos.md<br>ctf-website/techniques/22-dos/02-resource-exhaustion.md<br>ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `drdos distributed reflection dos` | ctf-website | ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `dse` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `dump` | apk-reverse, ctf-website/database-attacks, pe-reverse | apk-reverse/techniques/07-packer/04-vmp-dump-trace-recovery.md<br>ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md |
| `dumpable check` | general | general/techniques/01-kernel/03-mm-null-ptrace-bypass.md |
| `dumped dex corrupt` | apk-reverse | apk-reverse/techniques/07-packer/02-modern-art-dex-dump-and-repair.md |
| `dynamic planning` | general | general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `e_lfanew` | pe-reverse/pe-structure | pe-reverse/techniques/02-pe-structure/01-pe-header-parsing.md |
| `eac` | general, general/cheating | general/techniques/cheating/01-memory-hacking.md<br>general/techniques/cheating/02-packet-interception.md<br>general/techniques/cheating/03-esp-wallhack-rendering.md |
| `easy anti-cheat` | general/cheating | general/techniques/cheating/01-memory-hacking.md<br>general/techniques/cheating/02-packet-interception.md<br>general/techniques/cheating/03-esp-wallhack-rendering.md |
| `eat` | pe-reverse/pe-structure | pe-reverse/techniques/02-pe-structure/01-pe-header-parsing.md |
| `ecb` | apk-reverse/crypto, ctf-website/web-crypto | apk-reverse/techniques/04-crypto/01-game-encryption-patterns.md<br>apk-reverse/techniques/04-crypto/02-rc4-custom-crypto.md<br>ctf-website/techniques/07-client/web-crypto-abuse.md |
| `ecb detection` | general | general/techniques/crypto/01-algorithm-identification.md |
| `ecc` | general/crypto | general/techniques/crypto/01-algorithm-identification.md<br>general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `ecdsa nonce` | general/prng | general/techniques/crypto/03-prng-randomness-cracking.md |
| `ecdsa nonce reuse` | general | general/techniques/crypto/03-prng-randomness-cracking.md |
| `ed25519` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `edr bypass` | pe-reverse/av-evasion | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `efficiency` | general/methodology | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `ejs` | ctf-website/prototype-pollution | ctf-website/techniques/03-injection/prototype-pollution.md |
| `elasticsearch` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `elasticsearch groovy 脚本` | ctf-website | ctf-website/techniques/24-database/03-nosql-injection.md |
| `electron` | ctf-website/mobile-bridge | ctf-website/techniques/21-mobile-bridge/01-webview-attacks.md<br>ctf-website/techniques/21-mobile-bridge/02-cordova-reactnative.md |
| `elf` | apk-reverse/native | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md<br>apk-reverse/techniques/02-native/02-pointer-chain-patterns.md<br>apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `elliptic curve` | general/crypto | general/techniques/crypto/01-algorithm-identification.md<br>general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `eloquent` | ctf-website/payment-php | ctf-website/techniques/12-payment/payment-php.md |
| `email bounce` | ctf-website/payment-bounce-idor | ctf-website/techniques/12-payment/payment-email-bounce-idor.md |
| `email injection` | ctf-website/hpp-crlf | ctf-website/techniques/03-injection/hpp-crlf.md |
| `email spoofing` | ctf-website/dns-email | ctf-website/techniques/19-dns-email/01-subdomain-takeover.md<br>ctf-website/techniques/19-dns-email/02-email-spoofing.md |
| `embedded payload` | apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `encrypt` | apk-reverse/crypto, general/crypto | apk-reverse/techniques/04-crypto/01-game-encryption-patterns.md<br>apk-reverse/techniques/04-crypto/02-rc4-custom-crypto.md<br>general/techniques/crypto/01-algorithm-identification.md |
| `encryption analysis` | general | general/techniques/methodology/02-toolchain-decision-tree.md |
| `entropy` | general/crypto | general/techniques/crypto/01-algorithm-identification.md<br>general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `entropy analysis` | general | general/techniques/crypto/01-algorithm-identification.md |
| `entropy delimit` | general | general/techniques/protocol/01-unknown-protocol-reverse.md |
| `entry point` | apk-reverse/manifest, ctf-website/attack-network | apk-reverse/techniques/03-manifest/01-entry-point-tracing.md<br>ctf-website/techniques/attack-network.md |
| `entry point analysis` | general | general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `entrypoint 前执行` | pe-reverse | pe-reverse/techniques/02-pe-structure/02-tls-callback-analysis.md |
| `enumeration` | ctf-website/idor | ctf-website/techniques/14-idor/01-idor-enumeration.md<br>ctf-website/techniques/14-idor/02-bac-business-logic.md |
| `epss` | ctf-website/cve | ctf-website/techniques/09-cve/cve-correlation-graph.md<br>ctf-website/techniques/09-cve/cve-workflow.md<br>ctf-website/techniques/09-cve/multi-cve-chain-playbook.md |
| `erb` | ctf-website/ssti | ctf-website/techniques/03-injection/ssti.md |
| `error-based` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `error_bad_exe_format` | pe-reverse | pe-reverse/techniques/10-license-keygen/08-cross-version-aob-migration.md |
| `esp` | general/cheating | general/techniques/cheating/01-memory-hacking.md<br>general/techniques/cheating/02-packet-interception.md<br>general/techniques/cheating/03-esp-wallhack-rendering.md |
| `etcd` | ctf-website/kubernetes | ctf-website/techniques/10-cloud/container-runtime-escape.md<br>ctf-website/techniques/10-cloud/k8s-rbac-attack-paths.md<br>ctf-website/techniques/10-cloud/kubernetes-container.md |
| `etw patching` | general | general/techniques/cheating/04-anti-cheat-bypass.md |
| `event loop block` | ctf-website/redos-timing | ctf-website/techniques/03-injection/redos-timing.md |
| `event loop 延迟 >1s` | ctf-website | ctf-website/techniques/22-dos/04-redos.md |
| `event.source` | ctf-website/postmessage | ctf-website/techniques/07-client/postmessage.md |
| `exandroidnativeemu` | general | general/methodology/01-headless-emulation-windows-android-handbook.md |
| `exfiltration` | ctf-website/xss | ctf-website/techniques/07-client/admin-bot-xss.md |
| `expired sign` | ctf-website/signature-replay | ctf-website/techniques/13-signature/06-replay-nonce.md |
| `exploit` | ctf-website/cve | ctf-website/techniques/09-cve/cve-correlation-graph.md<br>ctf-website/techniques/09-cve/cve-workflow.md<br>ctf-website/techniques/09-cve/multi-cve-chain-playbook.md |
| `export` | pe-reverse/pe-structure | pe-reverse/techniques/02-pe-structure/01-pe-header-parsing.md |
| `export address table` | pe-reverse | pe-reverse/techniques/03-static-analysis/05-dynamic-api-resolution.md |
| `export directory` | pe-reverse | pe-reverse/techniques/02-pe-structure/01-pe-header-parsing.md |
| `exported` | apk-reverse/manifest | apk-reverse/techniques/03-manifest/01-entry-point-tracing.md |
| `external memory` | pe-reverse/dynamic-analysis | pe-reverse/techniques/04-dynamic-analysis/01-dll-injection.md<br>pe-reverse/techniques/04-dynamic-analysis/02-trampoline-detour.md<br>pe-reverse/techniques/04-dynamic-analysis/03-external-memory-rw.md |
| `external trainer` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/03-external-memory-rw.md |
| `extract` | ctf-website/payment-php | ctf-website/techniques/12-payment/payment-php.md |
| `extract bypass` | ctf-website/signature-implementation | ctf-website/techniques/13-signature/02-implementation.md |
| `extractable` | ctf-website/web-crypto | ctf-website/techniques/07-client/web-crypto-abuse.md |
| `extractvalue updatexml 报错` | ctf-website | ctf-website/techniques/24-database/01-sqli-fundamentals.md |
| `eyj` | ctf-website/jwt | ctf-website/techniques/02-auth/jwt/00-overview.md<br>ctf-website/techniques/02-auth/jwt/01-alg-none.md<br>ctf-website/techniques/02-auth/jwt/02-algorithm-confusion.md |
| `failed to deserialize form` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/04-twinbasic-compressed-resource-recovery.md |
| `fallbacktofrontend` | ctf-website/nezha-path-traversal | ctf-website/techniques/09-cve/04-nezha-path-traversal-jwt.md |
| `fart` | apk-reverse, apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `fart dump` | apk-reverse | apk-reverse/techniques/07-packer/02-modern-art-dex-dump-and-repair.md |
| `fastly` | ctf-website/cloudflare-bypass | ctf-website/techniques/01-recon/cloudflare-bypass.md |
| `fat get` | ctf-website/cache-deception | ctf-website/techniques/08-infra/web-cache-deception.md |
| `fd theft` | general | general/techniques/01-kernel/03-mm-null-ptrace-bypass.md |
| `feistel` | general/crypto | general/techniques/crypto/01-algorithm-identification.md<br>general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `feistel detection` | general | general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `fetch api` | ctf-website/js-runtime | ctf-website/techniques/07-client/js-runtime.md |
| `field classification` | general | general/techniques/protocol/01-unknown-protocol-reverse.md |
| `field inference` | general/protocol | general/techniques/protocol/01-unknown-protocol-reverse.md<br>general/techniques/protocol/02-protobuf-flatbuffers-reverse.md |
| `field number` | ctf-website/grpc | ctf-website/techniques/03-injection/grpc-protobuf.md |
| `field offset` | pe-reverse | pe-reverse/techniques/03-static-analysis/01-struct-reconstruction.md |
| `field type inference` | general, pe-reverse | general/techniques/protocol/02-protobuf-flatbuffers-reverse.md<br>pe-reverse/techniques/03-static-analysis/04-reclass-reconstruction.md |
| `file descriptor stealing` | general | general/techniques/01-kernel/03-mm-null-ptrace-bypass.md |
| `file monitoring` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/08-procmon-patterns.md |
| `file path` | pe-reverse/ioc | pe-reverse/techniques/06-ioc-extraction/01-ioc-extraction.md |
| `file read` | ctf-website/file-attacks | ctf-website/techniques/06-file-attacks/file-upload-xxe-lfi.md |
| `file type routing` | general | general/techniques/methodology/02-toolchain-decision-tree.md |
| `file upload` | ctf-website/file-attacks | ctf-website/techniques/06-file-attacks/file-upload-xxe-lfi.md |
| `file:///dev/random 阻塞` | ctf-website | ctf-website/techniques/22-dos/12-ssrf-dos.md |
| `filter rules` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/08-procmon-patterns.md |
| `finddmaaddy` | pe-reverse/dynamic-analysis | pe-reverse/techniques/04-dynamic-analysis/01-dll-injection.md<br>pe-reverse/techniques/04-dynamic-analysis/02-trampoline-detour.md<br>pe-reverse/techniques/04-dynamic-analysis/03-external-memory-rw.md |
| `findkeyjson 递归搜索` | ctf-website | ctf-website/techniques/23-paywall-bypass/04-content-extraction.md |
| `findpattern` | pe-reverse/triage | pe-reverse/techniques/01-triage/01-aob-signature-scan.md |
| `fingerprint` | ctf-website/recon | ctf-website/techniques/01-recon/recon-routing.md<br>ctf-website/techniques/01-recon/version-fingerprinting.md |
| `firebase config` | ctf-website/api-attacks | ctf-website/techniques/17-api-attacks/01-api-discovery-leak.md<br>ctf-website/techniques/17-api-attacks/02-api-key-leak.md |
| `first 30 min` | general/methodology | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `flatbuffers` | general/protocol | general/techniques/protocol/01-unknown-protocol-reverse.md<br>general/techniques/protocol/02-protobuf-flatbuffers-reverse.md |
| `flatbuffers offset` | general | general/techniques/protocol/02-protobuf-flatbuffers-reverse.md |
| `fleet` | ctf-website/24h-loop-orchestration | ctf-website/techniques/00-workflow/24h-loop-orchestration.md<br>ctf-website/techniques/attack-network.md |
| `fleet orchestration` | ctf-website | ctf-website/techniques/00-workflow/24h-loop-orchestration.md |
| `float precision` | ctf-website/payment-bypass | ctf-website/techniques/12-payment/payment-bypass.md |
| `flushall debug sleep` | ctf-website | ctf-website/techniques/22-dos/12-ssrf-dos.md |
| `flutter` | ctf-website/mobile-bridge | ctf-website/techniques/21-mobile-bridge/01-webview-attacks.md<br>ctf-website/techniques/21-mobile-bridge/02-cordova-reactnative.md |
| `flutter app` | apk-reverse | apk-reverse/techniques/02-native/08-flutter-dart-aot-reconstruction.md |
| `flutter engine id` | apk-reverse | apk-reverse/techniques/02-native/08-flutter-dart-aot-reconstruction.md |
| `fofa` | ctf-website/fofa | ctf-website/techniques/01-recon/fofa-hunting.md |
| `fofa query` | ctf-website/fofa | ctf-website/techniques/01-recon/fofa-hunting.md |
| `fofa.so` | ctf-website/fofa | ctf-website/techniques/01-recon/fofa-hunting.md |
| `fofa语法` | ctf-website/fofa | ctf-website/techniques/01-recon/fofa-hunting.md |
| `foll_pin` | general | general/techniques/01-kernel/05-pintheft-io-uring-page-cache.md |
| `fragment` | ctf-website/graphql | ctf-website/techniques/03-injection/graphql.md |
| `fragnesia` | ctf-website/page-cache-write | general/techniques/01-kernel/01-page-cache-write-family.md |
| `frame counting` | ctf-website/csp-cors-advanced | ctf-website/techniques/18-cors-csp-advanced/01-csp-bypass.md<br>ctf-website/techniques/18-cors-csp-advanced/02-xs-leaks-browser-sidechannels.md |
| `freemarker` | ctf-website/ssti | ctf-website/techniques/03-injection/ssti.md |
| `frida` | apk-reverse/dynamic-frida | apk-reverse/techniques/06-dynamic/01-memory-rw-hook.md<br>apk-reverse/techniques/06-dynamic/02-overlay-rendering-hook.md<br>apk-reverse/techniques/06-dynamic/03-touch-input-hook.md |
| `frida bypass` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/05-anti-debug-bypass.md |
| `frida crypto hooking` | general | general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `frida dump` | pe-reverse | pe-reverse/techniques/03-static-analysis/01-struct-reconstruction.md |
| `frida 检测` | apk-reverse | apk-reverse/techniques/07-packer/05-vmp-anti-debug-bypass.md |
| `frida 调用栈` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `frida 验证` | pe-reverse | pe-reverse/techniques/10-license-keygen/05-keygen-frida-verification-loop.md |
| `frida-dexdump` | apk-reverse | apk-reverse/techniques/07-packer/02-modern-art-dex-dump-and-repair.md<br>apk-reverse/techniques/07-packer/04-vmp-dump-trace-recovery.md |
| `function url` | ctf-website/cloud-serverless | ctf-website/techniques/10-cloud/aws-iam-privesc.md<br>ctf-website/techniques/10-cloud/serverless-lambda.md |
| `gadget` | ctf-website/deserialization | ctf-website/techniques/05-deserialization/deserialization.md |
| `game hack` | general/cheating | general/techniques/cheating/01-memory-hacking.md<br>general/techniques/cheating/02-packet-interception.md<br>general/techniques/cheating/03-esp-wallhack-rendering.md |
| `gateway` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/02-trampoline-detour.md<br>pe-reverse/techniques/04-dynamic-analysis/04-naked-function-hook.md |
| `gbk` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `gcp key` | ctf-website/api-attacks | ctf-website/techniques/17-api-attacks/01-api-discovery-leak.md<br>ctf-website/techniques/17-api-attacks/02-api-key-leak.md |
| `geetest` | ctf-website/captcha-bypass | ctf-website/techniques/01-recon/captcha-bypass.md |
| `getdlgitemtext` | pe-reverse | pe-reverse/techniques/10-license-keygen/02-validation-function-location.md |
| `getmodulehandle` | pe-reverse/triage | pe-reverse/techniques/01-triage/01-aob-signature-scan.md |
| `getpackageinfo` | apk-reverse | apk-reverse/techniques/08-patch-repack/02-signature-integrity-bypass.md |
| `getprocaddress` | pe-reverse | pe-reverse/techniques/03-static-analysis/05-dynamic-api-resolution.md |
| `gettickcount hook` | general | general/techniques/cheating/05-speedhack-time-manipulation.md |
| `gettime` | general/cheating | general/techniques/cheating/01-memory-hacking.md<br>general/techniques/cheating/02-packet-interception.md<br>general/techniques/cheating/03-esp-wallhack-rendering.md |
| `getwindowtext` | pe-reverse | pe-reverse/techniques/10-license-keygen/02-validation-function-location.md |
| `getzz` | apk-reverse/native | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md<br>apk-reverse/techniques/02-native/02-pointer-chain-patterns.md<br>apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `ghost paywall` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `gift card` | ctf-website/payment-digital-goods | ctf-website/techniques/12-payment/payment-digital-goods.md |
| `github actions` | ctf-website/ci-cd | ctf-website/techniques/10-cloud/ci-cd-pipeline.md<br>ctf-website/techniques/10-cloud/github-actions-abuse-paths.md<br>ctf-website/techniques/10-cloud/terraform-state-secrets.md |
| `github dorking` | ctf-website/api-attacks | ctf-website/techniques/17-api-attacks/01-api-discovery-leak.md<br>ctf-website/techniques/17-api-attacks/02-api-key-leak.md |
| `github_token` | ctf-website/ci-cd | ctf-website/techniques/10-cloud/ci-cd-pipeline.md<br>ctf-website/techniques/10-cloud/github-actions-abuse-paths.md<br>ctf-website/techniques/10-cloud/terraform-state-secrets.md |
| `gitlab ci` | ctf-website/ci-cd | ctf-website/techniques/10-cloud/ci-cd-pipeline.md<br>ctf-website/techniques/10-cloud/github-actions-abuse-paths.md<br>ctf-website/techniques/10-cloud/terraform-state-secrets.md |
| `glyph signature` | pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `go binary` | pe-reverse | pe-reverse/techniques/03-static-analysis/06-go-rust-binary-reconstruction.md |
| `go.buildid` | pe-reverse | pe-reverse/techniques/03-static-analysis/06-go-rust-binary-reconstruction.md |
| `google play` | ctf-website/payment-digital-goods | ctf-website/techniques/12-payment/payment-digital-goods.md |
| `google web cache 完整内容` | ctf-website | ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md |
| `google webcache` | ctf-website | ctf-website/techniques/23-paywall-bypass/04-content-extraction.md |
| `googlebot` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `googlebot ua 差异化` | ctf-website | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md |
| `gopher` | ctf-website/ssrf | ctf-website/techniques/04-ssrf/ssrf.md |
| `gopher 协议 redis 命令` | ctf-website | ctf-website/techniques/22-dos/12-ssrf-dos.md |
| `graphiql` | ctf-website/graphql | ctf-website/techniques/03-injection/graphql.md |
| `graphql` | ctf-website/graphql | ctf-website/techniques/03-injection/graphql.md |
| `graphql amplification` | ctf-website/dos | ctf-website/techniques/22-dos/01-application-layer-dos.md<br>ctf-website/techniques/22-dos/02-resource-exhaustion.md<br>ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `graphql idor` | ctf-website/idor | ctf-website/techniques/14-idor/01-idor-enumeration.md<br>ctf-website/techniques/14-idor/02-bac-business-logic.md |
| `graphql introspection` | ctf-website/api-attacks | ctf-website/techniques/17-api-attacks/01-api-discovery-leak.md<br>ctf-website/techniques/17-api-attacks/02-api-key-leak.md |
| `graphql 别名轰炸` | ctf-website | ctf-website/techniques/22-dos/01-application-layer-dos.md |
| `groovy` | ctf-website/ci-cd | ctf-website/techniques/10-cloud/ci-cd-pipeline.md<br>ctf-website/techniques/10-cloud/github-actions-abuse-paths.md<br>ctf-website/techniques/10-cloud/terraform-state-secrets.md |
| `grpc` | ctf-website/grpc, general/protocol | ctf-website/techniques/03-injection/grpc-protobuf.md<br>general/techniques/protocol/01-unknown-protocol-reverse.md<br>general/techniques/protocol/02-protobuf-flatbuffers-reverse.md |
| `grpc reflection` | general | general/techniques/protocol/02-protobuf-flatbuffers-reverse.md |
| `grpc-web` | ctf-website/grpc | ctf-website/techniques/03-injection/grpc-protobuf.md |
| `guest order leak` | ctf-website/payment-bounce-idor | ctf-website/techniques/12-payment/payment-email-bounce-idor.md |
| `gzip` | apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `h2` | ctf-website/grpc, ctf-website/http2 | ctf-website/techniques/03-injection/grpc-protobuf.md<br>ctf-website/techniques/08-infra/http2-attacks.md |
| `h2 rapid reset` | ctf-website/dos | ctf-website/techniques/22-dos/01-application-layer-dos.md<br>ctf-website/techniques/22-dos/02-resource-exhaustion.md<br>ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `h2c` | ctf-website/http2 | ctf-website/techniques/08-infra/http2-attacks.md |
| `handle stripping` | general | general/techniques/cheating/04-anti-cheat-bypass.md |
| `handler` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `handler 表` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `handler 调度` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/07-modern-virtual-machine-devirtualization-mogvmp-llvm.md |
| `hard paywall` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `hardcoded key` | ctf-website/signature-key | ctf-website/techniques/13-signature/03-key-attacks.md |
| `hardware breakpoint` | pe-reverse | pe-reverse/techniques/03-static-analysis/03-x64dbg-breakpoints.md |
| `hash` | apk-reverse/crypto, ctf-website/signature, general/crypto | apk-reverse/techniques/04-crypto/01-game-encryption-patterns.md<br>apk-reverse/techniques/04-crypto/02-rc4-custom-crypto.md<br>ctf-website/techniques/13-signature/00-overview.md |
| `hash extender` | ctf-website/signature-length-extension | ctf-website/techniques/13-signature/05-length-extension.md |
| `hash iv constants` | general | general/techniques/crypto/01-algorithm-identification.md |
| `hash length attack` | ctf-website/signature-length-extension | ctf-website/techniques/13-signature/05-length-extension.md |
| `hash length extension` | ctf-website/signature-length-extension | ctf-website/techniques/13-signature/05-length-extension.md |
| `hash 碰撞 cpu 100%` | ctf-website | ctf-website/techniques/22-dos/02-resource-exhaustion.md |
| `hashdos` | ctf-website/dos | ctf-website/techniques/22-dos/01-application-layer-dos.md<br>ctf-website/techniques/22-dos/02-resource-exhaustion.md<br>ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `hashdos cve-2011-4885` | ctf-website | ctf-website/techniques/22-dos/02-resource-exhaustion.md |
| `hashmap rehash` | ctf-website/chrome-uaf-blink | ctf-website/techniques/09-cve/01-browser-sandbox-escape.md |
| `hashpumpy` | ctf-website/signature-length-extension | ctf-website/techniques/13-signature/05-length-extension.md |
| `hcaptcha` | ctf-website/captcha-bypass | ctf-website/techniques/01-recon/captcha-bypass.md |
| `header fuzzing` | ctf-website/recon | ctf-website/techniques/01-recon/recon-routing.md<br>ctf-website/techniques/01-recon/version-fingerprinting.md |
| `header injection` | ctf-website/hpp-crlf | ctf-website/techniques/03-injection/hpp-crlf.md |
| `headless` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `headless emulation` | general | general/methodology/01-headless-emulation-windows-android-handbook.md |
| `heap buffer overflow` | ctf-website/redis-valkey-restore-zipmap | ctf-website/techniques/09-cve/02-redis-zipmap-rce.md |
| `heap overflow` | ctf-website/nginx-rewrite-heapoverflow | ctf-website/techniques/09-cve/06-nginx-rewrite-heapoverflow.md |
| `hell's gate` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/07-direct-syscall.md |
| `hessian` | ctf-website/deserialization | ctf-website/techniques/05-deserialization/deserialization.md |
| `hex` | pe-reverse/yara-sigma | pe-reverse/techniques/07-yara-sigma/01-yara-rule-writing.md |
| `hex dump` | pe-reverse | pe-reverse/techniques/03-static-analysis/04-reclass-reconstruction.md |
| `hex-rays microcode` | pe-reverse | pe-reverse/techniques/03-static-analysis/07-ida-microcode-mba-deobfuscation-d810.md |
| `high entropy not encrypted` | pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `hmac` | apk-reverse/crypto, ctf-website/jwt, ctf-website/signature | apk-reverse/techniques/04-crypto/01-game-encryption-patterns.md<br>apk-reverse/techniques/04-crypto/02-rc4-custom-crypto.md<br>ctf-website/techniques/02-auth/jwt/00-overview.md |
| `hmac key` | ctf-website/signature-key | ctf-website/techniques/13-signature/03-key-attacks.md |
| `hook` | apk-reverse/dynamic-frida, ctf-website/js-runtime, pe-reverse/dynamic-analysis | apk-reverse/techniques/06-dynamic/01-memory-rw-hook.md<br>apk-reverse/techniques/06-dynamic/02-overlay-rendering-hook.md<br>apk-reverse/techniques/06-dynamic/03-touch-input-hook.md |
| `hook boundary` | pe-reverse | pe-reverse/techniques/03-static-analysis/02-disasm-jit-asm.md |
| `hook 查询面` | pe-reverse | pe-reverse/techniques/10-license-keygen/06-cloud-license-frida-hook.md |
| `horizontal privilege` | ctf-website/idor | ctf-website/techniques/14-idor/01-idor-enumeration.md<br>ctf-website/techniques/14-idor/02-bac-business-logic.md |
| `host header` | ctf-website/host-header | ctf-website/techniques/02-auth/host-header.md |
| `host injection` | ctf-website/host-header | ctf-website/techniques/02-auth/host-header.md |
| `host override` | ctf-website/host-header | ctf-website/techniques/02-auth/host-header.md |
| `hostpath` | ctf-website/kubernetes | ctf-website/techniques/10-cloud/container-runtime-escape.md<br>ctf-website/techniques/10-cloud/k8s-rbac-attack-paths.md<br>ctf-website/techniques/10-cloud/kubernetes-container.md |
| `hotkey toggle` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/04-naked-function-hook.md |
| `hpa 扩容至 maxreplicas` | ctf-website | ctf-website/techniques/22-dos/11-cloud-container-dos.md |
| `hpack` | ctf-website/http2 | ctf-website/techniques/08-infra/http2-attacks.md |
| `hpack 动态表引用` | ctf-website | ctf-website/techniques/22-dos/05-http2-continuation.md |
| `hpp` | ctf-website/hpp-crlf, ctf-website/signature-canonicalization | ctf-website/techniques/03-injection/hpp-crlf.md<br>ctf-website/techniques/13-signature/04-canonicalization.md |
| `hpp http 参数污染` | ctf-website | ctf-website/techniques/24-database/02-sqli-advanced.md |
| `html 堆叠 多段 body` | ctf-website | ctf-website/techniques/24-database/07-data-cleaning.md |
| `http` | apk-reverse/network | apk-reverse/techniques/05-network/01-game-protocol-hook.md<br>apk-reverse/techniques/05-network/02-license-verification-bypass.md |
| `http 406 not acceptable` | general | general/methodology/02-remote-mcp-device-bridge-deployment.md |
| `http header 逐字节发送` | ctf-website | ctf-website/techniques/22-dos/01-application-layer-dos.md |
| `http/2` | ctf-website/http2 | ctf-website/techniques/08-infra/http2-attacks.md |
| `http/2 rst_stream 帧` | ctf-website | ctf-website/techniques/22-dos/01-application-layer-dos.md |
| `http/2 连接内存 oom` | ctf-website | ctf-website/techniques/22-dos/05-http2-continuation.md |
| `http/3 0-rtt 重放` | ctf-website | ctf-website/techniques/22-dos/05-http2-continuation.md |
| `http2` | ctf-website/http2 | ctf-website/techniques/08-infra/http2-attacks.md |
| `https` | apk-reverse/network | apk-reverse/techniques/05-network/01-game-protocol-hook.md<br>apk-reverse/techniques/05-network/02-license-verification-bypass.md |
| `hub approval` | general | general/methodology/02-remote-mcp-device-bridge-deployment.md |
| `hunter` | ctf-website/fofa | ctf-website/techniques/01-recon/fofa-hunting.md |
| `hxd` | pe-reverse/patch | pe-reverse/techniques/08-patch/01-code-patching.md |
| `iac` | ctf-website/ci-cd | ctf-website/techniques/10-cloud/ci-cd-pipeline.md<br>ctf-website/techniques/10-cloud/github-actions-abuse-paths.md<br>ctf-website/techniques/10-cloud/terraform-state-secrets.md |
| `iam role` | ctf-website/cloud-serverless | ctf-website/techniques/10-cloud/aws-iam-privesc.md<br>ctf-website/techniques/10-cloud/serverless-lambda.md |
| `iap` | ctf-website/payment-digital-goods | ctf-website/techniques/12-payment/payment-digital-goods.md |
| `iat` | pe-reverse/pe-structure | pe-reverse/techniques/02-pe-structure/01-pe-header-parsing.md |
| `iat filling` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/06-manual-map-injection.md |
| `iat rebuild` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `id increment` | ctf-website/idor | ctf-website/techniques/14-idor/01-idor-enumeration.md<br>ctf-website/techniques/14-idor/02-bac-business-logic.md |
| `id token` | ctf-website/oauth | ctf-website/techniques/02-auth/oauth-sso.md |
| `idat` | pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `idempotency` | ctf-website/payment-callback | ctf-website/techniques/12-payment/payment-callback-async.md |
| `identity provider` | ctf-website/saml | ctf-website/techniques/02-auth/saml-attacks.md |
| `idle in transaction 连接` | ctf-website | ctf-website/techniques/22-dos/13-database-dos.md |
| `idor` | ctf-website/database-attacks, ctf-website/idor, ctf-website/payment-bounce-idor | ctf-website/techniques/12-payment/payment-email-bounce-idor.md<br>ctf-website/techniques/14-idor/01-idor-enumeration.md<br>ctf-website/techniques/14-idor/02-bac-business-logic.md |
| `idp` | ctf-website/saml | ctf-website/techniques/02-auth/saml-attacks.md |
| `il2cpp` | apk-reverse/native | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md<br>apk-reverse/techniques/02-native/02-pointer-chain-patterns.md<br>apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `image file execution options` | pe-reverse | pe-reverse/techniques/06-ioc-extraction/02-persistence-startup-chain.md |
| `image_dos_header` | pe-reverse | pe-reverse/techniques/02-pe-structure/01-pe-header-parsing.md |
| `image_nt_headers` | pe-reverse | pe-reverse/techniques/02-pe-structure/01-pe-header-parsing.md |
| `imds` | ctf-website/ssrf | ctf-website/techniques/04-ssrf/ssrf.md |
| `imds 169.254.169.254` | ctf-website | ctf-website/techniques/22-dos/11-cloud-container-dos.md |
| `imgui` | apk-reverse/dynamic-frida, general/cheating | apk-reverse/techniques/06-dynamic/01-memory-rw-hook.md<br>apk-reverse/techniques/06-dynamic/02-overlay-rendering-hook.md<br>apk-reverse/techniques/06-dynamic/03-touch-input-hook.md |
| `imgui esp` | general | general/techniques/cheating/03-esp-wallhack-rendering.md |
| `immediate value` | pe-reverse | pe-reverse/techniques/08-patch/01-code-patching.md |
| `imperva` | ctf-website/cloudflare-bypass | ctf-website/techniques/01-recon/cloudflare-bypass.md |
| `implementation` | apk-reverse/dynamic-frida | apk-reverse/techniques/06-dynamic/01-memory-rw-hook.md<br>apk-reverse/techniques/06-dynamic/02-overlay-rendering-hook.md<br>apk-reverse/techniques/06-dynamic/03-touch-input-hook.md |
| `implicit flow` | ctf-website/oauth, ctf-website/oauth-deep | ctf-website/techniques/02-auth/oauth-sso.md<br>ctf-website/techniques/20-oauth-deep/01-oauth-attack-chains.md<br>ctf-website/techniques/20-oauth-deep/02-session-fixation-attacks.md |
| `import` | pe-reverse/pe-structure | pe-reverse/techniques/02-pe-structure/01-pe-header-parsing.md |
| `import analysis` | general | general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `import directory` | pe-reverse | pe-reverse/techniques/02-pe-structure/01-pe-header-parsing.md |
| `import table` | pe-reverse | pe-reverse/techniques/07-yara-sigma/01-yara-rule-writing.md |
| `import table empty` | pe-reverse | pe-reverse/techniques/03-static-analysis/05-dynamic-api-resolution.md |
| `in-app purchase` | ctf-website/payment-digital-goods | ctf-website/techniques/12-payment/payment-digital-goods.md |
| `in-place decrypt` | general | general/techniques/01-kernel/01-page-cache-write-family.md |
| `include` | ctf-website/file-attacks | ctf-website/techniques/06-file-attacks/file-upload-xxe-lfi.md |
| `inflate` | pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `information_schema tables` | ctf-website | ctf-website/techniques/24-database/01-sqli-fundamentals.md |
| `inject` | apk-reverse/patch-repack | apk-reverse/techniques/08-patch-repack/01-so-injection-repack.md |
| `injectimmediately document_start` | ctf-website | ctf-website/techniques/23-paywall-bypass/05-dom-css-manipulation.md |
| `inline asm` | pe-reverse/dynamic-analysis | pe-reverse/techniques/04-dynamic-analysis/01-dll-injection.md<br>pe-reverse/techniques/04-dynamic-analysis/02-trampoline-detour.md<br>pe-reverse/techniques/04-dynamic-analysis/03-external-memory-rw.md |
| `inline assembly` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/04-naked-function-hook.md |
| `inline hook` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/02-trampoline-detour.md |
| `input` | apk-reverse/dynamic-frida | apk-reverse/techniques/06-dynamic/01-memory-rw-hook.md<br>apk-reverse/techniques/06-dynamic/02-overlay-rendering-hook.md<br>apk-reverse/techniques/06-dynamic/03-touch-input-hook.md |
| `insecure direct object reference` | ctf-website/idor, ctf-website/payment-bounce-idor | ctf-website/techniques/12-payment/payment-email-bounce-idor.md<br>ctf-website/techniques/14-idor/01-idor-enumeration.md<br>ctf-website/techniques/14-idor/02-bac-business-logic.md |
| `insert update delete 注入` | ctf-website | ctf-website/techniques/24-database/02-sqli-advanced.md |
| `install.lock` | ctf-website | ctf-website/techniques/24-database/05-backup-log-leak.md |
| `install/install.sql` | ctf-website | ctf-website/techniques/24-database/05-backup-log-leak.md |
| `installer package` | apk-reverse | apk-reverse/techniques/08-patch-repack/02-signature-integrity-bypass.md |
| `instruction decoding` | pe-reverse | pe-reverse/techniques/03-static-analysis/02-disasm-jit-asm.md |
| `int 3` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `int 3 旁路` | general | general/methodology/01-headless-emulation-windows-android-handbook.md |
| `integrity` | apk-reverse/patch-repack | apk-reverse/techniques/08-patch-repack/01-so-injection-repack.md |
| `intent` | apk-reverse/manifest | apk-reverse/techniques/03-manifest/01-entry-point-tracing.md |
| `intent hijacking` | ctf-website/mobile-bridge | ctf-website/techniques/21-mobile-bridge/01-webview-attacks.md<br>ctf-website/techniques/21-mobile-bridge/02-cordova-reactnative.md |
| `intercept` | apk-reverse/dynamic-frida | apk-reverse/techniques/06-dynamic/01-memory-rw-hook.md<br>apk-reverse/techniques/06-dynamic/02-overlay-rendering-hook.md<br>apk-reverse/techniques/06-dynamic/03-touch-input-hook.md |
| `internal network` | ctf-website/ssrf | ctf-website/techniques/04-ssrf/ssrf.md |
| `internal_user` | ctf-website/litellm-privesc | ctf-website/techniques/09-cve/05-litellm-privesc.md |
| `introspection` | ctf-website/graphql | ctf-website/techniques/03-injection/graphql.md |
| `invalid key` | pe-reverse | pe-reverse/techniques/10-license-keygen/02-validation-function-location.md |
| `invoice` | ctf-website/payment | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/12-payment/payment-digital-goods.md |
| `io_uring` | general | general/techniques/01-kernel/05-pintheft-io-uring-page-cache.md |
| `ioc extraction` | pe-reverse | pe-reverse/techniques/06-ioc-extraction/01-ioc-extraction.md |
| `ioc 提取` | pe-reverse | pe-reverse/techniques/06-ioc-extraction/01-ioc-extraction.md |
| `ioctl` | apk-reverse/dynamic-frida | apk-reverse/techniques/06-dynamic/01-memory-rw-hook.md<br>apk-reverse/techniques/06-dynamic/02-overlay-rendering-hook.md<br>apk-reverse/techniques/06-dynamic/03-touch-input-hook.md |
| `ip` | pe-reverse/ioc | pe-reverse/techniques/06-ioc-extraction/01-ioc-extraction.md |
| `ip rotation` | ctf-website/rate-limit | ctf-website/techniques/16-rate-limit/01-rate-limit-bypass.md<br>ctf-website/techniques/16-rate-limit/02-brute-force-tactics.md |
| `ip spoofing` | ctf-website/dos | ctf-website/techniques/22-dos/01-application-layer-dos.md<br>ctf-website/techniques/22-dos/02-resource-exhaustion.md<br>ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `ip spoofing 原始套接字` | ctf-website | ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `irsa` | ctf-website/cloud-serverless | ctf-website/techniques/10-cloud/aws-iam-privesc.md<br>ctf-website/techniques/10-cloud/serverless-lambda.md |
| `isdebuggerpresent` | pe-reverse/dynamic-analysis | pe-reverse/techniques/04-dynamic-analysis/01-dll-injection.md<br>pe-reverse/techniques/04-dynamic-analysis/02-trampoline-detour.md<br>pe-reverse/techniques/04-dynamic-analysis/03-external-memory-rw.md |
| `iv` | apk-reverse/crypto | apk-reverse/techniques/04-crypto/01-game-encryption-patterns.md<br>apk-reverse/techniques/04-crypto/02-rc4-custom-crypto.md |
| `jackson polymorphic` | ctf-website/deserialization | ctf-website/techniques/05-deserialization/deserialization.md |
| `jadx` | apk-reverse/dex-java | apk-reverse/techniques/01-dex-java/01-smali-injection.md |
| `jadx cant open dex` | apk-reverse | apk-reverse/techniques/07-packer/02-modern-art-dex-dump-and-repair.md |
| `java` | apk-reverse/dex-java | apk-reverse/techniques/01-dex-java/01-smali-injection.md |
| `java random` | general/prng | general/techniques/crypto/03-prng-randomness-cracking.md |
| `java random cracking` | general | general/techniques/crypto/03-prng-randomness-cracking.md |
| `java.perform` | apk-reverse/dynamic-frida | apk-reverse/techniques/06-dynamic/01-memory-rw-hook.md<br>apk-reverse/techniques/06-dynamic/02-overlay-rendering-hook.md<br>apk-reverse/techniques/06-dynamic/03-touch-input-hook.md |
| `java_com_` | apk-reverse, apk-reverse/native | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md<br>apk-reverse/techniques/02-native/02-pointer-chain-patterns.md<br>apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `javascript` | ctf-website/js-runtime | ctf-website/techniques/07-client/js-runtime.md |
| `javascript bridge` | ctf-website/mobile-bridge | ctf-website/techniques/21-mobile-bridge/01-webview-attacks.md<br>ctf-website/techniques/21-mobile-bridge/02-cordova-reactnative.md |
| `javascript-obfuscator` | ctf-website | ctf-website/techniques/27-js-reverse/01-ast-deobfuscation-pipeline.md |
| `javax.crypto` | apk-reverse/crypto | apk-reverse/techniques/04-crypto/01-game-encryption-patterns.md<br>apk-reverse/techniques/04-crypto/02-rc4-custom-crypto.md |
| `jenkins` | ctf-website/ci-cd | ctf-website/techniques/10-cloud/ci-cd-pipeline.md<br>ctf-website/techniques/10-cloud/github-actions-abuse-paths.md<br>ctf-website/techniques/10-cloud/terraform-state-secrets.md |
| `jinja2` | ctf-website/ssti | ctf-website/techniques/03-injection/ssti.md |
| `jit` | pe-reverse/static-analysis | pe-reverse/techniques/03-static-analysis/01-struct-reconstruction.md<br>pe-reverse/techniques/03-static-analysis/02-disasm-jit-asm.md<br>pe-reverse/techniques/03-static-analysis/03-x64dbg-breakpoints.md |
| `jit assembly` | pe-reverse | pe-reverse/techniques/03-static-analysis/02-disasm-jit-asm.md |
| `jmp` | pe-reverse/patch | pe-reverse/techniques/08-patch/01-code-patching.md |
| `jmp [base+idx*scale]` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/09-runtime-vm-detection-generic.md |
| `jmp [r12+rax*8]` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/08-selfhealing-emulation-vmp-handler-extraction.md |
| `jmp hook` | pe-reverse, pe-reverse/dynamic-analysis | pe-reverse/techniques/04-dynamic-analysis/01-dll-injection.md<br>pe-reverse/techniques/04-dynamic-analysis/02-trampoline-detour.md<br>pe-reverse/techniques/04-dynamic-analysis/03-external-memory-rw.md |
| `jmp modification` | pe-reverse | pe-reverse/techniques/08-patch/01-code-patching.md |
| `jmp rdx` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `jmp reg` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `jndi` | ctf-website/ldap | ctf-website/techniques/02-auth/ldap-injection.md |
| `jni` | apk-reverse/native | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md<br>apk-reverse/techniques/02-native/02-pointer-chain-patterns.md<br>apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `jni 打桩` | general | general/methodology/01-headless-emulation-windows-android-handbook.md |
| `jni_onload` | apk-reverse, apk-reverse/native | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md<br>apk-reverse/techniques/02-native/02-pointer-chain-patterns.md<br>apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `jni_onload 崩溃` | apk-reverse | apk-reverse/techniques/02-native/07-unidbg-native-emulation-pipeline.md |
| `jnienv` | apk-reverse | apk-reverse/techniques/02-native/07-unidbg-native-emulation-pipeline.md |
| `js` | ctf-website/js-runtime | ctf-website/techniques/07-client/js-runtime.md |
| `json canonicalization` | ctf-website/signature-canonicalization | ctf-website/techniques/13-signature/04-canonicalization.md |
| `json web token` | ctf-website/jwt | ctf-website/techniques/02-auth/jwt/00-overview.md<br>ctf-website/techniques/02-auth/jwt/01-alg-none.md<br>ctf-website/techniques/02-auth/jwt/02-algorithm-confusion.md |
| `json 响应 泄露数据` | ctf-website | ctf-website/techniques/24-database/07-data-cleaning.md |
| `json 深度嵌套解析器崩溃` | ctf-website | ctf-website/techniques/22-dos/02-resource-exhaustion.md |
| `json-ld articlebody` | ctf-website, ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `jsonp` | ctf-website/csp-cors-advanced | ctf-website/techniques/18-cors-csp-advanced/01-csp-bypass.md<br>ctf-website/techniques/18-cors-csp-advanced/02-xs-leaks-browser-sidechannels.md |
| `junk code` | pe-reverse/av-evasion | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `jwe` | ctf-website/jwt, ctf-website/web-crypto | ctf-website/techniques/02-auth/jwt/00-overview.md<br>ctf-website/techniques/02-auth/jwt/01-alg-none.md<br>ctf-website/techniques/02-auth/jwt/02-algorithm-confusion.md |
| `jws` | ctf-website/jwt | ctf-website/techniques/02-auth/jwt/00-overview.md<br>ctf-website/techniques/02-auth/jwt/01-alg-none.md<br>ctf-website/techniques/02-auth/jwt/02-algorithm-confusion.md |
| `jwt` | ctf-website/jwt | ctf-website/techniques/02-auth/jwt/00-overview.md<br>ctf-website/techniques/02-auth/jwt/01-alg-none.md<br>ctf-website/techniques/02-auth/jwt/02-algorithm-confusion.md |
| `jwt secret` | ctf-website/nezha-path-traversal, ctf-website/signature-key | ctf-website/techniques/09-cve/04-nezha-path-traversal-jwt.md<br>ctf-website/techniques/13-signature/03-key-attacks.md |
| `k8s` | ctf-website/kubernetes | ctf-website/techniques/10-cloud/container-runtime-escape.md<br>ctf-website/techniques/10-cloud/k8s-rbac-attack-paths.md<br>ctf-website/techniques/10-cloud/kubernetes-container.md |
| `kasiski examination` | general | general/techniques/crypto/01-algorithm-identification.md |
| `kernel driver` | apk-reverse/native | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md<br>apk-reverse/techniques/02-native/02-pointer-chain-patterns.md<br>apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `kernel driver r/w` | general | general/techniques/cheating/01-memory-hacking.md |
| `kernel privilege escalation` | general | general/techniques/01-kernel/01-page-cache-write-family.md |
| `kev` | ctf-website/cve | ctf-website/techniques/09-cve/cve-correlation-graph.md<br>ctf-website/techniques/09-cve/cve-workflow.md<br>ctf-website/techniques/09-cve/multi-cve-chain-playbook.md |
| `key` | apk-reverse/crypto | apk-reverse/techniques/04-crypto/01-game-encryption-patterns.md<br>apk-reverse/techniques/04-crypto/02-rc4-custom-crypto.md |
| `key exchange` | general/crypto | general/techniques/crypto/01-algorithm-identification.md<br>general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `key file` | pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `key reuse` | ctf-website/signature-key | ctf-website/techniques/13-signature/03-key-attacks.md |
| `key/generate` | ctf-website/litellm-privesc | ctf-website/techniques/09-cve/05-litellm-privesc.md |
| `keygen` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `keysign` | ctf-website/fd-theft-pidfd | general/techniques/01-kernel/03-mm-null-ptrace-bypass.md |
| `kfence` | general | general/techniques/01-kernel/02-slab-cross-cache.md |
| `kfence_ksize` | general | general/techniques/01-kernel/02-slab-cross-cache.md |
| `kmem_cache_free` | ctf-website/slab-cross-cache | general/techniques/01-kernel/02-slab-cross-cache.md |
| `kmem_cache_free mismatch` | general | general/techniques/01-kernel/02-slab-cross-cache.md |
| `kminfo innerhtml xss` | ctf-website | ctf-website/techniques/24-database/06-card-platform.md |
| `ksa` | apk-reverse/crypto | apk-reverse/techniques/04-crypto/01-game-encryption-patterns.md<br>apk-reverse/techniques/04-crypto/02-rc4-custom-crypto.md |
| `kubelet` | ctf-website/kubernetes | ctf-website/techniques/10-cloud/container-runtime-escape.md<br>ctf-website/techniques/10-cloud/k8s-rbac-attack-paths.md<br>ctf-website/techniques/10-cloud/kubernetes-container.md |
| `kubernetes` | ctf-website/kubernetes | ctf-website/techniques/10-cloud/container-runtime-escape.md<br>ctf-website/techniques/10-cloud/k8s-rbac-attack-paths.md<br>ctf-website/techniques/10-cloud/kubernetes-container.md |
| `kubernetes resourcequota 耗尽` | ctf-website | ctf-website/techniques/22-dos/11-cloud-container-dos.md |
| `lambda` | ctf-website/cloud-serverless | ctf-website/techniques/10-cloud/aws-iam-privesc.md<br>ctf-website/techniques/10-cloud/serverless-lambda.md |
| `laravel` | ctf-website/payment-php | ctf-website/techniques/12-payment/payment-php.md |
| `laravel fillable` | ctf-website/mass-assignment | ctf-website/techniques/15-mass-assignment/01-mass-assignment.md<br>ctf-website/techniques/15-mass-assignment/02-parameter-tampering.md |
| `lcg` | general/prng | general/techniques/crypto/03-prng-randomness-cracking.md |
| `lcg parameter recovery` | general | general/techniques/crypto/03-prng-randomness-cracking.md |
| `lcg 密钥流` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/10-nested-vm-matryoshka-reverse-and-defeat.md |
| `ld_preload` | general | general/techniques/cheating/02-packet-interception.md |
| `ldap` | ctf-website/ldap | ctf-website/techniques/02-auth/ldap-injection.md |
| `ldap filter` | ctf-website/ldap | ctf-website/techniques/02-auth/ldap-injection.md |
| `leaky paywall` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `length extension` | ctf-website/signature-length-extension | ctf-website/techniques/13-signature/05-length-extension.md |
| `length field detection` | general | general/techniques/protocol/01-unknown-protocol-reverse.md |
| `lfi` | ctf-website/file-attacks | ctf-website/techniques/06-file-attacks/file-upload-xxe-lfi.md |
| `lib` | apk-reverse/native | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md<br>apk-reverse/techniques/02-native/02-pointer-chain-patterns.md<br>apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `libapp.so` | apk-reverse | apk-reverse/techniques/02-native/07-unidbg-native-emulation-pipeline.md<br>apk-reverse/techniques/02-native/08-flutter-dart-aot-reconstruction.md |
| `libdexhelper` | apk-reverse, apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `libflutter.so` | apk-reverse | apk-reverse/techniques/02-native/08-flutter-dart-aot-reconstruction.md |
| `libil2cpp` | apk-reverse/native | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md<br>apk-reverse/techniques/02-native/02-pointer-chain-patterns.md<br>apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `libinject` | apk-reverse/patch-repack | apk-reverse/techniques/08-patch-repack/01-so-injection-repack.md |
| `libjiagu` | apk-reverse, apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `libshell` | apk-reverse, apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `libue4` | apk-reverse/native | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md<br>apk-reverse/techniques/02-native/02-pointer-chain-patterns.md<br>apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `license` | apk-reverse/network, ctf-website/payment-subscription, pe-reverse/license-keygen | apk-reverse/techniques/05-network/01-game-protocol-hook.md<br>apk-reverse/techniques/05-network/02-license-verification-bypass.md<br>ctf-website/techniques/12-payment/payment-subscription.md |
| `license key` | ctf-website/payment-digital-goods, pe-reverse | ctf-website/techniques/12-payment/payment-digital-goods.md<br>pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md |
| `licensed` | pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `licensingservice` | pe-reverse | pe-reverse/techniques/10-license-keygen/06-cloud-license-frida-hook.md |
| `linux 模拟运行 pe` | general | general/methodology/01-headless-emulation-windows-android-handbook.md |
| `litellm` | ctf-website/litellm-privesc | ctf-website/techniques/09-cve/05-litellm-privesc.md |
| `llm proxy` | ctf-website/race-lost-update | ctf-website/techniques/12-payment/payment-race-lost-update.md |
| `llvm ir lifting` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `load_file 文件读取` | ctf-website | ctf-website/techniques/24-database/01-sqli-fundamentals.md |
| `loader` | pe-reverse | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `loadlibrary` | apk-reverse/native, pe-reverse, pe-reverse/dynamic-analysis | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md<br>apk-reverse/techniques/02-native/02-pointer-chain-patterns.md<br>apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `loadlibrarya` | pe-reverse | pe-reverse/techniques/03-static-analysis/05-dynamic-api-resolution.md |
| `localstorage meter` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `localstorage.clear()` | ctf-website | ctf-website/techniques/23-paywall-bypass/05-dom-css-manipulation.md |
| `location header` | ctf-website/open-redirect | ctf-website/techniques/04-ssrf/open-redirect.md |
| `loop` | ctf-website/24h-loop-orchestration | ctf-website/techniques/00-workflow/24h-loop-orchestration.md<br>ctf-website/techniques/attack-network.md |
| `lost update` | ctf-website/race-lost-update | ctf-website/techniques/12-payment/payment-race-lost-update.md |
| `loyalty points` | ctf-website/payment-digital-goods | ctf-website/techniques/12-payment/payment-digital-goods.md |
| `lz4 magic 04 22 4d 18` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/05-high-entropy-compression-vs-crypto-routing.md |
| `mac shellcode` | pe-reverse/av-evasion | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `machine code` | pe-reverse/static-analysis | pe-reverse/techniques/03-static-analysis/01-struct-reconstruction.md<br>pe-reverse/techniques/03-static-analysis/02-disasm-jit-asm.md<br>pe-reverse/techniques/03-static-analysis/03-x64dbg-breakpoints.md |
| `machineguid` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `magento` | ctf-website/payment-php | ctf-website/techniques/12-payment/payment-php.md |
| `magic byte detection` | general | general/techniques/crypto/01-algorithm-identification.md |
| `magic hash` | ctf-website/payment-php, ctf-website/signature-implementation | ctf-website/techniques/12-payment/payment-php.md<br>ctf-website/techniques/13-signature/02-implementation.md |
| `magic prefix detection` | general | general/techniques/protocol/01-unknown-protocol-reverse.md |
| `maildir` | ctf-website/cpanel-caldav-traversal | ctf-website/techniques/09-cve/03-cpanel-caldav-traversal.md |
| `manifest` | apk-reverse/manifest | apk-reverse/techniques/03-manifest/01-entry-point-tracing.md |
| `manifest confusion` | ctf-website/supply-chain | ctf-website/techniques/11-supply-chain/dependency-confusion.md |
| `manual map` | pe-reverse, pe-reverse/dynamic-analysis | pe-reverse/techniques/04-dynamic-analysis/01-dll-injection.md<br>pe-reverse/techniques/04-dynamic-analysis/02-trampoline-detour.md<br>pe-reverse/techniques/04-dynamic-analysis/03-external-memory-rw.md |
| `manual mapping` | general | general/techniques/cheating/04-anti-cheat-bypass.md |
| `maps 检测` | apk-reverse | apk-reverse/techniques/07-packer/05-vmp-anti-debug-bypass.md |
| `mask` | pe-reverse/triage | pe-reverse/techniques/01-triage/01-aob-signature-scan.md |
| `mass assignment` | ctf-website/mass-assignment, ctf-website/payment-bypass, ctf-website/payment-php | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/12-payment/payment-php.md<br>ctf-website/techniques/15-mass-assignment/01-mass-assignment.md |
| `match` | pe-reverse/yara-sigma | pe-reverse/techniques/07-yara-sigma/01-yara-rule-writing.md |
| `math.random` | ctf-website/web-crypto, general/prng | ctf-website/techniques/07-client/web-crypto-abuse.md<br>general/techniques/crypto/03-prng-randomness-cracking.md |
| `matryoshka-vm` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/10-nested-vm-matryoshka-reverse-and-defeat.md |
| `max-height: 200px 正文容器` | ctf-website | ctf-website/techniques/23-paywall-bypass/05-dom-css-manipulation.md |
| `mba 混淆` | general, pe-reverse | general/crypto/02-angr-symbolic-execution-solver.md<br>pe-reverse/techniques/03-static-analysis/07-ida-microcode-mba-deobfuscation-d810.md |
| `mcp over http` | general | general/methodology/02-remote-mcp-device-bridge-deployment.md |
| `mcp tool mapping` | general | general/techniques/methodology/02-toolchain-decision-tree.md |
| `md5` | apk-reverse/crypto, general/crypto | apk-reverse/techniques/04-crypto/01-game-encryption-patterns.md<br>apk-reverse/techniques/04-crypto/02-rc4-custom-crypto.md<br>general/techniques/crypto/01-algorithm-identification.md |
| `md5 array` | ctf-website/signature-implementation | ctf-website/techniques/13-signature/02-implementation.md |
| `md5 downgrade` | ctf-website/signature-algorithm | ctf-website/techniques/13-signature/01-algorithm.md |
| `md5 extension` | ctf-website/signature-length-extension | ctf-website/techniques/13-signature/05-length-extension.md |
| `md5 sign` | ctf-website/signature | ctf-website/techniques/13-signature/00-overview.md<br>ctf-website/techniques/13-signature/01-algorithm.md<br>ctf-website/techniques/13-signature/02-implementation.md |
| `medium paywall` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `memcached udp` | ctf-website/dos | ctf-website/techniques/22-dos/01-application-layer-dos.md<br>ctf-website/techniques/22-dos/02-resource-exhaustion.md<br>ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `memcached udp 50,000x 放大` | ctf-website | ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `memcmp 校验` | pe-reverse | pe-reverse/techniques/10-license-keygen/02-validation-function-location.md |
| `memory dump` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md |
| `memory dumped pe` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/06-modern-pe-unmapping-and-dump-reconstruction.md |
| `memory hack` | general/cheating | general/techniques/cheating/01-memory-hacking.md<br>general/techniques/cheating/02-packet-interception.md<br>general/techniques/cheating/03-esp-wallhack-rendering.md |
| `memory patch` | pe-reverse/patch | pe-reverse/techniques/08-patch/01-code-patching.md |
| `memory read` | apk-reverse/dynamic-frida | apk-reverse/techniques/06-dynamic/01-memory-rw-hook.md<br>apk-reverse/techniques/06-dynamic/02-overlay-rendering-hook.md<br>apk-reverse/techniques/06-dynamic/03-touch-input-hook.md |
| `mersenne twister` | general/prng | general/techniques/crypto/03-prng-randomness-cracking.md |
| `message queue` | ctf-website/payment-callback | ctf-website/techniques/12-payment/payment-callback-async.md |
| `messagedigest` | apk-reverse | apk-reverse/techniques/08-patch-repack/02-signature-integrity-bypass.md |
| `messagepack` | general/protocol | general/techniques/protocol/01-unknown-protocol-reverse.md<br>general/techniques/protocol/02-protobuf-flatbuffers-reverse.md |
| `metadata` | ctf-website/ssrf | ctf-website/techniques/04-ssrf/ssrf.md |
| `metadata service` | ctf-website/cloud-serverless | ctf-website/techniques/10-cloud/aws-iam-privesc.md<br>ctf-website/techniques/10-cloud/serverless-lambda.md |
| `metered billing` | ctf-website/payment-subscription | ctf-website/techniques/12-payment/payment-subscription.md |
| `metered paywall` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `metered paywall article_limit cookie` | ctf-website | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md |
| `meterpreter` | pe-reverse/av-evasion | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `method` | apk-reverse/dex-java | apk-reverse/techniques/01-dex-java/01-smali-injection.md |
| `method override` | ctf-website/recon | ctf-website/techniques/01-recon/recon-routing.md<br>ctf-website/techniques/01-recon/version-fingerprinting.md |
| `methodology` | general/methodology | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `mfa fatigue` | ctf-website/rate-limit | ctf-website/techniques/16-rate-limit/01-rate-limit-bypass.md<br>ctf-website/techniques/16-rate-limit/02-brute-force-tactics.md |
| `microsoft 365` | ctf-website/dns-email | ctf-website/techniques/19-dns-email/01-subdomain-takeover.md<br>ctf-website/techniques/19-dns-email/02-email-spoofing.md |
| `misp` | pe-reverse | pe-reverse/techniques/06-ioc-extraction/01-ioc-extraction.md |
| `mixed boolean-arithmetic` | pe-reverse | pe-reverse/techniques/03-static-analysis/07-ida-microcode-mba-deobfuscation-d810.md |
| `mm-null` | ctf-website/fd-theft-pidfd | general/techniques/01-kernel/03-mm-null-ptrace-bypass.md |
| `mm-null window` | general | general/techniques/01-kernel/03-mm-null-ptrace-bypass.md |
| `modify` | apk-reverse/patch-repack, pe-reverse/patch | apk-reverse/techniques/08-patch-repack/01-so-injection-repack.md<br>pe-reverse/techniques/08-patch/01-code-patching.md |
| `mogvmp` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `mongodb` | ctf-website/database-attacks, ctf-website/sqli | ctf-website/techniques/03-injection/sqli-nosqli.md<br>ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md |
| `mongodb $ne $gt $regex` | ctf-website | ctf-website/techniques/24-database/03-nosql-injection.md |
| `monitoring` | ctf-website/nezha-path-traversal | ctf-website/techniques/09-cve/04-nezha-path-traversal-jwt.md |
| `mq attack` | ctf-website/payment-callback | ctf-website/techniques/12-payment/payment-callback-async.md |
| `mqtt` | ctf-website/websocket | ctf-website/techniques/07-client/websocket.md |
| `msfvenom` | pe-reverse/av-evasion | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `mssql` | ctf-website/sqli | ctf-website/techniques/03-injection/sqli-nosqli.md |
| `mt19937` | general/prng | general/techniques/crypto/03-prng-randomness-cracking.md |
| `mt19937 state cloning` | general | general/techniques/crypto/03-prng-randomness-cracking.md |
| `multibulk` | ctf-website/valkey-resp-dos | ctf-website/techniques/11-dos/01-valkey-resp-dos.md |
| `multidex` | apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `multipart 绕过 waf` | ctf-website | ctf-website/techniques/24-database/02-sqli-advanced.md |
| `mutation` | ctf-website/graphql | ctf-website/techniques/03-injection/graphql.md |
| `mutation xss` | ctf-website/xss | ctf-website/techniques/07-client/admin-bot-xss.md |
| `mutationobserver 动态注入` | ctf-website | ctf-website/techniques/23-paywall-bypass/05-dom-css-manipulation.md |
| `mutex` | pe-reverse/ioc | pe-reverse/techniques/06-ioc-extraction/01-ioc-extraction.md |
| `mutex name` | pe-reverse | pe-reverse/techniques/06-ioc-extraction/01-ioc-extraction.md |
| `mysql` | ctf-website/sqli | ctf-website/techniques/03-injection/sqli-nosqli.md |
| `naked` | pe-reverse/dynamic-analysis | pe-reverse/techniques/04-dynamic-analysis/01-dll-injection.md<br>pe-reverse/techniques/04-dynamic-analysis/02-trampoline-detour.md<br>pe-reverse/techniques/04-dynamic-analysis/03-external-memory-rw.md |
| `naked function` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/04-naked-function-hook.md |
| `name service switch` | ctf-website/cifswitch-nss | general/techniques/01-kernel/04-cifswitch-nss-privesc.md |
| `namespace abuse` | general | general/techniques/01-kernel/04-cifswitch-nss-privesc.md |
| `naming` | general/methodology | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `native` | apk-reverse/native | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md<br>apk-reverse/techniques/02-native/02-pointer-chain-patterns.md<br>apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `native method` | apk-reverse, apk-reverse/native | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md<br>apk-reverse/techniques/02-native/02-pointer-chain-patterns.md<br>apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `native stub` | apk-reverse, apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `native 签名算法` | apk-reverse | apk-reverse/techniques/02-native/07-unidbg-native-emulation-pipeline.md |
| `navigator is not defined` | ctf-website | ctf-website/techniques/27-js-reverse/02-browser-env-emulation-proxy-sandbox.md |
| `navigator.webdriver` | ctf-website | ctf-website/techniques/27-js-reverse/02-browser-env-emulation-proxy-sandbox.md |
| `ndk` | apk-reverse/native | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md<br>apk-reverse/techniques/02-native/02-pointer-chain-patterns.md<br>apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `ndr` | ctf-website/payment-bounce-idor | ctf-website/techniques/12-payment/payment-email-bounce-idor.md |
| `nested vm` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `nesting params` | ctf-website/mass-assignment | ctf-website/techniques/15-mass-assignment/01-mass-assignment.md<br>ctf-website/techniques/15-mass-assignment/02-parameter-tampering.md |
| `netstat syn flooding` | ctf-website | ctf-website/techniques/22-dos/06-tcp-state-exhaustion.md |
| `network capture` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/08-procmon-patterns.md |
| `networking.c` | ctf-website/valkey-resp-dos | ctf-website/techniques/11-dos/01-valkey-resp-dos.md |
| `new api` | ctf-website/race-lost-update | ctf-website/techniques/12-payment/payment-race-lost-update.md |
| `new-api` | ctf-website/race-lost-update | ctf-website/techniques/12-payment/payment-race-lost-update.md |
| `news paywall` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `next param` | ctf-website/open-redirect | ctf-website/techniques/04-ssrf/open-redirect.md |
| `nezha` | ctf-website/nezha-path-traversal | ctf-website/techniques/09-cve/04-nezha-path-traversal-jwt.md |
| `nf_conntrack_max 耗尽` | ctf-website | ctf-website/techniques/22-dos/06-tcp-state-exhaustion.md |
| `nfqueue` | general | general/techniques/cheating/02-packet-interception.md |
| `nginx` | ctf-website/nginx-rewrite-heapoverflow | ctf-website/techniques/09-cve/06-nginx-rewrite-heapoverflow.md |
| `ngx_http_rewrite_module` | ctf-website/nginx-rewrite-heapoverflow | ctf-website/techniques/09-cve/06-nginx-rewrite-heapoverflow.md |
| `no-scroll paywall-active class` | ctf-website | ctf-website/techniques/23-paywall-bypass/05-dom-css-manipulation.md |
| `node-serialize` | ctf-website/deserialization | ctf-website/techniques/05-deserialization/deserialization.md |
| `node.js` | ctf-website/prototype-pollution | ctf-website/techniques/03-injection/prototype-pollution.md |
| `nodeintegration` | ctf-website/mobile-bridge | ctf-website/techniques/21-mobile-bridge/01-webview-attacks.md<br>ctf-website/techniques/21-mobile-bridge/02-cordova-reactnative.md |
| `non-delivery receipt` | ctf-website/payment-bounce-idor | ctf-website/techniques/12-payment/payment-email-bounce-idor.md |
| `nonce bypass` | ctf-website/signature-replay | ctf-website/techniques/13-signature/06-replay-nonce.md |
| `nonce predict` | ctf-website/signature-replay | ctf-website/techniques/13-signature/06-replay-nonce.md |
| `nonce reuse` | ctf-website/signature-replay, general/prng | ctf-website/techniques/13-signature/06-replay-nonce.md<br>general/techniques/crypto/03-prng-randomness-cracking.md |
| `none algorithm` | ctf-website/signature-algorithm | ctf-website/techniques/13-signature/01-algorithm.md |
| `nop` | pe-reverse/patch | pe-reverse/techniques/08-patch/01-code-patching.md |
| `nop patch` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/05-anti-debug-bypass.md<br>pe-reverse/techniques/08-patch/01-code-patching.md |
| `nop 填充` | apk-reverse, apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `nosql` | ctf-website/database-attacks, ctf-website/sqli | ctf-website/techniques/03-injection/sqli-nosqli.md<br>ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md |
| `nosql 注入 mongodb redis` | ctf-website | ctf-website/techniques/24-database/00-overview.md |
| `note taking` | general/methodology | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `notepad plus plus` | ctf-website/notepadpp-config-injection | windows/techniques/notepadpp-config-injection.md |
| `notepad++` | windows | windows/techniques/notepadpp-config-injection.md |
| `notify` | ctf-website/payment | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/12-payment/payment-digital-goods.md |
| `novmp` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `npm` | ctf-website/supply-chain | ctf-website/techniques/11-supply-chain/dependency-confusion.md |
| `nsl` | pe-reverse | pe-reverse/techniques/10-license-keygen/06-cloud-license-frida-hook.md |
| `nss` | ctf-website/cifswitch-nss | general/techniques/01-kernel/04-cifswitch-nss-privesc.md |
| `nss module injection` | general | general/techniques/01-kernel/04-cifswitch-nss-privesc.md |
| `nt header` | pe-reverse/pe-structure | pe-reverse/techniques/02-pe-structure/01-pe-header-parsing.md |
| `ntdll` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/07-direct-syscall.md |
| `ntdll hook` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/07-direct-syscall.md |
| `ntglobalflag` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/05-anti-debug-bypass.md |
| `ntp monlist` | ctf-website/dos | ctf-website/techniques/22-dos/01-application-layer-dos.md<br>ctf-website/techniques/22-dos/02-resource-exhaustion.md<br>ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `ntp monlist 放大 556x` | ctf-website | ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `ntqueryinformationprocess` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/05-anti-debug-bypass.md |
| `nvd` | ctf-website/cve | ctf-website/techniques/09-cve/cve-correlation-graph.md<br>ctf-website/techniques/09-cve/cve-workflow.md<br>ctf-website/techniques/09-cve/multi-cve-chain-playbook.md |
| `nxdomain 响应占比 >90%` | ctf-website | ctf-website/techniques/22-dos/07-dns-dos.md |
| `nytimes paywall` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `oauth` | ctf-website/oauth | ctf-website/techniques/02-auth/oauth-sso.md |
| `oauth attack` | ctf-website/oauth-deep | ctf-website/techniques/20-oauth-deep/01-oauth-attack-chains.md<br>ctf-website/techniques/20-oauth-deep/02-session-fixation-attacks.md |
| `oauth2` | ctf-website/oauth | ctf-website/techniques/02-auth/oauth-sso.md |
| `ob 混淆` | ctf-website | ctf-website/techniques/27-js-reverse/01-ast-deobfuscation-pipeline.md |
| `obfuscate` | apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `obfuscated algorithm` | general/crypto | general/techniques/crypto/01-algorithm-identification.md<br>general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `obfuscation` | ctf-website/js-runtime, pe-reverse | ctf-website/techniques/07-client/js-runtime.md<br>pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `obfuscation handling` | general | general/techniques/methodology/02-toolchain-decision-tree.md |
| `object merge` | ctf-website/prototype-pollution | ctf-website/techniques/03-injection/prototype-pollution.md |
| `object reference` | ctf-website/idor | ctf-website/techniques/14-idor/01-idor-enumeration.md<br>ctf-website/techniques/14-idor/02-bac-business-logic.md |
| `obregistercallbacks` | general | general/techniques/cheating/01-memory-hacking.md |
| `ocr` | ctf-website/captcha-bypass | ctf-website/techniques/01-recon/captcha-bypass.md |
| `oep` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `offset` | apk-reverse/native, pe-reverse/static-analysis | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md<br>apk-reverse/techniques/02-native/02-pointer-chain-patterns.md<br>apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `oidc` | ctf-website/ci-cd, ctf-website/oauth | ctf-website/techniques/02-auth/oauth-sso.md<br>ctf-website/techniques/10-cloud/ci-cd-pipeline.md<br>ctf-website/techniques/10-cloud/github-actions-abuse-paths.md |
| `okhttp` | apk-reverse/network | apk-reverse/techniques/05-network/01-game-protocol-hook.md<br>apk-reverse/techniques/05-network/02-license-verification-bypass.md |
| `okhttp3.certificatepinner` | apk-reverse | apk-reverse/techniques/05-network/03-tls-pinning-unpinning.md |
| `oleaut32` | pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `oleloadpictureex` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/04-twinbasic-compressed-resource-recovery.md |
| `ollvm` | apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `ollvm so` | apk-reverse | apk-reverse/techniques/02-native/07-unidbg-native-emulation-pipeline.md |
| `ollvm 混淆消除` | pe-reverse | pe-reverse/techniques/03-static-analysis/07-ida-microcode-mba-deobfuscation-d810.md |
| `omnipay` | ctf-website/payment-php | ctf-website/techniques/12-payment/payment-php.md |
| `one api` | ctf-website/race-lost-update | ctf-website/techniques/12-payment/payment-race-lost-update.md |
| `oob` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `oob dns 带外 dnslog` | ctf-website | ctf-website/techniques/24-database/02-sqli-advanced.md |
| `open redirect` | ctf-website/open-redirect | ctf-website/techniques/04-ssrf/open-redirect.md |
| `openapi` | ctf-website/api-attacks | ctf-website/techniques/17-api-attacks/01-api-discovery-leak.md<br>ctf-website/techniques/17-api-attacks/02-api-key-leak.md |
| `openid` | ctf-website/oauth | ctf-website/techniques/02-auth/oauth-sso.md |
| `openprocess` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/03-external-memory-rw.md |
| `optimistic lock` | ctf-website/race-lost-update | ctf-website/techniques/12-payment/payment-race-lost-update.md |
| `oracle` | ctf-website/sqli | ctf-website/techniques/03-injection/sqli-nosqli.md |
| `order` | ctf-website/payment | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/12-payment/payment-digital-goods.md |
| `order by random()` | ctf-website | ctf-website/techniques/22-dos/13-database-dos.md |
| `order by 列数探测` | ctf-website | ctf-website/techniques/24-database/01-sqli-fundamentals.md |
| `order by 注入 case when` | ctf-website | ctf-website/techniques/24-database/02-sqli-advanced.md |
| `order detail leak` | ctf-website/payment-bounce-idor | ctf-website/techniques/12-payment/payment-email-bounce-idor.md |
| `order enumeration` | ctf-website/payment-bounce-idor | ctf-website/techniques/12-payment/payment-email-bounce-idor.md |
| `order idor` | ctf-website/payment-bounce-idor | ctf-website/techniques/12-payment/payment-email-bounce-idor.md |
| `org filter` | ctf-website/fofa | ctf-website/techniques/01-recon/fofa-hunting.md |
| `organization` | general/methodology | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `origin header` | ctf-website/cors-csrf | ctf-website/techniques/07-client/cors-csrf.md |
| `origin ip` | ctf-website/cloudflare-bypass | ctf-website/techniques/01-recon/cloudflare-bypass.md |
| `orm 注入 hql jpql` | ctf-website | ctf-website/techniques/24-database/00-overview.md |
| `overflow: hidden body 截断` | ctf-website | ctf-website/techniques/23-paywall-bypass/05-dom-css-manipulation.md |
| `overlay` | apk-reverse/dynamic-frida | apk-reverse/techniques/06-dynamic/01-memory-rw-hook.md<br>apk-reverse/techniques/06-dynamic/02-overlay-rendering-hook.md<br>apk-reverse/techniques/06-dynamic/03-touch-input-hook.md |
| `overlay rendering` | general | general/techniques/cheating/03-esp-wallhack-rendering.md |
| `overload` | apk-reverse/dynamic-frida | apk-reverse/techniques/06-dynamic/01-memory-rw-hook.md<br>apk-reverse/techniques/06-dynamic/02-overlay-rendering-hook.md<br>apk-reverse/techniques/06-dynamic/03-touch-input-hook.md |
| `oxorany` | apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `pack` | apk-reverse/packer, pe-reverse/crypto-unpack | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `package hijack` | ctf-website/supply-chain | ctf-website/techniques/11-supply-chain/dependency-confusion.md |
| `package.json` | ctf-website/supply-chain | ctf-website/techniques/11-supply-chain/dependency-confusion.md |
| `packer` | apk-reverse/packer, pe-reverse/crypto-unpack | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `packer detection` | general, pe-reverse | general/techniques/methodology/01-reverse-checklist-first-30-min.md<br>pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md |
| `packet` | apk-reverse/network, general/protocol | apk-reverse/techniques/05-network/01-game-protocol-hook.md<br>apk-reverse/techniques/05-network/02-license-verification-bypass.md<br>general/techniques/protocol/01-unknown-protocol-reverse.md |
| `packet intercept` | general/cheating | general/techniques/cheating/01-memory-hacking.md<br>general/techniques/cheating/02-packet-interception.md<br>general/techniques/cheating/03-esp-wallhack-rendering.md |
| `packet replay` | general | general/techniques/cheating/02-packet-interception.md |
| `page cache` | ctf-website/page-cache-write | general/techniques/01-kernel/01-page-cache-write-family.md |
| `page cache poisoning` | general | general/techniques/01-kernel/01-page-cache-write-family.md<br>general/techniques/01-kernel/05-pintheft-io-uring-page-cache.md |
| `pagemap` | apk-reverse/native | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md<br>apk-reverse/techniques/02-native/02-pointer-chain-patterns.md<br>apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `panic_bounds_check` | pe-reverse | pe-reverse/techniques/03-static-analysis/06-go-rust-binary-reconstruction.md |
| `parameter injection` | ctf-website/mass-assignment | ctf-website/techniques/15-mass-assignment/01-mass-assignment.md<br>ctf-website/techniques/15-mass-assignment/02-parameter-tampering.md |
| `parameter pollution` | ctf-website/hpp-crlf, ctf-website/signature-canonicalization | ctf-website/techniques/03-injection/hpp-crlf.md<br>ctf-website/techniques/13-signature/04-canonicalization.md |
| `parse_str` | ctf-website/signature-implementation | ctf-website/techniques/13-signature/02-implementation.md |
| `parseval` | pe-reverse | pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `passive recon` | ctf-website/fofa | ctf-website/techniques/01-recon/fofa-hunting.md |
| `passrole` | ctf-website/cloud-serverless | ctf-website/techniques/10-cloud/aws-iam-privesc.md<br>ctf-website/techniques/10-cloud/serverless-lambda.md |
| `password reset` | ctf-website/host-header | ctf-website/techniques/02-auth/host-header.md |
| `password spray` | ctf-website/rate-limit | ctf-website/techniques/16-rate-limit/01-rate-limit-bypass.md<br>ctf-website/techniques/16-rate-limit/02-brute-force-tactics.md |
| `patch` | apk-reverse/patch-repack, pe-reverse/patch | apk-reverse/techniques/08-patch-repack/01-so-injection-repack.md<br>pe-reverse/techniques/08-patch/01-code-patching.md |
| `path` | ctf-website/recon | ctf-website/techniques/01-recon/recon-routing.md<br>ctf-website/techniques/01-recon/version-fingerprinting.md |
| `path traversal` | ctf-website/cpanel-caldav-traversal, ctf-website/file-attacks, ctf-website/nezha-path-traversal | ctf-website/techniques/06-file-attacks/file-upload-xxe-lfi.md<br>ctf-website/techniques/09-cve/03-cpanel-caldav-traversal.md<br>ctf-website/techniques/09-cve/04-nezha-path-traversal-jwt.md |
| `pattern` | pe-reverse/yara-sigma | pe-reverse/techniques/07-yara-sigma/01-yara-rule-writing.md |
| `pattern scan` | pe-reverse/triage | pe-reverse/techniques/01-triage/01-aob-signature-scan.md |
| `pattern scanning` | pe-reverse | pe-reverse/techniques/01-triage/01-aob-signature-scan.md |
| `pay` | ctf-website/payment | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/12-payment/payment-digital-goods.md |
| `payload` | pe-reverse/av-evasion | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `payment` | ctf-website/payment | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/12-payment/payment-digital-goods.md |
| `payment bypass` | ctf-website/payment-bypass | ctf-website/techniques/12-payment/payment-bypass.md |
| `payment callback` | ctf-website/payment-callback | ctf-website/techniques/12-payment/payment-callback-async.md |
| `paypal` | ctf-website/payment | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/12-payment/payment-digital-goods.md |
| `paywall` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `paywall overlay div.paywall` | ctf-website | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md |
| `paywall overlay position:fixed z-index:9999` | ctf-website | ctf-website/techniques/23-paywall-bypass/05-dom-css-manipulation.md |
| `pbkdf` | general/crypto | general/techniques/crypto/01-algorithm-identification.md<br>general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `pclntab` | pe-reverse | pe-reverse/techniques/03-static-analysis/06-go-rust-binary-reconstruction.md |
| `pdf generation` | ctf-website/file-attacks | ctf-website/techniques/06-file-attacks/file-upload-xxe-lfi.md |
| `pe loader` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/06-manual-map-injection.md |
| `pe signature` | pe-reverse | pe-reverse/techniques/02-pe-structure/01-pe-header-parsing.md<br>pe-reverse/techniques/07-yara-sigma/01-yara-rule-writing.md |
| `pe unmapping` | pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `pe-sieve dump` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/06-modern-pe-unmapping-and-dump-reconstruction.md |
| `peb` | pe-reverse, pe-reverse/dynamic-analysis | pe-reverse/techniques/04-dynamic-analysis/01-dll-injection.md<br>pe-reverse/techniques/04-dynamic-analysis/02-trampoline-detour.md<br>pe-reverse/techniques/04-dynamic-analysis/03-external-memory-rw.md |
| `peb.beingdebugged` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/05-anti-debug-bypass.md |
| `peb_ldr_data` | pe-reverse | pe-reverse/techniques/03-static-analysis/05-dynamic-api-resolution.md |
| `pebble` | ctf-website/ssti | ctf-website/techniques/03-injection/ssti.md |
| `pendingapproval` | general | general/methodology/02-remote-mcp-device-bridge-deployment.md |
| `performance api` | ctf-website/csp-cors-advanced | ctf-website/techniques/18-cors-csp-advanced/01-csp-bypass.md<br>ctf-website/techniques/18-cors-csp-advanced/02-xs-leaks-browser-sidechannels.md |
| `permission` | apk-reverse/manifest | apk-reverse/techniques/03-manifest/01-entry-point-tracing.md |
| `persisted query` | ctf-website/graphql | ctf-website/techniques/03-injection/graphql.md |
| `pgp` | pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `pgp 清文签名` | pe-reverse | pe-reverse/techniques/10-license-keygen/04-signature-chain-pubkey-swap.md |
| `pgp 签名` | pe-reverse | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md |
| `phantom domain 静默丢弃` | ctf-website | ctf-website/techniques/22-dos/07-dns-dos.md |
| `phar` | ctf-website/payment-php | ctf-website/techniques/12-payment/payment-php.md |
| `phishing` | ctf-website/dns-email | ctf-website/techniques/19-dns-email/01-subdomain-takeover.md<br>ctf-website/techniques/19-dns-email/02-email-spoofing.md |
| `php` | ctf-website/payment-php | ctf-website/techniques/12-payment/payment-php.md |
| `php mt_rand` | general/prng | general/techniques/crypto/03-prng-randomness-cracking.md |
| `php mt_rand seed recovery` | general | general/techniques/crypto/03-prng-randomness-cracking.md |
| `php serialization` | ctf-website/payment-php | ctf-website/techniques/12-payment/payment-php.md |
| `php session` | ctf-website/payment-php | ctf-website/techniques/12-payment/payment-php.md |
| `php wrapper` | ctf-website/file-attacks | ctf-website/techniques/06-file-attacks/file-upload-xxe-lfi.md |
| `php://filter 源码读取` | ctf-website | ctf-website/techniques/24-database/04-config-exposure.md |
| `phpinfo() document_root` | ctf-website | ctf-website/techniques/24-database/04-config-exposure.md |
| `phpmyadmin` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `phpmyadmin /phpmyadmin/` | ctf-website | ctf-website/techniques/24-database/05-backup-log-leak.md |
| `phpmyadmin adminer 未授权` | ctf-website | ctf-website/techniques/24-database/00-overview.md |
| `physical address` | apk-reverse/native | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md<br>apk-reverse/techniques/02-native/02-pointer-chain-patterns.md<br>apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `piano` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `piano overlay` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `piano tinypass script[src*=\"tinypass.com\"]` | ctf-website | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md |
| `pickle` | ctf-website/deserialization | ctf-website/techniques/05-deserialization/deserialization.md |
| `pidfd` | ctf-website/fd-theft-pidfd | general/techniques/01-kernel/03-mm-null-ptrace-bypass.md |
| `pidfd_getfd` | general | general/techniques/01-kernel/03-mm-null-ptrace-bypass.md |
| `pin count` | ctf-website/pintheft-io-uring | general/techniques/01-kernel/05-pintheft-io-uring-page-cache.md |
| `pipe` | pe-reverse/ioc | pe-reverse/techniques/06-ioc-extraction/01-ioc-extraction.md |
| `pipeline` | ctf-website/ci-cd, ctf-website/valkey-resp-dos | ctf-website/techniques/10-cloud/ci-cd-pipeline.md<br>ctf-website/techniques/10-cloud/github-actions-abuse-paths.md<br>ctf-website/techniques/10-cloud/terraform-state-secrets.md |
| `pkce` | ctf-website/oauth | ctf-website/techniques/02-auth/oauth-sso.md |
| `pkce bypass` | ctf-website/oauth-deep | ctf-website/techniques/20-oauth-deep/01-oauth-attack-chains.md<br>ctf-website/techniques/20-oauth-deep/02-session-fixation-attacks.md |
| `pkcs padding` | general | general/techniques/crypto/01-algorithm-identification.md |
| `plan switch` | ctf-website/payment-subscription | ctf-website/techniques/12-payment/payment-subscription.md |
| `platform channel` | ctf-website/mobile-bridge | ctf-website/techniques/21-mobile-bridge/01-webview-attacks.md<br>ctf-website/techniques/21-mobile-bridge/02-cordova-reactnative.md |
| `play integrity` | apk-reverse | apk-reverse/techniques/08-patch-repack/02-signature-integrity-bypass.md |
| `playwright` | ctf-website/captcha-bypass | ctf-website/techniques/01-recon/captcha-bypass.md |
| `plus alias` | ctf-website/cpanel-caldav-traversal | ctf-website/techniques/09-cve/03-cpanel-caldav-traversal.md |
| `png resource` | pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `poc` | ctf-website/cve | ctf-website/techniques/09-cve/cve-correlation-graph.md<br>ctf-website/techniques/09-cve/cve-workflow.md<br>ctf-website/techniques/09-cve/multi-cve-chain-playbook.md |
| `pod` | ctf-website/kubernetes | ctf-website/techniques/10-cloud/container-runtime-escape.md<br>ctf-website/techniques/10-cloud/k8s-rbac-attack-paths.md<br>ctf-website/techniques/10-cloud/kubernetes-container.md |
| `pod oomkilled exit 137` | ctf-website | ctf-website/techniques/22-dos/11-cloud-container-dos.md |
| `pods/exec` | ctf-website/kubernetes | ctf-website/techniques/10-cloud/container-runtime-escape.md<br>ctf-website/techniques/10-cloud/k8s-rbac-attack-paths.md<br>ctf-website/techniques/10-cloud/kubernetes-container.md |
| `pointer chain` | apk-reverse/native, pe-reverse, pe-reverse/dynamic-analysis | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md<br>apk-reverse/techniques/02-native/02-pointer-chain-patterns.md<br>apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `pointer scan` | general/cheating | general/techniques/cheating/01-memory-hacking.md<br>general/techniques/cheating/02-packet-interception.md<br>general/techniques/cheating/03-esp-wallhack-rendering.md |
| `pointer scanning` | general | general/techniques/cheating/01-memory-hacking.md |
| `pointertorawdata == virtualaddress` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/06-modern-pe-unmapping-and-dump-reconstruction.md |
| `policy simulation` | ctf-website/cloud-serverless | ctf-website/techniques/10-cloud/aws-iam-privesc.md<br>ctf-website/techniques/10-cloud/serverless-lambda.md |
| `poool` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `poool script[src*=\".poool.fr/\"]` | ctf-website | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md |
| `post message` | ctf-website/postmessage | ctf-website/techniques/07-client/postmessage.md |
| `postgresql` | ctf-website/sqli | ctf-website/techniques/03-injection/sqli-nosqli.md |
| `postman collection` | ctf-website/api-attacks | ctf-website/techniques/17-api-attacks/01-api-discovery-leak.md<br>ctf-website/techniques/17-api-attacks/02-api-key-leak.md |
| `postmessage` | ctf-website/postmessage | ctf-website/techniques/07-client/postmessage.md |
| `pp` | ctf-website/prototype-pollution | ctf-website/techniques/03-injection/prototype-pollution.md |
| `pre-auth dos` | ctf-website/valkey-resp-dos | ctf-website/techniques/11-dos/01-valkey-resp-dos.md |
| `predictable random` | general/prng | general/techniques/crypto/03-prng-randomness-cracking.md |
| `preferences.json` | pe-reverse | pe-reverse/techniques/10-license-keygen/05-keygen-frida-verification-loop.md |
| `preg_match cpu 100%` | ctf-website | ctf-website/techniques/22-dos/04-redos.md |
| `present hook` | general | general/techniques/cheating/03-esp-wallhack-rendering.md |
| `prga` | apk-reverse/crypto | apk-reverse/techniques/04-crypto/01-game-encryption-patterns.md<br>apk-reverse/techniques/04-crypto/02-rc4-custom-crypto.md |
| `price manipulation` | ctf-website/mass-assignment, ctf-website/payment-bypass | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/15-mass-assignment/01-mass-assignment.md<br>ctf-website/techniques/15-mass-assignment/02-parameter-tampering.md |
| `privilege escalation` | ctf-website/litellm-privesc, general | ctf-website/techniques/09-cve/05-litellm-privesc.md<br>general/techniques/01-kernel/05-pintheft-io-uring-page-cache.md |
| `privileged` | ctf-website/kubernetes | ctf-website/techniques/10-cloud/container-runtime-escape.md<br>ctf-website/techniques/10-cloud/k8s-rbac-attack-paths.md<br>ctf-website/techniques/10-cloud/kubernetes-container.md |
| `prng` | ctf-website/web-crypto, general/prng | ctf-website/techniques/07-client/web-crypto-abuse.md<br>general/techniques/crypto/03-prng-randomness-cracking.md |
| `proc node` | apk-reverse/native | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md<br>apk-reverse/techniques/02-native/02-pointer-chain-patterns.md<br>apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `procdump` | pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `process hollowing` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/06-modern-pe-unmapping-and-dump-reconstruction.md |
| `process monitor` | pe-reverse/dynamic-analysis | pe-reverse/techniques/04-dynamic-analysis/01-dll-injection.md<br>pe-reverse/techniques/04-dynamic-analysis/02-trampoline-detour.md<br>pe-reverse/techniques/04-dynamic-analysis/03-external-memory-rw.md |
| `process_vm_readv` | apk-reverse/dynamic-frida | apk-reverse/techniques/06-dynamic/01-memory-rw-hook.md<br>apk-reverse/techniques/06-dynamic/02-overlay-rendering-hook.md<br>apk-reverse/techniques/06-dynamic/03-touch-input-hook.md |
| `procfs` | apk-reverse/native | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md<br>apk-reverse/techniques/02-native/02-pointer-chain-patterns.md<br>apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `procmon` | pe-reverse, pe-reverse/dynamic-analysis | pe-reverse/techniques/04-dynamic-analysis/01-dll-injection.md<br>pe-reverse/techniques/04-dynamic-analysis/02-trampoline-detour.md<br>pe-reverse/techniques/04-dynamic-analysis/03-external-memory-rw.md |
| `proguard` | apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `proration` | ctf-website/payment-subscription | ctf-website/techniques/12-payment/payment-subscription.md |
| `protobuf` | apk-reverse/network, ctf-website/grpc, general/protocol | apk-reverse/techniques/05-network/01-game-protocol-hook.md<br>apk-reverse/techniques/05-network/02-license-verification-bypass.md<br>ctf-website/techniques/03-injection/grpc-protobuf.md |
| `protocol` | apk-reverse/network, general/protocol | apk-reverse/techniques/05-network/01-game-protocol-hook.md<br>apk-reverse/techniques/05-network/02-license-verification-bypass.md<br>general/techniques/protocol/01-unknown-protocol-reverse.md |
| `protocol buffer` | ctf-website/grpc | ctf-website/techniques/03-injection/grpc-protobuf.md |
| `protocol reverse` | general | general/techniques/cheating/02-packet-interception.md |
| `prototype pollution` | ctf-website/prototype-pollution | ctf-website/techniques/03-injection/prototype-pollution.md |
| `provider` | apk-reverse/manifest | apk-reverse/techniques/03-manifest/01-entry-point-tracing.md |
| `proxy 探针` | ctf-website | ctf-website/techniques/27-js-reverse/02-browser-env-emulation-proxy-sandbox.md |
| `proxy_admin` | ctf-website/litellm-privesc | ctf-website/techniques/09-cve/05-litellm-privesc.md |
| `ptrace` | apk-reverse, apk-reverse/packer, ctf-website/fd-theft-pidfd | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `ptrace bypass` | general | general/techniques/01-kernel/03-mm-null-ptrace-bypass.md |
| `pubkey swap` | pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `publisher paywall` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `pug` | ctf-website/prototype-pollution | ctf-website/techniques/03-injection/prototype-pollution.md |
| `pull_request_target` | ctf-website/ci-cd | ctf-website/techniques/10-cloud/ci-cd-pipeline.md<br>ctf-website/techniques/10-cloud/github-actions-abuse-paths.md<br>ctf-website/techniques/10-cloud/terraform-state-secrets.md |
| `push bombing` | ctf-website/rate-limit | ctf-website/techniques/16-rate-limit/01-rate-limit-bypass.md<br>ctf-website/techniques/16-rate-limit/02-brute-force-tactics.md |
| `pushad` | pe-reverse/dynamic-analysis | pe-reverse/techniques/04-dynamic-analysis/01-dll-injection.md<br>pe-reverse/techniques/04-dynamic-analysis/02-trampoline-detour.md<br>pe-reverse/techniques/04-dynamic-analysis/03-external-memory-rw.md |
| `pushad/popad` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/04-naked-function-hook.md |
| `pypi` | ctf-website/supply-chain | ctf-website/techniques/11-supply-chain/dependency-confusion.md |
| `qiling framework` | general | general/methodology/01-headless-emulation-windows-android-handbook.md |
| `quake` | ctf-website/fofa | ctf-website/techniques/01-recon/fofa-hunting.md |
| `query` | ctf-website/sqli | ctf-website/techniques/03-injection/sqli-nosqli.md |
| `queryperformancecounter` | general, general/cheating | general/techniques/cheating/01-memory-hacking.md<br>general/techniques/cheating/02-packet-interception.md<br>general/techniques/cheating/03-esp-wallhack-rendering.md |
| `quic cid 耗尽` | ctf-website | ctf-website/techniques/22-dos/05-http2-continuation.md |
| `quota bypass` | ctf-website/race-lost-update | ctf-website/techniques/12-payment/payment-race-lost-update.md |
| `qvd-2026-27616` | ctf-website/pintheft-io-uring | general/techniques/01-kernel/05-pintheft-io-uring-page-cache.md |
| `qvd-2026-29453` | ctf-website/cifswitch-nss | general/techniques/01-kernel/04-cifswitch-nss-privesc.md |
| `race condition` | ctf-website/race-lost-update, ctf-website/race-smuggling | ctf-website/techniques/08-infra/race-cache-smuggling.md<br>ctf-website/techniques/12-payment/payment-race-lost-update.md |
| `race condition coupon` | ctf-website/mass-assignment | ctf-website/techniques/15-mass-assignment/01-mass-assignment.md<br>ctf-website/techniques/15-mass-assignment/02-parameter-tampering.md |
| `random` | general/prng | general/techniques/crypto/03-prng-randomness-cracking.md |
| `random.nextint` | general/prng | general/techniques/crypto/03-prng-randomness-cracking.md |
| `range header 缓存穿透` | ctf-website | ctf-website/techniques/22-dos/09-cache-cdn-dos.md |
| `rapid reset` | ctf-website/dos | ctf-website/techniques/22-dos/01-application-layer-dos.md<br>ctf-website/techniques/22-dos/02-resource-exhaustion.md<br>ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `rapid reset cve-2023-44487` | ctf-website | ctf-website/techniques/22-dos/01-application-layer-dos.md |
| `rate limit` | ctf-website/rate-limit | ctf-website/techniques/16-rate-limit/01-rate-limit-bypass.md<br>ctf-website/techniques/16-rate-limit/02-brute-force-tactics.md |
| `raw deflate` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `raw deflate 78 5e 头` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/04-twinbasic-compressed-resource-recovery.md |
| `razor` | ctf-website/ssti | ctf-website/techniques/03-injection/ssti.md |
| `rbac` | ctf-website/kubernetes | ctf-website/techniques/10-cloud/container-runtime-escape.md<br>ctf-website/techniques/10-cloud/k8s-rbac-attack-paths.md<br>ctf-website/techniques/10-cloud/kubernetes-container.md |
| `rc4` | apk-reverse/crypto | apk-reverse/techniques/04-crypto/01-game-encryption-patterns.md<br>apk-reverse/techniques/04-crypto/02-rc4-custom-crypto.md |
| `rdb` | ctf-website/redis-valkey-restore-zipmap | ctf-website/techniques/09-cve/02-redis-zipmap-rce.md |
| `rds` | ctf-website/pintheft-io-uring | general/techniques/01-kernel/05-pintheft-io-uring-page-cache.md |
| `rds zerocopy` | general | general/techniques/01-kernel/05-pintheft-io-uring-page-cache.md |
| `rdtsc hook` | general | general/techniques/cheating/05-speedhack-time-manipulation.md |
| `react native` | ctf-website/mobile-bridge | ctf-website/techniques/21-mobile-bridge/01-webview-attacks.md<br>ctf-website/techniques/21-mobile-bridge/02-cordova-reactnative.md |
| `readprocessmemory` | pe-reverse, pe-reverse/dynamic-analysis | pe-reverse/techniques/04-dynamic-analysis/01-dll-injection.md<br>pe-reverse/techniques/04-dynamic-analysis/02-trampoline-detour.md<br>pe-reverse/techniques/04-dynamic-analysis/03-external-memory-rw.md |
| `real ip` | ctf-website/cloudflare-bypass | ctf-website/techniques/01-recon/cloudflare-bypass.md |
| `real-time` | ctf-website/websocket | ctf-website/techniques/07-client/websocket.md |
| `realtime` | ctf-website/websocket | ctf-website/techniques/07-client/websocket.md |
| `recaptcha` | ctf-website/captcha-bypass | ctf-website/techniques/01-recon/captcha-bypass.md |
| `receipt` | ctf-website/payment-digital-goods | ctf-website/techniques/12-payment/payment-digital-goods.md |
| `receiver` | apk-reverse/manifest | apk-reverse/techniques/03-manifest/01-entry-point-tracing.md |
| `recharge` | ctf-website/payment | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/12-payment/payment-digital-goods.md |
| `reclass` | pe-reverse, pe-reverse/static-analysis | pe-reverse/techniques/03-static-analysis/01-struct-reconstruction.md<br>pe-reverse/techniques/03-static-analysis/02-disasm-jit-asm.md<br>pe-reverse/techniques/03-static-analysis/03-x64dbg-breakpoints.md |
| `recon` | ctf-website/recon | ctf-website/techniques/01-recon/recon-routing.md<br>ctf-website/techniques/01-recon/version-fingerprinting.md |
| `reconciliation` | ctf-website/payment-callback | ctf-website/techniques/12-payment/payment-callback-async.md |
| `reconnaissance` | ctf-website/recon | ctf-website/techniques/01-recon/recon-routing.md<br>ctf-website/techniques/01-recon/version-fingerprinting.md |
| `reconstruct` | pe-reverse/static-analysis | pe-reverse/techniques/03-static-analysis/01-struct-reconstruction.md<br>pe-reverse/techniques/03-static-analysis/02-disasm-jit-asm.md<br>pe-reverse/techniques/03-static-analysis/03-x64dbg-breakpoints.md |
| `recurring` | ctf-website/payment-subscription | ctf-website/techniques/12-payment/payment-subscription.md |
| `recvfrom` | apk-reverse/network | apk-reverse/techniques/05-network/01-game-protocol-hook.md<br>apk-reverse/techniques/05-network/02-license-verification-bypass.md |
| `redirect` | ctf-website/open-redirect | ctf-website/techniques/04-ssrf/open-redirect.md |
| `redirect_uri` | ctf-website/oauth, ctf-website/open-redirect | ctf-website/techniques/02-auth/oauth-sso.md<br>ctf-website/techniques/04-ssrf/open-redirect.md |
| `redirect_uri bypass` | ctf-website/oauth-deep | ctf-website/techniques/20-oauth-deep/01-oauth-attack-chains.md<br>ctf-website/techniques/20-oauth-deep/02-session-fixation-attacks.md |
| `redis` | ctf-website/database-attacks, ctf-website/redis-valkey-restore-zipmap | ctf-website/techniques/09-cve/02-redis-zipmap-rce.md<br>ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md |
| `redis ping 未授权 config set` | ctf-website | ctf-website/techniques/24-database/03-nosql-injection.md |
| `redos` | ctf-website/redos-timing | ctf-website/techniques/03-injection/redos-timing.md |
| `redos cve-2020-5243` | ctf-website | ctf-website/techniques/22-dos/04-redos.md |
| `referer spoof` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `referer: https://www.google.com/` | ctf-website | ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md |
| `reflective` | pe-reverse/dynamic-analysis | pe-reverse/techniques/04-dynamic-analysis/01-dll-injection.md<br>pe-reverse/techniques/04-dynamic-analysis/02-trampoline-detour.md<br>pe-reverse/techniques/04-dynamic-analysis/03-external-memory-rw.md |
| `reflective dll` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/06-modern-pe-unmapping-and-dump-reconstruction.md |
| `refresh token abuse` | ctf-website/oauth-deep | ctf-website/techniques/20-oauth-deep/01-oauth-attack-chains.md<br>ctf-website/techniques/20-oauth-deep/02-session-fixation-attacks.md |
| `refund` | ctf-website/payment | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/12-payment/payment-digital-goods.md |
| `regex` | ctf-website/redos-timing | ctf-website/techniques/03-injection/redos-timing.md |
| `regexfilter paywall sdk` | ctf-website | ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `register context` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/02-trampoline-detour.md |
| `registernatives` | apk-reverse, apk-reverse/native | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md<br>apk-reverse/techniques/02-native/02-pointer-chain-patterns.md<br>apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `registration wall` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `registry` | pe-reverse/ioc | pe-reverse/techniques/06-ioc-extraction/01-ioc-extraction.md |
| `registry key` | pe-reverse | pe-reverse/techniques/06-ioc-extraction/01-ioc-extraction.md |
| `registry monitoring` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/08-procmon-patterns.md |
| `regkey` | pe-reverse/ioc | pe-reverse/techniques/06-ioc-extraction/01-ioc-extraction.md |
| `regsetvalueex` | pe-reverse | pe-reverse/techniques/06-ioc-extraction/02-persistence-startup-chain.md |
| `regular expression` | ctf-website/redos-timing | ctf-website/techniques/03-injection/redos-timing.md |
| `rel32 exclusion` | pe-reverse | pe-reverse/techniques/01-triage/01-aob-signature-scan.md |
| `relative offset table` | pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `relocation` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/06-manual-map-injection.md |
| `remember-me` | ctf-website/oauth-deep | ctf-website/techniques/20-oauth-deep/01-oauth-attack-chains.md<br>ctf-website/techniques/20-oauth-deep/02-session-fixation-attacks.md |
| `remill` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `renderer sandbox` | ctf-website/chrome-uaf-blink | ctf-website/techniques/09-cve/01-browser-sandbox-escape.md |
| `renegotiation 重协商循环` | ctf-website | ctf-website/techniques/22-dos/08-tls-exhaustion.md |
| `renewal` | ctf-website/payment-subscription | ctf-website/techniques/12-payment/payment-subscription.md |
| `repack` | apk-reverse/patch-repack | apk-reverse/techniques/08-patch-repack/01-so-injection-repack.md |
| `replay attack` | ctf-website/payment-callback, ctf-website/signature-replay | ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/13-signature/06-replay-nonce.md |
| `replay sig` | ctf-website/signature-replay | ctf-website/techniques/13-signature/06-replay-nonce.md |
| `request` | apk-reverse/network | apk-reverse/techniques/05-network/01-game-protocol-hook.md<br>apk-reverse/techniques/05-network/02-license-verification-bypass.md |
| `request smuggling` | ctf-website/race-smuggling | ctf-website/techniques/08-infra/race-cache-smuggling.md |
| `request-key` | general | general/techniques/01-kernel/04-cifswitch-nss-privesc.md |
| `resource exhaustion` | ctf-website/dos | ctf-website/techniques/22-dos/01-application-layer-dos.md<br>ctf-website/techniques/22-dos/02-resource-exhaustion.md<br>ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `resp` | ctf-website/valkey-resp-dos | ctf-website/techniques/11-dos/01-valkey-resp-dos.md |
| `resp 协议 redis` | ctf-website | ctf-website/techniques/24-database/03-nosql-injection.md |
| `response` | apk-reverse/network | apk-reverse/techniques/05-network/01-game-protocol-hook.md<br>apk-reverse/techniques/05-network/02-license-verification-bypass.md |
| `response splitting` | ctf-website/hpp-crlf | ctf-website/techniques/03-injection/hpp-crlf.md |
| `restore` | ctf-website/redis-valkey-restore-zipmap | ctf-website/techniques/09-cve/02-redis-zipmap-rce.md |
| `retrofit` | apk-reverse/network | apk-reverse/techniques/05-network/01-game-protocol-hook.md<br>apk-reverse/techniques/05-network/02-license-verification-bypass.md |
| `return url` | ctf-website/open-redirect | ctf-website/techniques/04-ssrf/open-redirect.md |
| `rewrite` | ctf-website/nginx-rewrite-heapoverflow | ctf-website/techniques/09-cve/06-nginx-rewrite-heapoverflow.md |
| `rish` | general | general/methodology/02-remote-mcp-device-bridge-deployment.md |
| `ror13` | pe-reverse | pe-reverse/techniques/03-static-analysis/05-dynamic-api-resolution.md |
| `rounding attack` | ctf-website/payment-bypass | ctf-website/techniques/12-payment/payment-bypass.md |
| `route` | ctf-website/recon | ctf-website/techniques/01-recon/recon-routing.md<br>ctf-website/techniques/01-recon/version-fingerprinting.md |
| `rpc` | apk-reverse/dynamic-frida | apk-reverse/techniques/06-dynamic/01-memory-rw-hook.md<br>apk-reverse/techniques/06-dynamic/02-overlay-rendering-hook.md<br>apk-reverse/techniques/06-dynamic/03-touch-input-hook.md |
| `rpm/wpm` | general | general/techniques/cheating/01-memory-hacking.md |
| `rs256 hs256` | ctf-website/signature-algorithm | ctf-website/techniques/13-signature/01-algorithm.md |
| `rsa` | apk-reverse/crypto, general/crypto | apk-reverse/techniques/04-crypto/01-game-encryption-patterns.md<br>apk-reverse/techniques/04-crypto/02-rc4-custom-crypto.md<br>general/techniques/crypto/01-algorithm-identification.md |
| `rsa key` | ctf-website/web-crypto | ctf-website/techniques/07-client/web-crypto-abuse.md |
| `rsa 签名` | pe-reverse | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/04-signature-chain-pubkey-swap.md |
| `rudy` | ctf-website/dos | ctf-website/techniques/22-dos/01-application-layer-dos.md<br>ctf-website/techniques/22-dos/02-resource-exhaustion.md<br>ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `rule` | pe-reverse/yara-sigma | pe-reverse/techniques/07-yara-sigma/01-yara-rule-writing.md |
| `runc` | ctf-website/kubernetes | ctf-website/techniques/10-cloud/container-runtime-escape.md<br>ctf-website/techniques/10-cloud/k8s-rbac-attack-paths.md<br>ctf-website/techniques/10-cloud/kubernetes-container.md |
| `runner` | ctf-website/ci-cd | ctf-website/techniques/10-cloud/ci-cd-pipeline.md<br>ctf-website/techniques/10-cloud/github-actions-abuse-paths.md<br>ctf-website/techniques/10-cloud/terraform-state-secrets.md |
| `runtime vm detection` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `runtime.g` | pe-reverse | pe-reverse/techniques/03-static-analysis/06-go-rust-binary-reconstruction.md |
| `runtime.morestack` | pe-reverse | pe-reverse/techniques/03-static-analysis/06-go-rust-binary-reconstruction.md |
| `rust binary` | pe-reverse | pe-reverse/techniques/03-static-analysis/06-go-rust-binary-reconstruction.md |
| `rustc` | pe-reverse | pe-reverse/techniques/03-static-analysis/06-go-rust-binary-reconstruction.md |
| `s-box` | general/crypto | general/techniques/crypto/01-algorithm-identification.md<br>general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `s-box fingerprinting` | general | general/techniques/crypto/01-algorithm-identification.md |
| `same origin` | ctf-website/cors-csrf | ctf-website/techniques/07-client/cors-csrf.md |
| `samesite` | ctf-website/cors-csrf | ctf-website/techniques/07-client/cors-csrf.md |
| `samesite bypass` | ctf-website/oauth-deep | ctf-website/techniques/20-oauth-deep/01-oauth-attack-chains.md<br>ctf-website/techniques/20-oauth-deep/02-session-fixation-attacks.md |
| `saml` | ctf-website/saml | ctf-website/techniques/02-auth/saml-attacks.md |
| `saml response` | ctf-website/saml | ctf-website/techniques/02-auth/saml-attacks.md |
| `sample triage` | general | general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `sanitizer` | ctf-website/xss | ctf-website/techniques/07-client/admin-bot-xss.md |
| `scan engine` | ctf-website/fofa | ctf-website/techniques/01-recon/fofa-hunting.md |
| `schtasks` | pe-reverse | pe-reverse/techniques/06-ioc-extraction/02-persistence-startup-chain.md |
| `scope escalation` | ctf-website/oauth-deep | ctf-website/techniques/20-oauth-deep/01-oauth-attack-chains.md<br>ctf-website/techniques/20-oauth-deep/02-session-fixation-attacks.md |
| `script id=\"__next_data__\` | ctf-website | ctf-website/techniques/23-paywall-bypass/04-content-extraction.md |
| `script type=\"application/ld+json\` | ctf-website | ctf-website/techniques/23-paywall-bypass/04-content-extraction.md |
| `script[src*=\"piano.io\"]` | ctf-website | ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `script[src*=\"poool.fr\"]` | ctf-website | ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `script[src*=\"tinypass.com\"]` | ctf-website | ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `scylla` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `scyllahide` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/05-anti-debug-bypass.md |
| `seat` | ctf-website/payment-subscription | ctf-website/techniques/12-payment/payment-subscription.md |
| `second order` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `secret key leak` | ctf-website/signature-key | ctf-website/techniques/13-signature/03-key-attacks.md |
| `secret_key` | ctf-website/signature-key | ctf-website/techniques/13-signature/03-key-attacks.md |
| `secretkey` | apk-reverse/crypto | apk-reverse/techniques/04-crypto/01-game-encryption-patterns.md<br>apk-reverse/techniques/04-crypto/02-rc4-custom-crypto.md |
| `section` | pe-reverse/pe-structure | pe-reverse/techniques/02-pe-structure/01-pe-header-parsing.md |
| `section filtering` | pe-reverse | pe-reverse/techniques/01-triage/01-aob-signature-scan.md |
| `section table` | pe-reverse | pe-reverse/techniques/02-pe-structure/01-pe-header-parsing.md |
| `sectionalignment vs filealignment` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/06-modern-pe-unmapping-and-dump-reconstruction.md |
| `securitytrails` | ctf-website/cloudflare-bypass | ctf-website/techniques/01-recon/cloudflare-bypass.md |
| `seed recovery` | general/prng | general/techniques/crypto/03-prng-randomness-cracking.md |
| `seh handler 噪声` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `select sleep(30)` | ctf-website | ctf-website/techniques/22-dos/13-database-dos.md |
| `self extract` | apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `self-healing emulation` | general, general/methodology, pe-reverse | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `self-hosted` | ctf-website/ci-cd | ctf-website/techniques/10-cloud/ci-cd-pipeline.md<br>ctf-website/techniques/10-cloud/github-actions-abuse-paths.md<br>ctf-website/techniques/10-cloud/terraform-state-secrets.md |
| `self-replication` | pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `selfsubjectaccessreview` | ctf-website/kubernetes | ctf-website/techniques/10-cloud/container-runtime-escape.md<br>ctf-website/techniques/10-cloud/k8s-rbac-attack-paths.md<br>ctf-website/techniques/10-cloud/kubernetes-container.md |
| `send` | apk-reverse/dynamic-frida | apk-reverse/techniques/06-dynamic/01-memory-rw-hook.md<br>apk-reverse/techniques/06-dynamic/02-overlay-rendering-hook.md<br>apk-reverse/techniques/06-dynamic/03-touch-input-hook.md |
| `sender forgery` | ctf-website/dns-email | ctf-website/techniques/19-dns-email/01-subdomain-takeover.md<br>ctf-website/techniques/19-dns-email/02-email-spoofing.md |
| `sendto` | apk-reverse/network | apk-reverse/techniques/05-network/01-game-protocol-hook.md<br>apk-reverse/techniques/05-network/02-license-verification-bypass.md |
| `serial` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `serialized value` | ctf-website/redis-valkey-restore-zipmap | ctf-website/techniques/09-cve/02-redis-zipmap-rce.md |
| `server-side request forgery` | ctf-website/ssrf | ctf-website/techniques/04-ssrf/ssrf.md |
| `server-side validation` | general | general/techniques/cheating/05-speedhack-time-manipulation.md |
| `serverless` | ctf-website/cloud-serverless | ctf-website/techniques/10-cloud/aws-iam-privesc.md<br>ctf-website/techniques/10-cloud/serverless-lambda.md |
| `serverless 计费爆炸` | ctf-website | ctf-website/techniques/22-dos/11-cloud-container-dos.md |
| `service` | apk-reverse/manifest | apk-reverse/techniques/03-manifest/01-entry-point-tracing.md |
| `service account` | ctf-website/kubernetes | ctf-website/techniques/10-cloud/container-runtime-escape.md<br>ctf-website/techniques/10-cloud/k8s-rbac-attack-paths.md<br>ctf-website/techniques/10-cloud/kubernetes-container.md |
| `session fixation` | ctf-website/oauth-deep | ctf-website/techniques/20-oauth-deep/01-oauth-attack-chains.md<br>ctf-website/techniques/20-oauth-deep/02-session-fixation-attacks.md |
| `session puzzling` | ctf-website/oauth-deep | ctf-website/techniques/20-oauth-deep/01-oauth-attack-chains.md<br>ctf-website/techniques/20-oauth-deep/02-session-fixation-attacks.md |
| `session ticket cache churn` | ctf-website | ctf-website/techniques/22-dos/08-tls-exhaustion.md |
| `set` | ctf-website/nginx-rewrite-heapoverflow | ctf-website/techniques/09-cve/06-nginx-rewrite-heapoverflow.md |
| `settings_header_table_size` | ctf-website | ctf-website/techniques/22-dos/05-http2-continuation.md |
| `settlement` | ctf-website/payment-callback | ctf-website/techniques/12-payment/payment-callback-async.md |
| `sha` | apk-reverse/crypto | apk-reverse/techniques/04-crypto/01-game-encryption-patterns.md<br>apk-reverse/techniques/04-crypto/02-rc4-custom-crypto.md |
| `sha-1 signature mismatch` | apk-reverse | apk-reverse/techniques/07-packer/02-modern-art-dex-dump-and-repair.md |
| `sha-256 白名单` | pe-reverse | pe-reverse/techniques/10-license-keygen/04-signature-chain-pubkey-swap.md |
| `sha1` | general/crypto | general/techniques/crypto/01-algorithm-identification.md<br>general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `sha1 array` | ctf-website/signature-implementation | ctf-website/techniques/13-signature/02-implementation.md |
| `sha1 extension` | ctf-website/signature-length-extension | ctf-website/techniques/13-signature/05-length-extension.md |
| `sha1 sign` | ctf-website/signature | ctf-website/techniques/13-signature/00-overview.md<br>ctf-website/techniques/13-signature/01-algorithm.md<br>ctf-website/techniques/13-signature/02-implementation.md |
| `sha256` | general/crypto | general/techniques/crypto/01-algorithm-identification.md<br>general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `sha256 extension` | ctf-website/signature-length-extension | ctf-website/techniques/13-signature/05-length-extension.md |
| `sha256 sign` | ctf-website/signature | ctf-website/techniques/13-signature/00-overview.md<br>ctf-website/techniques/13-signature/01-algorithm.md<br>ctf-website/techniques/13-signature/02-implementation.md |
| `shader modification` | general | general/techniques/cheating/03-esp-wallhack-rendering.md |
| `shellcode` | pe-reverse, pe-reverse/av-evasion | pe-reverse/techniques/04-dynamic-analysis/06-manual-map-injection.md<br>pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `shellcode encrypt` | pe-reverse/av-evasion | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `shellcode encryption` | pe-reverse | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `shellcode obfuscate` | pe-reverse/av-evasion | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `shellexecute` | windows | windows/techniques/notepadpp-config-injection.md |
| `shizuku` | general | general/methodology/02-remote-mcp-device-bridge-deployment.md |
| `shodan` | ctf-website/cloudflare-bypass | ctf-website/techniques/01-recon/cloudflare-bypass.md |
| `shuji` | ctf-website | ctf-website/techniques/27-js-reverse/03-sourcemap-unpack-and-webpack-hijacking.md |
| `side channel` | ctf-website/csp-cors-advanced, ctf-website/redos-timing, general/crypto | ctf-website/techniques/03-injection/redos-timing.md<br>ctf-website/techniques/18-cors-csp-advanced/01-csp-bypass.md<br>ctf-website/techniques/18-cors-csp-advanced/02-xs-leaks-browser-sidechannels.md |
| `sigma` | pe-reverse/yara-sigma | pe-reverse/techniques/07-yara-sigma/01-yara-rule-writing.md |
| `sign` | apk-reverse/patch-repack, ctf-website/signature | apk-reverse/techniques/08-patch-repack/01-so-injection-repack.md<br>ctf-website/techniques/13-signature/00-overview.md<br>ctf-website/techniques/13-signature/01-algorithm.md |
| `sign_method` | ctf-website/signature | ctf-website/techniques/13-signature/00-overview.md<br>ctf-website/techniques/13-signature/01-algorithm.md<br>ctf-website/techniques/13-signature/02-implementation.md |
| `sign_type` | ctf-website/signature | ctf-website/techniques/13-signature/00-overview.md<br>ctf-website/techniques/13-signature/01-algorithm.md<br>ctf-website/techniques/13-signature/02-implementation.md |
| `signature` | ctf-website/signature, pe-reverse/triage, pe-reverse/yara-sigma | ctf-website/techniques/13-signature/00-overview.md<br>ctf-website/techniques/13-signature/01-algorithm.md<br>ctf-website/techniques/13-signature/02-implementation.md |
| `signature bypass` | ctf-website/payment-callback, ctf-website/signature | ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/13-signature/00-overview.md<br>ctf-website/techniques/13-signature/01-algorithm.md |
| `signature check` | apk-reverse, apk-reverse/patch-repack | apk-reverse/techniques/08-patch-repack/01-so-injection-repack.md<br>apk-reverse/techniques/08-patch-repack/02-signature-integrity-bypass.md |
| `signature extraction` | pe-reverse | pe-reverse/techniques/01-triage/01-aob-signature-scan.md |
| `signature forgery` | ctf-website/signature | ctf-website/techniques/13-signature/00-overview.md<br>ctf-website/techniques/13-signature/01-algorithm.md<br>ctf-website/techniques/13-signature/02-implementation.md |
| `signature nonce` | ctf-website/signature-replay | ctf-website/techniques/13-signature/06-replay-nonce.md |
| `signature replay` | ctf-website/signature-replay | ctf-website/techniques/13-signature/06-replay-nonce.md |
| `signature verification` | ctf-website/signature | ctf-website/techniques/13-signature/00-overview.md<br>ctf-website/techniques/13-signature/01-algorithm.md<br>ctf-website/techniques/13-signature/02-implementation.md |
| `signing key` | ctf-website/signature-key | ctf-website/techniques/13-signature/03-key-attacks.md |
| `signinginfo` | apk-reverse | apk-reverse/techniques/08-patch-repack/02-signature-integrity-bypass.md |
| `simd pattern scan` | general | general/techniques/cheating/01-memory-hacking.md |
| `simd sse 展开` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/10-nested-vm-matryoshka-reverse-and-defeat.md |
| `site paywall` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `sizeof deduction` | pe-reverse | pe-reverse/techniques/03-static-analysis/01-struct-reconstruction.md |
| `skb_small_head_cache` | general | general/techniques/01-kernel/02-slab-cross-cache.md |
| `slab` | ctf-website/slab-cross-cache | general/techniques/01-kernel/02-slab-cross-cache.md |
| `slab cross-cache` | general | general/techniques/01-kernel/02-slab-cross-cache.md |
| `sleep benchmark 时间盲注` | ctf-website | ctf-website/techniques/24-database/01-sqli-fundamentals.md |
| `slider` | ctf-website/captcha-bypass | ctf-website/techniques/01-recon/captcha-bypass.md |
| `slow http` | ctf-website/dos | ctf-website/techniques/22-dos/01-application-layer-dos.md<br>ctf-website/techniques/22-dos/02-resource-exhaustion.md<br>ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `slow.log general.log mysql` | ctf-website | ctf-website/techniques/24-database/05-backup-log-leak.md |
| `slowloris` | ctf-website/dos | ctf-website/techniques/22-dos/01-application-layer-dos.md<br>ctf-website/techniques/22-dos/02-resource-exhaustion.md<br>ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `slowloris incomplete request` | ctf-website | ctf-website/techniques/22-dos/01-application-layer-dos.md |
| `slub corruption` | general | general/techniques/01-kernel/02-slab-cross-cache.md |
| `smali` | apk-reverse/dex-java | apk-reverse/techniques/01-dex-java/01-smali-injection.md |
| `smarty` | ctf-website/ssti | ctf-website/techniques/03-injection/ssti.md |
| `sms verify` | ctf-website/captcha-bypass | ctf-website/techniques/01-recon/captcha-bypass.md |
| `smt solver` | general | general/crypto/02-angr-symbolic-execution-solver.md |
| `smtp injection` | ctf-website/dns-email, ctf-website/hpp-crlf | ctf-website/techniques/03-injection/hpp-crlf.md<br>ctf-website/techniques/19-dns-email/01-subdomain-takeover.md<br>ctf-website/techniques/19-dns-email/02-email-spoofing.md |
| `snapshot_hash` | apk-reverse | apk-reverse/techniques/02-native/08-flutter-dart-aot-reconstruction.md |
| `so inject` | apk-reverse/patch-repack | apk-reverse/techniques/08-patch-repack/01-so-injection-repack.md |
| `soap` | ctf-website/api-attacks | ctf-website/techniques/17-api-attacks/01-api-discovery-leak.md<br>ctf-website/techniques/17-api-attacks/02-api-key-leak.md |
| `socket` | apk-reverse/network | apk-reverse/techniques/05-network/01-game-protocol-hook.md<br>apk-reverse/techniques/05-network/02-license-verification-bypass.md |
| `socket buffer 内存压力` | ctf-website | ctf-website/techniques/22-dos/06-tcp-state-exhaustion.md |
| `socket.io` | ctf-website/websocket | ctf-website/techniques/07-client/websocket.md |
| `software breakpoint` | pe-reverse | pe-reverse/techniques/03-static-analysis/03-x64dbg-breakpoints.md |
| `solve license` | general | general/crypto/02-angr-symbolic-execution-solver.md |
| `sophi` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `sophi script[src*=\".sophi.io/\"]` | ctf-website | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md |
| `source map` | ctf-website/api-attacks | ctf-website/techniques/17-api-attacks/01-api-discovery-leak.md<br>ctf-website/techniques/17-api-attacks/02-api-key-leak.md |
| `sourcemap` | ctf-website | ctf-website/techniques/27-js-reverse/03-sourcemap-unpack-and-webpack-hijacking.md |
| `sourcemappingurl` | ctf-website | ctf-website/techniques/27-js-reverse/03-sourcemap-unpack-and-webpack-hijacking.md |
| `space mapping` | ctf-website/fofa | ctf-website/techniques/01-recon/fofa-hunting.md |
| `spawn` | apk-reverse/dynamic-frida | apk-reverse/techniques/06-dynamic/01-memory-rw-hook.md<br>apk-reverse/techniques/06-dynamic/02-overlay-rendering-hook.md<br>apk-reverse/techniques/06-dynamic/03-touch-input-hook.md |
| `speed hack` | general/cheating | general/techniques/cheating/01-memory-hacking.md<br>general/techniques/cheating/02-packet-interception.md<br>general/techniques/cheating/03-esp-wallhack-rendering.md |
| `spf` | ctf-website/dns-email | ctf-website/techniques/19-dns-email/01-subdomain-takeover.md<br>ctf-website/techniques/19-dns-email/02-email-spoofing.md |
| `spf bypass` | ctf-website/dns-email | ctf-website/techniques/19-dns-email/01-subdomain-takeover.md<br>ctf-website/techniques/19-dns-email/02-email-spoofing.md |
| `splice` | ctf-website/page-cache-write | general/techniques/01-kernel/01-page-cache-write-family.md |
| `splice zero-copy` | general | general/techniques/01-kernel/01-page-cache-write-family.md |
| `spnego` | ctf-website/cifswitch-nss | general/techniques/01-kernel/04-cifswitch-nss-privesc.md |
| `spring boot binding` | ctf-website/mass-assignment | ctf-website/techniques/15-mass-assignment/01-mass-assignment.md<br>ctf-website/techniques/15-mass-assignment/02-parameter-tampering.md |
| `sql` | ctf-website/database-attacks, ctf-website/sqli | ctf-website/techniques/03-injection/sqli-nosqli.md<br>ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md |
| `sql injection` | ctf-website/sqli | ctf-website/techniques/03-injection/sqli-nosqli.md |
| `sql 注入 injection` | ctf-website | ctf-website/techniques/24-database/00-overview.md |
| `sqli` | ctf-website/database-attacks, ctf-website/sqli | ctf-website/techniques/03-injection/sqli-nosqli.md<br>ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md |
| `sqlite` | ctf-website/sqli | ctf-website/techniques/03-injection/sqli-nosqli.md |
| `sqlite write lock` | ctf-website/race-lost-update | ctf-website/techniques/12-payment/payment-race-lost-update.md |
| `ssdp ws-discovery 放大` | ctf-website | ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `ssh keysign` | ctf-website/fd-theft-pidfd | general/techniques/01-kernel/03-mm-null-ptrace-bypass.md |
| `ssl` | apk-reverse/network | apk-reverse/techniques/05-network/01-game-protocol-hook.md<br>apk-reverse/techniques/05-network/02-license-verification-bypass.md |
| `ssl pinning` | apk-reverse/crypto | apk-reverse/techniques/04-crypto/01-game-encryption-patterns.md<br>apk-reverse/techniques/04-crypto/02-rc4-custom-crypto.md |
| `ssl search` | ctf-website/cloudflare-bypass | ctf-website/techniques/01-recon/cloudflare-bypass.md |
| `ssl unpinning` | general | general/techniques/cheating/02-packet-interception.md |
| `ssl 结构体内存 ~70kb/连接` | ctf-website | ctf-website/techniques/22-dos/08-tls-exhaustion.md |
| `ssl_accept 超时` | ctf-website | ctf-website/techniques/22-dos/08-tls-exhaustion.md |
| `ssl_get_verify_result` | apk-reverse | apk-reverse/techniques/05-network/03-tls-pinning-unpinning.md |
| `sslhandshakeexception` | apk-reverse | apk-reverse/techniques/05-network/03-tls-pinning-unpinning.md |
| `sso` | ctf-website/oauth | ctf-website/techniques/02-auth/oauth-sso.md |
| `sso hijack` | ctf-website/oauth-deep | ctf-website/techniques/20-oauth-deep/01-oauth-attack-chains.md<br>ctf-website/techniques/20-oauth-deep/02-session-fixation-attacks.md |
| `ssrf` | ctf-website/ssrf | ctf-website/techniques/04-ssrf/ssrf.md |
| `ssrf 内网 ip 10.x 172.16.x` | ctf-website | ctf-website/techniques/22-dos/12-ssrf-dos.md |
| `ssrf 内网数据库` | ctf-website | ctf-website/techniques/24-database/00-overview.md |
| `ssti` | ctf-website/ssti | ctf-website/techniques/03-injection/ssti.md |
| `stalker` | apk-reverse, apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `startup chain` | apk-reverse/manifest | apk-reverse/techniques/03-manifest/01-entry-point-tracing.md |
| `startup folder` | pe-reverse | pe-reverse/techniques/06-ioc-extraction/02-persistence-startup-chain.md |
| `state machine` | ctf-website/payment-bypass, general/protocol | ctf-website/techniques/12-payment/payment-bypass.md<br>general/techniques/protocol/01-unknown-protocol-reverse.md<br>general/techniques/protocol/02-protobuf-flatbuffers-reverse.md |
| `state machine inference` | general | general/techniques/protocol/01-unknown-protocol-reverse.md |
| `state nonce` | ctf-website/oauth | ctf-website/techniques/02-auth/oauth-sso.md |
| `state replay` | ctf-website/oauth-deep | ctf-website/techniques/20-oauth-deep/01-oauth-attack-chains.md<br>ctf-website/techniques/20-oauth-deep/02-session-fixation-attacks.md |
| `stealth` | ctf-website/captcha-bypass | ctf-website/techniques/01-recon/captcha-bypass.md |
| `steam` | ctf-website/payment-digital-goods | ctf-website/techniques/12-payment/payment-digital-goods.md |
| `strcmp` | ctf-website/payment-php | ctf-website/techniques/12-payment/payment-php.md |
| `strcmp bypass` | ctf-website/signature-implementation | ctf-website/techniques/13-signature/02-implementation.md |
| `stream cipher` | general/crypto | general/techniques/crypto/01-algorithm-identification.md<br>general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `stream multiplexing` | ctf-website/http2 | ctf-website/techniques/08-infra/http2-attacks.md |
| `stream 优先级 starvation` | ctf-website | ctf-website/techniques/22-dos/05-http2-continuation.md |
| `strict-dynamic bypass` | ctf-website/csp-cors-advanced | ctf-website/techniques/18-cors-csp-advanced/01-csp-bypass.md<br>ctf-website/techniques/18-cors-csp-advanced/02-xs-leaks-browser-sidechannels.md |
| `string array shift` | ctf-website | ctf-website/techniques/27-js-reverse/01-ast-deobfuscation-pipeline.md |
| `string encryption` | apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `string matching` | pe-reverse | pe-reverse/techniques/07-yara-sigma/01-yara-rule-writing.md |
| `strings extraction` | general | general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `stripe` | ctf-website/payment | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/12-payment/payment-digital-goods.md |
| `stripe billing` | ctf-website/payment-subscription | ctf-website/techniques/12-payment/payment-subscription.md |
| `stripe key` | ctf-website/api-attacks | ctf-website/techniques/17-api-attacks/01-api-discovery-leak.md<br>ctf-website/techniques/17-api-attacks/02-api-key-leak.md |
| `struct` | pe-reverse/static-analysis | pe-reverse/techniques/03-static-analysis/01-struct-reconstruction.md<br>pe-reverse/techniques/03-static-analysis/02-disasm-jit-asm.md<br>pe-reverse/techniques/03-static-analysis/03-x64dbg-breakpoints.md |
| `struct reconstruction` | pe-reverse | pe-reverse/techniques/03-static-analysis/01-struct-reconstruction.md |
| `structure rebuild` | pe-reverse/static-analysis | pe-reverse/techniques/03-static-analysis/01-struct-reconstruction.md<br>pe-reverse/techniques/03-static-analysis/02-disasm-jit-asm.md<br>pe-reverse/techniques/03-static-analysis/03-x64dbg-breakpoints.md |
| `structured clone` | ctf-website/postmessage | ctf-website/techniques/07-client/postmessage.md |
| `sts` | ctf-website/cloud-serverless | ctf-website/techniques/10-cloud/aws-iam-privesc.md<br>ctf-website/techniques/10-cloud/serverless-lambda.md |
| `subdomain takeover` | ctf-website/dns-email | ctf-website/techniques/19-dns-email/01-subdomain-takeover.md<br>ctf-website/techniques/19-dns-email/02-email-spoofing.md |
| `subscription` | ctf-website/graphql, ctf-website/payment-subscription | ctf-website/techniques/03-injection/graphql.md<br>ctf-website/techniques/12-payment/payment-subscription.md |
| `substack paywall` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `substitution-permutation` | general/crypto | general/techniques/crypto/01-algorithm-identification.md<br>general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `subtle` | ctf-website/web-crypto | ctf-website/techniques/07-client/web-crypto-abuse.md |
| `suid` | general | general/techniques/01-kernel/03-mm-null-ptrace-bypass.md |
| `supply chain` | ctf-website/supply-chain | ctf-website/techniques/11-supply-chain/dependency-confusion.md |
| `svg` | ctf-website/xss | ctf-website/techniques/07-client/admin-bot-xss.md |
| `swagger` | ctf-website/api-attacks | ctf-website/techniques/17-api-attacks/01-api-discovery-leak.md<br>ctf-website/techniques/17-api-attacks/02-api-key-leak.md |
| `symbolic execution` | general, pe-reverse | general/crypto/02-angr-symbolic-execution-solver.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `syn_recv 半连接队列溢出` | ctf-website | ctf-website/techniques/22-dos/06-tcp-state-exhaustion.md |
| `syscall` | apk-reverse, pe-reverse, pe-reverse/dynamic-analysis | apk-reverse/techniques/07-packer/05-vmp-anti-debug-bypass.md<br>pe-reverse/techniques/04-dynamic-analysis/01-dll-injection.md<br>pe-reverse/techniques/04-dynamic-analysis/02-trampoline-detour.md |
| `syscall bypass` | pe-reverse/av-evasion | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `syscall number` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/07-direct-syscall.md |
| `system.load` | apk-reverse/native | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md<br>apk-reverse/techniques/02-native/02-pointer-chain-patterns.md<br>apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `system.loadlibrary` | apk-reverse | apk-reverse/techniques/02-native/06-jni-register-natives-tracing.md |
| `t-table` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/05-high-entropy-compression-vs-crypto-routing.md |
| `tcp` | general/protocol | general/techniques/protocol/01-unknown-protocol-reverse.md<br>general/techniques/protocol/02-protobuf-flatbuffers-reverse.md |
| `tcp fast open 滥用` | ctf-website | ctf-website/techniques/22-dos/06-tcp-state-exhaustion.md |
| `tcp window 0 sockstress` | ctf-website | ctf-website/techniques/22-dos/06-tcp-state-exhaustion.md |
| `tcpdump` | general/protocol | general/techniques/protocol/01-unknown-protocol-reverse.md<br>general/techniques/protocol/02-protobuf-flatbuffers-reverse.md |
| `te.cl` | ctf-website/race-smuggling | ctf-website/techniques/08-infra/race-cache-smuggling.md |
| `technology stack` | ctf-website/recon | ctf-website/techniques/01-recon/recon-routing.md<br>ctf-website/techniques/01-recon/version-fingerprinting.md |
| `template engine` | ctf-website/ssti | ctf-website/techniques/03-injection/ssti.md |
| `template injection` | ctf-website/ssti | ctf-website/techniques/03-injection/ssti.md |
| `termux-open` | general | general/methodology/02-remote-mcp-device-bridge-deployment.md |
| `terraform` | ctf-website/ci-cd | ctf-website/techniques/10-cloud/ci-cd-pipeline.md<br>ctf-website/techniques/10-cloud/github-actions-abuse-paths.md<br>ctf-website/techniques/10-cloud/terraform-state-secrets.md |
| `tfstate` | ctf-website/ci-cd | ctf-website/techniques/10-cloud/ci-cd-pipeline.md<br>ctf-website/techniques/10-cloud/github-actions-abuse-paths.md<br>ctf-website/techniques/10-cloud/terraform-state-secrets.md |
| `thank you` | pe-reverse | pe-reverse/techniques/10-license-keygen/02-validation-function-location.md |
| `themida` | pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `thinkphp` | ctf-website/payment-php | ctf-website/techniques/12-payment/payment-php.md |
| `thread.backtrace` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `throttle bypass` | ctf-website/rate-limit | ctf-website/techniques/16-rate-limit/01-rate-limit-bypass.md<br>ctf-website/techniques/16-rate-limit/02-brute-force-tactics.md |
| `thunderrt6` | pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `thunderrt6formdc` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/04-twinbasic-compressed-resource-recovery.md |
| `thymeleaf` | ctf-website/ssti | ctf-website/techniques/03-injection/ssti.md |
| `tick manipulation` | general | general/techniques/cheating/05-speedhack-time-manipulation.md |
| `time manipulation` | general/cheating | general/techniques/cheating/01-memory-hacking.md<br>general/techniques/cheating/02-packet-interception.md<br>general/techniques/cheating/03-esp-wallhack-rendering.md |
| `time-based` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `time.timescale` | general | general/techniques/cheating/05-speedhack-time-manipulation.md |
| `time_wait 条目 > 50000` | ctf-website | ctf-website/techniques/22-dos/06-tcp-state-exhaustion.md |
| `timestamp bypass` | ctf-website/signature-replay | ctf-website/techniques/13-signature/06-replay-nonce.md |
| `timing attack` | ctf-website/redos-timing, general/crypto | ctf-website/techniques/03-injection/redos-timing.md<br>general/techniques/crypto/01-algorithm-identification.md<br>general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `timing attack sign` | ctf-website/signature-implementation | ctf-website/techniques/13-signature/02-implementation.md |
| `tinypass` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `tls` | apk-reverse/network | apk-reverse/techniques/05-network/01-game-protocol-hook.md<br>apk-reverse/techniques/05-network/02-license-verification-bypass.md |
| `tls callback` | pe-reverse | pe-reverse/techniques/02-pe-structure/02-tls-callback-analysis.md |
| `tls directory` | pe-reverse | pe-reverse/techniques/02-pe-structure/02-tls-callback-analysis.md |
| `tls 握手不对称 rsa 2048` | ctf-website | ctf-website/techniques/22-dos/08-tls-exhaustion.md |
| `tlv` | general/protocol | general/techniques/protocol/01-unknown-protocol-reverse.md<br>general/techniques/protocol/02-protobuf-flatbuffers-reverse.md |
| `toctou` | ctf-website/race-lost-update, ctf-website/race-smuggling | ctf-website/techniques/08-infra/race-cache-smuggling.md<br>ctf-website/techniques/12-payment/payment-race-lost-update.md |
| `toctou payment` | ctf-website/payment-callback | ctf-website/techniques/12-payment/payment-callback-async.md |
| `token` | ctf-website/jwt, ctf-website/payment-digital-goods | ctf-website/techniques/02-auth/jwt/00-overview.md<br>ctf-website/techniques/02-auth/jwt/01-alg-none.md<br>ctf-website/techniques/02-auth/jwt/02-algorithm-confusion.md |
| `token reuse` | ctf-website/captcha-bypass | ctf-website/techniques/01-recon/captcha-bypass.md |
| `tool selection` | general | general/techniques/methodology/02-toolchain-decision-tree.md |
| `toolchain` | general/methodology | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `tools/call` | general | general/methodology/02-remote-mcp-device-bridge-deployment.md |
| `tornado` | ctf-website/ssti | ctf-website/techniques/03-injection/ssti.md |
| `tostring() 防篡改` | ctf-website | ctf-website/techniques/27-js-reverse/02-browser-env-emulation-proxy-sandbox.md |
| `touch` | apk-reverse/dynamic-frida | apk-reverse/techniques/06-dynamic/01-memory-rw-hook.md<br>apk-reverse/techniques/06-dynamic/02-overlay-rendering-hook.md<br>apk-reverse/techniques/06-dynamic/03-touch-input-hook.md |
| `trace` | apk-reverse, pe-reverse | apk-reverse/techniques/07-packer/04-vmp-dump-trace-recovery.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `trace logging` | pe-reverse | pe-reverse/techniques/03-static-analysis/03-x64dbg-breakpoints.md |
| `tracerpid` | apk-reverse, apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `trade` | ctf-website/payment | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/12-payment/payment-digital-goods.md |
| `trampoline` | pe-reverse, pe-reverse/dynamic-analysis | pe-reverse/techniques/04-dynamic-analysis/01-dll-injection.md<br>pe-reverse/techniques/04-dynamic-analysis/02-trampoline-detour.md<br>pe-reverse/techniques/04-dynamic-analysis/03-external-memory-rw.md |
| `trampoline generation` | pe-reverse | pe-reverse/techniques/03-static-analysis/02-disasm-jit-asm.md |
| `triage` | general/methodology | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `trial` | ctf-website/payment-subscription, pe-reverse/license-keygen | ctf-website/techniques/12-payment/payment-subscription.md<br>pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md |
| `triton` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `true ip` | ctf-website/cloudflare-bypass | ctf-website/techniques/01-recon/cloudflare-bypass.md |
| `trustmanager` | apk-reverse | apk-reverse/techniques/05-network/03-tls-pinning-unpinning.md |
| `turbo intruder` | ctf-website/race-smuggling | ctf-website/techniques/08-infra/race-cache-smuggling.md |
| `turnstile` | ctf-website/captcha-bypass | ctf-website/techniques/01-recon/captcha-bypass.md |
| `twig` | ctf-website/ssti | ctf-website/techniques/03-injection/ssti.md |
| `twinbasic` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `twinbasic.ico` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/04-twinbasic-compressed-resource-recovery.md |
| `type confusion` | ctf-website/payment-bypass | ctf-website/techniques/12-payment/payment-bypass.md |
| `type juggling` | ctf-website/payment-php | ctf-website/techniques/12-payment/payment-php.md |
| `type juggling sign` | ctf-website/signature-implementation | ctf-website/techniques/13-signature/02-implementation.md |
| `typosquatting` | ctf-website/supply-chain | ctf-website/techniques/11-supply-chain/dependency-confusion.md |
| `uaf` | ctf-website/chrome-uaf-blink | ctf-website/techniques/09-cve/01-browser-sandbox-escape.md |
| `uc_hook_intr` | general, general/methodology | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `uc_hook_mem_unmapped` | general, general/methodology | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `udp` | general/protocol | general/techniques/protocol/01-unknown-protocol-reverse.md<br>general/techniques/protocol/02-protobuf-flatbuffers-reverse.md |
| `udp 流量洪泛 伪造源ip` | ctf-website | ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `ue4` | apk-reverse/native | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md<br>apk-reverse/techniques/02-native/02-pointer-chain-patterns.md<br>apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `unholydragon-n.exe 文件名序号` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/04-twinbasic-compressed-resource-recovery.md |
| `unicorn` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `unicorn 仿真` | general | general/methodology/01-headless-emulation-windows-android-handbook.md |
| `unidbg` | apk-reverse, apk-reverse/packer | apk-reverse/techniques/02-native/07-unidbg-native-emulation-pipeline.md<br>apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md |
| `union select 回显位` | ctf-website | ctf-website/techniques/24-database/01-sqli-fundamentals.md |
| `unknown protocol` | general/protocol | general/techniques/protocol/01-unknown-protocol-reverse.md<br>general/techniques/protocol/02-protobuf-flatbuffers-reverse.md |
| `unmap` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/06-modern-pe-unmapping-and-dump-reconstruction.md |
| `unmapper` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/06-modern-pe-unmapping-and-dump-reconstruction.md |
| `unpack` | pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `unsatisfiedlinkerror` | apk-reverse | apk-reverse/techniques/02-native/06-jni-register-natives-tracing.md |
| `unserialize` | ctf-website/deserialization | ctf-website/techniques/05-deserialization/deserialization.md |
| `unwebpack` | ctf-website/api-attacks | ctf-website/techniques/17-api-attacks/01-api-discovery-leak.md<br>ctf-website/techniques/17-api-attacks/02-api-key-leak.md |
| `upx` | apk-reverse/packer, pe-reverse/crypto-unpack | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `url` | apk-reverse/network, pe-reverse/ioc | apk-reverse/techniques/05-network/01-game-protocol-hook.md<br>apk-reverse/techniques/05-network/02-license-verification-bypass.md<br>pe-reverse/techniques/06-ioc-extraction/01-ioc-extraction.md |
| `url encoding sign` | ctf-website/signature-canonicalization | ctf-website/techniques/13-signature/04-canonicalization.md |
| `url parser` | ctf-website/ssrf | ctf-website/techniques/04-ssrf/ssrf.md |
| `use after free` | ctf-website/chrome-uaf-blink | ctf-website/techniques/09-cve/01-browser-sandbox-escape.md |
| `user-agent` | pe-reverse/ioc | pe-reverse/techniques/06-ioc-extraction/01-ioc-extraction.md |
| `user-agent spoof` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `user-agent: googlebot/2.1` | ctf-website | ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md |
| `user-mode bypass` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/07-direct-syscall.md |
| `user/update` | ctf-website/litellm-privesc | ctf-website/techniques/09-cve/05-litellm-privesc.md |
| `uuid predictable` | ctf-website/idor | ctf-website/techniques/14-idor/01-idor-enumeration.md<br>ctf-website/techniques/14-idor/02-bac-business-logic.md |
| `uuid shellcode` | pe-reverse/av-evasion | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `v8 math.random()` | general | general/techniques/crypto/03-prng-randomness-cracking.md |
| `valkey` | ctf-website/redis-valkey-restore-zipmap, ctf-website/valkey-resp-dos | ctf-website/techniques/09-cve/02-redis-zipmap-rce.md<br>ctf-website/techniques/11-dos/01-valkey-resp-dos.md |
| `vanguard` | general/cheating | general/techniques/cheating/01-memory-hacking.md<br>general/techniques/cheating/02-packet-interception.md<br>general/techniques/cheating/03-esp-wallhack-rendering.md |
| `vanguard vgk.sys` | general | general/techniques/cheating/04-anti-cheat-bypass.md |
| `variable override` | ctf-website/signature-implementation | ctf-website/techniques/13-signature/02-implementation.md |
| `varint` | general | general/techniques/protocol/02-protobuf-flatbuffers-reverse.md |
| `vary: user-agent 响应头` | ctf-website | ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md |
| `vb.timer / vb.textbox` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/04-twinbasic-compressed-resource-recovery.md |
| `vb6` | pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `veh` | pe-reverse | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `velocity` | ctf-website/ssti | ctf-website/techniques/03-injection/ssti.md |
| `verify` | apk-reverse/network | apk-reverse/techniques/05-network/01-game-protocol-hook.md<br>apk-reverse/techniques/05-network/02-license-verification-bypass.md |
| `verify sign` | ctf-website/signature | ctf-website/techniques/13-signature/00-overview.md<br>ctf-website/techniques/13-signature/01-algorithm.md<br>ctf-website/techniques/13-signature/02-implementation.md |
| `version conflict` | ctf-website/race-lost-update | ctf-website/techniques/12-payment/payment-race-lost-update.md |
| `version number` | ctf-website/race-lost-update | ctf-website/techniques/12-payment/payment-race-lost-update.md |
| `vertical privilege` | ctf-website/idor | ctf-website/techniques/14-idor/01-idor-enumeration.md<br>ctf-website/techniques/14-idor/02-bac-business-logic.md |
| `vet_description missing` | general | general/techniques/01-kernel/04-cifswitch-nss-privesc.md |
| `vhost` | ctf-website/host-header | ctf-website/techniques/02-auth/host-header.md |
| `view-source 完整正文` | ctf-website | ctf-website/techniques/23-paywall-bypass/04-content-extraction.md |
| `virtual address` | apk-reverse/native | apk-reverse/techniques/02-native/01-il2cpp-offset-discovery.md<br>apk-reverse/techniques/02-native/02-pointer-chain-patterns.md<br>apk-reverse/techniques/02-native/03-ue4-offset-hunting.md |
| `virtual currency` | ctf-website/payment-digital-goods | ctf-website/techniques/12-payment/payment-digital-goods.md |
| `virtualallocex` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/01-dll-injection.md |
| `virtualization` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `virtualprotect` | pe-reverse | pe-reverse/techniques/08-patch/01-code-patching.md |
| `vm bytecode` | pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `vm entry` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `vm 字节码` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `vm 字节码解密` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/10-nested-vm-matryoshka-reverse-and-defeat.md |
| `vmenter` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/07-modern-virtual-machine-devirtualization-mogvmp-llvm.md |
| `vmp` | apk-reverse, apk-reverse/packer, pe-reverse | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `vmp 3` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/07-modern-virtual-machine-devirtualization-mogvmp-llvm.md |
| `vmp0` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md |
| `vmp1` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md |
| `vmprotect` | apk-reverse, pe-reverse, pe-reverse/crypto-unpack | apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md<br>pe-reverse/techniques/04-dynamic-analysis/05-anti-debug-bypass.md<br>pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md |
| `vmprotectisdebuggerpresent` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/05-anti-debug-bypass.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md |
| `vmsplice` | ctf-website/page-cache-write | general/techniques/01-kernel/01-page-cache-write-family.md |
| `volley` | apk-reverse/network | apk-reverse/techniques/05-network/01-game-protocol-hook.md<br>apk-reverse/techniques/05-network/02-license-verification-bypass.md |
| `voucher leak` | ctf-website/payment-bounce-idor | ctf-website/techniques/12-payment/payment-email-bounce-idor.md |
| `vtable` | pe-reverse | pe-reverse/techniques/03-static-analysis/01-struct-reconstruction.md |
| `vtable scanning` | general | general/techniques/protocol/02-protobuf-flatbuffers-reverse.md |
| `vtable 间接调用` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `vtil` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `vtl` | pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `vulnerability` | ctf-website/cve | ctf-website/techniques/09-cve/cve-correlation-graph.md<br>ctf-website/techniques/09-cve/cve-workflow.md<br>ctf-website/techniques/09-cve/multi-cve-chain-playbook.md |
| `waf bypass` | ctf-website/cloudflare-bypass, ctf-website/database-attacks | ctf-website/techniques/01-recon/cloudflare-bypass.md<br>ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md |
| `waf bypass sql` | ctf-website/sqli | ctf-website/techniques/03-injection/sqli-nosqli.md |
| `waf 大小写双写注释绕过` | ctf-website | ctf-website/techniques/24-database/01-sqli-fundamentals.md |
| `wal 日志膨胀` | ctf-website | ctf-website/techniques/22-dos/13-database-dos.md |
| `wallhack` | general/cheating | general/techniques/cheating/01-memory-hacking.md<br>general/techniques/cheating/02-packet-interception.md<br>general/techniques/cheating/03-esp-wallhack-rendering.md |
| `wallkit` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `wappalyzer` | ctf-website/recon | ctf-website/techniques/01-recon/recon-routing.md<br>ctf-website/techniques/01-recon/version-fingerprinting.md |
| `warn_free_bad_obj` | ctf-website/slab-cross-cache | general/techniques/01-kernel/02-slab-cross-cache.md |
| `wasm` | ctf-website/js-runtime | ctf-website/techniques/07-client/js-runtime.md |
| `weak key` | ctf-website/signature-key | ctf-website/techniques/13-signature/03-key-attacks.md |
| `web cache` | ctf-website/cache-deception | ctf-website/techniques/08-infra/web-cache-deception.md |
| `web crypto` | ctf-website/web-crypto | ctf-website/techniques/07-client/web-crypto-abuse.md |
| `web.config 暴露` | ctf-website | ctf-website/techniques/24-database/04-config-exposure.md |
| `webcrypto` | ctf-website/js-runtime | ctf-website/techniques/07-client/js-runtime.md |
| `webgl 指纹` | ctf-website | ctf-website/techniques/27-js-reverse/02-browser-env-emulation-proxy-sandbox.md |
| `webhook` | ctf-website/payment | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/12-payment/payment-digital-goods.md |
| `webhook 回调慢速响应` | ctf-website | ctf-website/techniques/22-dos/10-api-abuse.md |
| `webpack` | ctf-website/js-runtime | ctf-website/techniques/07-client/js-runtime.md |
| `webpackchunk` | ctf-website | ctf-website/techniques/27-js-reverse/03-sourcemap-unpack-and-webpack-hijacking.md |
| `webpackjsonp` | ctf-website | ctf-website/techniques/27-js-reverse/03-sourcemap-unpack-and-webpack-hijacking.md |
| `websocket` | apk-reverse/network, ctf-website/websocket | apk-reverse/techniques/05-network/01-game-protocol-hook.md<br>apk-reverse/techniques/05-network/02-license-verification-bypass.md<br>ctf-website/techniques/07-client/websocket.md |
| `websocket dos` | ctf-website/dos | ctf-website/techniques/22-dos/01-application-layer-dos.md<br>ctf-website/techniques/22-dos/02-resource-exhaustion.md<br>ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `websocket 连接数飙升` | ctf-website | ctf-website/techniques/22-dos/01-application-layer-dos.md |
| `webview` | ctf-website/mobile-bridge | ctf-website/techniques/21-mobile-bridge/01-webview-attacks.md<br>ctf-website/techniques/21-mobile-bridge/02-cordova-reactnative.md |
| `wechat pay` | ctf-website/payment | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/12-payment/payment-digital-goods.md |
| `whatweb` | ctf-website/recon | ctf-website/techniques/01-recon/recon-routing.md<br>ctf-website/techniques/01-recon/version-fingerprinting.md |
| `while switch 状态机` | ctf-website | ctf-website/techniques/27-js-reverse/01-ast-deobfuscation-pipeline.md |
| `white-box` | general/crypto | general/techniques/crypto/01-algorithm-identification.md<br>general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `white-box aes` | general | general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `whm` | ctf-website/cpanel-caldav-traversal | ctf-website/techniques/09-cve/03-cpanel-caldav-traversal.md |
| `wildcard` | pe-reverse/triage | pe-reverse/techniques/01-triage/01-aob-signature-scan.md |
| `window is not defined` | ctf-website | ctf-website/techniques/27-js-reverse/02-browser-env-emulation-proxy-sandbox.md |
| `window.postmessage` | ctf-website/postmessage | ctf-website/techniques/07-client/postmessage.md |
| `winsock hook` | general, general/cheating | general/techniques/cheating/01-memory-hacking.md<br>general/techniques/cheating/02-packet-interception.md<br>general/techniques/cheating/03-esp-wallhack-rendering.md |
| `wire type decoding` | general | general/techniques/protocol/02-protobuf-flatbuffers-reverse.md |
| `wireshark` | general/protocol | general/techniques/protocol/01-unknown-protocol-reverse.md<br>general/techniques/protocol/02-protobuf-flatbuffers-reverse.md |
| `wkhtmltopdf` | ctf-website/file-attacks | ctf-website/techniques/06-file-attacks/file-upload-xxe-lfi.md |
| `wkwebview` | ctf-website/mobile-bridge | ctf-website/techniques/21-mobile-bridge/01-webview-attacks.md<br>ctf-website/techniques/21-mobile-bridge/02-cordova-reactnative.md |
| `wmi eventfilter` | pe-reverse | pe-reverse/techniques/06-ioc-extraction/02-persistence-startup-chain.md |
| `woocommerce` | ctf-website/payment-php | ctf-website/techniques/12-payment/payment-php.md |
| `wordpress` | ctf-website/payment-php | ctf-website/techniques/12-payment/payment-php.md |
| `workflow` | ctf-website/24h-loop-orchestration, ctf-website/ci-cd, general/methodology | ctf-website/techniques/00-workflow/24h-loop-orchestration.md<br>ctf-website/techniques/10-cloud/ci-cd-pipeline.md<br>ctf-website/techniques/10-cloud/github-actions-abuse-paths.md |
| `world-to-screen` | general | general/techniques/cheating/03-esp-wallhack-rendering.md |
| `write skew` | ctf-website/race-lost-update | ctf-website/techniques/12-payment/payment-race-lost-update.md |
| `write_file_base64` | general | general/methodology/02-remote-mcp-device-bridge-deployment.md |
| `writeprocessmemory` | pe-reverse, pe-reverse/dynamic-analysis | pe-reverse/techniques/04-dynamic-analysis/01-dll-injection.md<br>pe-reverse/techniques/04-dynamic-analysis/02-trampoline-detour.md<br>pe-reverse/techniques/04-dynamic-analysis/03-external-memory-rw.md |
| `ws` | ctf-website/websocket | ctf-website/techniques/07-client/websocket.md |
| `wsdl` | ctf-website/api-attacks | ctf-website/techniques/17-api-attacks/01-api-discovery-leak.md<br>ctf-website/techniques/17-api-attacks/02-api-key-leak.md |
| `wsj paywall` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `wss` | ctf-website/websocket | ctf-website/techniques/07-client/websocket.md |
| `x-cache` | ctf-website/cache-deception | ctf-website/techniques/08-infra/web-cache-deception.md |
| `x-cache: miss 命中率骤降` | ctf-website | ctf-website/techniques/22-dos/09-cache-cdn-dos.md |
| `x-forwarded-for` | ctf-website/rate-limit | ctf-website/techniques/16-rate-limit/01-rate-limit-bypass.md<br>ctf-website/techniques/16-rate-limit/02-brute-force-tactics.md |
| `x-forwarded-for 伪装` | ctf-website | ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md |
| `x-forwarded-for 轮换` | ctf-website | ctf-website/techniques/22-dos/10-api-abuse.md |
| `x-forwarded-host` | ctf-website/host-header | ctf-website/techniques/02-auth/host-header.md |
| `x-forwarded-host 缓存分片` | ctf-website | ctf-website/techniques/22-dos/09-cache-cdn-dos.md |
| `x509trustmanager` | apk-reverse | apk-reverse/techniques/05-network/03-tls-pinning-unpinning.md |
| `x64dbg` | pe-reverse/static-analysis | pe-reverse/techniques/03-static-analysis/01-struct-reconstruction.md<br>pe-reverse/techniques/03-static-analysis/02-disasm-jit-asm.md<br>pe-reverse/techniques/03-static-analysis/03-x64dbg-breakpoints.md |
| `xbyak` | pe-reverse, pe-reverse/static-analysis | pe-reverse/techniques/03-static-analysis/01-struct-reconstruction.md<br>pe-reverse/techniques/03-static-analysis/02-disasm-jit-asm.md<br>pe-reverse/techniques/03-static-analysis/03-x64dbg-breakpoints.md |
| `xml bomb` | ctf-website/dos | ctf-website/techniques/22-dos/01-application-layer-dos.md<br>ctf-website/techniques/22-dos/02-resource-exhaustion.md<br>ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `xml canonicalization` | ctf-website/saml, ctf-website/signature-canonicalization | ctf-website/techniques/02-auth/saml-attacks.md<br>ctf-website/techniques/13-signature/04-canonicalization.md |
| `xml entity expansion billion laughs` | ctf-website | ctf-website/techniques/22-dos/02-resource-exhaustion.md |
| `xml signature` | ctf-website/saml | ctf-website/techniques/02-auth/saml-attacks.md |
| `xml wrapping` | ctf-website/saml | ctf-website/techniques/02-auth/saml-attacks.md |
| `xor` | general/crypto | general/techniques/crypto/01-algorithm-identification.md<br>general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `xor key recovery` | general | general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `xorshift` | general/prng, pe-reverse | general/techniques/crypto/03-prng-randomness-cracking.md<br>pe-reverse/techniques/05-crypto-unpack/10-nested-vm-matryoshka-reverse-and-defeat.md |
| `xorshift128+ cracking` | general | general/techniques/crypto/03-prng-randomness-cracking.md |
| `xref 反查` | pe-reverse | pe-reverse/techniques/10-license-keygen/02-validation-function-location.md |
| `xs-leak` | ctf-website/csp-cors-advanced | ctf-website/techniques/18-cors-csp-advanced/01-csp-bypass.md<br>ctf-website/techniques/18-cors-csp-advanced/02-xs-leaks-browser-sidechannels.md |
| `xs-leaks` | ctf-website/csp-cors-advanced | ctf-website/techniques/18-cors-csp-advanced/01-csp-bypass.md<br>ctf-website/techniques/18-cors-csp-advanced/02-xs-leaks-browser-sidechannels.md |
| `xs-search` | ctf-website/csp-cors-advanced | ctf-website/techniques/18-cors-csp-advanced/01-csp-bypass.md<br>ctf-website/techniques/18-cors-csp-advanced/02-xs-leaks-browser-sidechannels.md |
| `xss` | ctf-website/xss | ctf-website/techniques/07-client/admin-bot-xss.md |
| `xxe` | ctf-website/file-attacks | ctf-website/techniques/06-file-attacks/file-upload-xxe-lfi.md |
| `yansongda` | ctf-website/payment-php | ctf-website/techniques/12-payment/payment-php.md |
| `yara` | pe-reverse/yara-sigma | pe-reverse/techniques/07-yara-sigma/01-yara-rule-writing.md |
| `yara rule` | pe-reverse | pe-reverse/techniques/07-yara-sigma/01-yara-rule-writing.md |
| `youpk` | apk-reverse, apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `ysoserial` | ctf-website/deserialization | ctf-website/techniques/05-deserialization/deserialization.md |
| `z3` | general | general/crypto/02-angr-symbolic-execution-solver.md |
| `z3 constraint solving` | general | general/techniques/crypto/02-custom-obfuscation-reverse.md |
| `zephr` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `zero price` | ctf-website/payment-bypass | ctf-website/techniques/12-payment/payment-bypass.md |
| `zerocopy` | ctf-website/pintheft-io-uring | general/techniques/01-kernel/05-pintheft-io-uring-page-cache.md |
| `zip bomb` | ctf-website/dos | ctf-website/techniques/22-dos/01-application-layer-dos.md<br>ctf-website/techniques/22-dos/02-resource-exhaustion.md<br>ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `zip bomb 42.zip` | ctf-website | ctf-website/techniques/22-dos/02-resource-exhaustion.md |
| `zip slip` | ctf-website/file-attacks | ctf-website/techniques/06-file-attacks/file-upload-xxe-lfi.md |
| `zipmap` | ctf-website/redis-valkey-restore-zipmap | ctf-website/techniques/09-cve/02-redis-zipmap-rce.md |
| `zlib 78 9c 78 01 78 5e` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/05-high-entropy-compression-vs-crypto-routing.md |
| `zstd magic 28 b5 2f fd` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/05-high-entropy-compression-vs-crypto-routing.md |
| `zydis` | pe-reverse, pe-reverse/static-analysis | pe-reverse/techniques/03-static-analysis/01-struct-reconstruction.md<br>pe-reverse/techniques/03-static-analysis/02-disasm-jit-asm.md<br>pe-reverse/techniques/03-static-analysis/03-x64dbg-breakpoints.md |
| `不是有效的 win32 应用程序` | pe-reverse | pe-reverse/techniques/10-license-keygen/08-cross-version-aob-migration.md |
| `不透明谓词` | pe-reverse | pe-reverse/techniques/03-static-analysis/07-ida-microcode-mba-deobfuscation-d810.md |
| `乐观锁` | ctf-website/race-lost-update | ctf-website/techniques/12-payment/payment-race-lost-update.md |
| `二阶注入` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `二阶注入 second-order sqli` | ctf-website | ctf-website/techniques/24-database/02-sqli-advanced.md |
| `云元数据 169.254.169.254` | ctf-website | ctf-website/techniques/22-dos/12-ssrf-dos.md |
| `云校验` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `云端授权` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `交互式样本` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `付费墙` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `付费订阅` | ctf-website/paywall-bypass | ctf-website/techniques/23-paywall-bypass/01-paywall-detection-bypass.md<br>ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md<br>ctf-website/techniques/23-paywall-bypass/03-network-rule-blocking.md |
| `代币` | ctf-website/payment-digital-goods | ctf-website/techniques/12-payment/payment-digital-goods.md |
| `代码位移` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `代码修改` | pe-reverse | pe-reverse/techniques/08-patch/01-code-patching.md |
| `价格篡改` | ctf-website/mass-assignment | ctf-website/techniques/15-mass-assignment/01-mass-assignment.md<br>ctf-website/techniques/15-mass-assignment/02-parameter-tampering.md |
| `优惠券` | ctf-website/payment | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/12-payment/payment-digital-goods.md |
| `优惠券叠加` | ctf-website/mass-assignment | ctf-website/techniques/15-mass-assignment/01-mass-assignment.md<br>ctf-website/techniques/15-mass-assignment/02-parameter-tampering.md |
| `位域` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `余额` | ctf-website/payment | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/12-payment/payment-digital-goods.md |
| `余额绕过` | ctf-website/race-lost-update | ctf-website/techniques/12-payment/payment-race-lost-update.md |
| `作弊` | general/cheating | general/techniques/cheating/01-memory-hacking.md<br>general/techniques/cheating/02-packet-interception.md<br>general/techniques/cheating/03-esp-wallhack-rendering.md |
| `假数据 占位符 asd123` | ctf-website | ctf-website/techniques/24-database/07-data-cleaning.md |
| `假阳性排除` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `偏移推断` | pe-reverse | pe-reverse/techniques/03-static-analysis/01-struct-reconstruction.md |
| `充值` | ctf-website/payment | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/12-payment/payment-digital-goods.md |
| `免杀` | pe-reverse | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `免杀loader` | pe-reverse/av-evasion | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `全流程` | ctf-website/24h-loop-orchestration | ctf-website/techniques/00-workflow/24h-loop-orchestration.md<br>ctf-website/techniques/attack-network.md |
| `全网图` | ctf-website/attack-network | ctf-website/techniques/attack-network.md |
| `公钥替换` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `共同稳定区` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `内存保护` | pe-reverse/av-evasion | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `内存标志位` | pe-reverse | pe-reverse/techniques/10-license-keygen/05-keygen-frida-verification-loop.md |
| `内存读写` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/03-external-memory-rw.md |
| `内嵌公钥` | pe-reverse | pe-reverse/techniques/10-license-keygen/04-signature-chain-pubkey-swap.md |
| `内联汇编` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/04-naked-function-hook.md |
| `内联注释 /*!50000select*/` | ctf-website | ctf-website/techniques/24-database/02-sqli-advanced.md |
| `内购` | ctf-website/payment-digital-goods | ctf-website/techniques/12-payment/payment-digital-goods.md |
| `内部服务洪泛` | ctf-website | ctf-website/techniques/22-dos/12-ssrf-dos.md |
| `决策树` | general/methodology | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `冷启动 cold_start_count` | ctf-website | ctf-website/techniques/22-dos/11-cloud-container-dos.md |
| `冷启动重算` | pe-reverse | pe-reverse/techniques/10-license-keygen/07-self-referencing-signature-convergence.md |
| `凭证喷洒` | ctf-website/rate-limit | ctf-website/techniques/16-rate-limit/01-rate-limit-bypass.md<br>ctf-website/techniques/16-rate-limit/02-brute-force-tactics.md |
| `函数劫持` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/02-trampoline-detour.md<br>pe-reverse/techniques/08-patch/01-code-patching.md |
| `函数指针` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `分叉` | ctf-website/attack-network | ctf-website/techniques/attack-network.md |
| `分发形态` | pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `分块传输 transfer-encoding chunked` | ctf-website | ctf-website/techniques/24-database/02-sqli-advanced.md |
| `分页 page > 10000` | ctf-website | ctf-website/techniques/22-dos/10-api-abuse.md |
| `前端源码泄露` | ctf-website | ctf-website/techniques/27-js-reverse/03-sourcemap-unpack-and-webpack-hijacking.md |
| `前缀聚类 2-3 字符` | ctf-website | ctf-website/techniques/24-database/07-data-cleaning.md |
| `加固` | apk-reverse, apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `加密字符串` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `加速` | general/cheating | general/techniques/cheating/01-memory-hacking.md<br>general/techniques/cheating/02-packet-interception.md<br>general/techniques/cheating/03-esp-wallhack-rendering.md |
| `升级` | ctf-website/payment-subscription | ctf-website/techniques/12-payment/payment-subscription.md |
| `半开连接 syn_rcvd close_wait` | ctf-website | ctf-website/techniques/22-dos/01-application-layer-dos.md |
| `单字节断言` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/10-nested-vm-matryoshka-reverse-and-defeat.md |
| `单请求响应时间异常增长 50ms→30s` | ctf-website | ctf-website/techniques/22-dos/04-redos.md |
| `占位 key` | pe-reverse | pe-reverse/techniques/10-license-keygen/07-self-referencing-signature-convergence.md |
| `卡密` | ctf-website/database-attacks, ctf-website/payment-digital-goods | ctf-website/techniques/12-payment/payment-digital-goods.md<br>ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md |
| `卡密泄露` | ctf-website/payment-bounce-idor | ctf-website/techniques/12-payment/payment-email-bounce-idor.md |
| `卡巴斯基绕过` | pe-reverse/av-evasion | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `卡盟` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `去虚拟化` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `参数排序` | ctf-website/signature-canonicalization | ctf-website/techniques/13-signature/04-canonicalization.md |
| `双态唯一性` | pe-reverse | pe-reverse/techniques/10-license-keygen/10-multiversion-signature-narrowing.md |
| `双态特征码` | pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `双机制` | pe-reverse | pe-reverse/techniques/10-license-keygen/07-self-referencing-signature-convergence.md |
| `双进程` | apk-reverse | apk-reverse/techniques/07-packer/05-vmp-anti-debug-bypass.md |
| `反射攻击` | ctf-website/dos | ctf-website/techniques/22-dos/01-application-layer-dos.md<br>ctf-website/techniques/22-dos/02-resource-exhaustion.md<br>ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `反汇编` | pe-reverse, pe-reverse/static-analysis | pe-reverse/techniques/03-static-analysis/01-struct-reconstruction.md<br>pe-reverse/techniques/03-static-analysis/02-disasm-jit-asm.md<br>pe-reverse/techniques/03-static-analysis/03-x64dbg-breakpoints.md |
| `反沙箱` | pe-reverse/av-evasion | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `反调试` | apk-reverse, apk-reverse/packer, pe-reverse | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `反调试早期触发` | pe-reverse | pe-reverse/techniques/02-pe-structure/02-tls-callback-analysis.md |
| `反调试陷阱` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `发卡` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `变种检测` | pe-reverse | pe-reverse/techniques/07-yara-sigma/01-yara-rule-writing.md |
| `命令注入` | windows | windows/techniques/notepadpp-config-injection.md |
| `命名` | general/methodology | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `哈希拼接` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `响应体大小 googlebot > chrome` | ctf-website | ctf-website/techniques/23-paywall-bypass/02-http-header-manipulation.md |
| `哪吒` | ctf-website/nezha-path-traversal | ctf-website/techniques/09-cve/04-nezha-path-traversal-jwt.md |
| `回滚点错版` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `在线激活` | pe-reverse | pe-reverse/techniques/10-license-keygen/06-cloud-license-frida-hook.md |
| `填充漂移` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `壳` | apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `壳行为` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md |
| `备份` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `备份文件 .sql .dump` | ctf-website | ctf-website/techniques/24-database/00-overview.md |
| `多个网站` | ctf-website/24h-loop-orchestration | ctf-website/techniques/00-workflow/24h-loop-orchestration.md<br>ctf-website/techniques/attack-network.md |
| `多入口` | ctf-website/attack-network | ctf-website/techniques/attack-network.md |
| `多层 vm` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/10-nested-vm-matryoshka-reverse-and-defeat.md |
| `多版本特征码` | pe-reverse | pe-reverse/techniques/10-license-keygen/08-cross-version-aob-migration.md<br>pe-reverse/techniques/10-license-keygen/10-multiversion-signature-narrowing.md |
| `多版本特征码收窄` | pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `多目标` | ctf-website/24h-loop-orchestration | ctf-website/techniques/00-workflow/24h-loop-orchestration.md<br>ctf-website/techniques/attack-network.md |
| `大数组移位` | ctf-website | ctf-website/techniques/27-js-reverse/01-ast-deobfuscation-pipeline.md |
| `大量 clienthello 无后续` | ctf-website | ctf-website/techniques/22-dos/08-tls-exhaustion.md |
| `套娃 vm` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/10-nested-vm-matryoshka-reverse-and-defeat.md |
| `如何判断是不是 vm` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `威胁情报` | pe-reverse | pe-reverse/techniques/06-ioc-extraction/01-ioc-extraction.md |
| `子域名接管` | ctf-website/dns-email | ctf-website/techniques/19-dns-email/01-subdomain-takeover.md<br>ctf-website/techniques/19-dns-email/02-email-spoofing.md |
| `字形签名` | pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `字符串锚定` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `字符集映射` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `字节替换` | pe-reverse | pe-reverse/techniques/08-patch/01-code-patching.md |
| `定期付款` | ctf-website/payment-subscription | ctf-website/techniques/12-payment/payment-subscription.md |
| `实时分析` | pe-reverse | pe-reverse/techniques/03-static-analysis/04-reclass-reconstruction.md |
| `容器 pid namespace 耗尽` | ctf-website | ctf-website/techniques/22-dos/11-cloud-container-dos.md |
| `宽字节` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `宽字节 %bf%27 gbk` | ctf-website | ctf-website/techniques/24-database/01-sqli-fundamentals.md |
| `寄存器保存` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/04-naked-function-hook.md |
| `密钥对` | pe-reverse | pe-reverse/techniques/10-license-keygen/04-signature-chain-pubkey-swap.md |
| `密钥泄露` | ctf-website/signature-key | ctf-website/techniques/13-signature/03-key-attacks.md |
| `对照组实验` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `对话框定位` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `对账` | ctf-website/payment-callback | ctf-website/techniques/12-payment/payment-callback-async.md |
| `对齐填充` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `导入表` | pe-reverse | pe-reverse/techniques/02-pe-structure/01-pe-header-parsing.md |
| `封包` | apk-reverse/network, general/cheating | apk-reverse/techniques/05-network/01-game-protocol-hook.md<br>apk-reverse/techniques/05-network/02-license-verification-bypass.md<br>general/techniques/cheating/01-memory-hacking.md |
| `局部不变性` | pe-reverse | pe-reverse/techniques/10-license-keygen/07-self-referencing-signature-convergence.md |
| `属性注入` | ctf-website/mass-assignment | ctf-website/techniques/15-mass-assignment/01-mass-assignment.md<br>ctf-website/techniques/15-mass-assignment/02-parameter-tampering.md |
| `嵌套 vm` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `嵌套虚拟机` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/10-nested-vm-matryoshka-reverse-and-defeat.md |
| `嵌套量词 (a+)+` | ctf-website | ctf-website/techniques/22-dos/04-redos.md |
| `工作流` | general/methodology | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `带壳样本仿真` | general, general/methodology | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `常量池位移` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `幂等` | ctf-website/payment-callback | ctf-website/techniques/12-payment/payment-callback-async.md |
| `并发扣费` | ctf-website/race-lost-update | ctf-website/techniques/12-payment/payment-race-lost-update.md |
| `异或常量` | pe-reverse | pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `异步支付` | ctf-website/payment-callback | ctf-website/techniques/12-payment/payment-callback-async.md |
| `弱密钥` | ctf-website/signature-key | ctf-website/techniques/13-signature/03-key-attacks.md |
| `弹窗触发条件` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `循环移位` | pe-reverse | pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `微代码反混淆` | pe-reverse | pe-reverse/techniques/03-static-analysis/07-ida-microcode-mba-deobfuscation-d810.md |
| `微验` | apk-reverse/network | apk-reverse/techniques/05-network/01-game-protocol-hook.md<br>apk-reverse/techniques/05-network/02-license-verification-bypass.md |
| `忽略反调试陷阱` | general, general/methodology | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `慢查询 pg_stat_activity` | ctf-website | ctf-website/techniques/22-dos/13-database-dos.md |
| `手动映射` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/06-manual-map-injection.md |
| `批量操作放大 bulk api` | ctf-website | ctf-website/techniques/22-dos/10-api-abuse.md |
| `批量赋值` | ctf-website/mass-assignment | ctf-website/techniques/15-mass-assignment/01-mass-assignment.md<br>ctf-website/techniques/15-mass-assignment/02-parameter-tampering.md |
| `抓包` | general/protocol | general/techniques/protocol/01-unknown-protocol-reverse.md<br>general/techniques/protocol/02-protobuf-flatbuffers-reverse.md |
| `抓取回填` | pe-reverse | pe-reverse/techniques/10-license-keygen/07-self-referencing-signature-convergence.md |
| `拒绝服务` | ctf-website/dos | ctf-website/techniques/22-dos/01-application-layer-dos.md<br>ctf-website/techniques/22-dos/02-resource-exhaustion.md<br>ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `指针链` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/03-external-memory-rw.md |
| `按比例` | ctf-website/payment-subscription | ctf-website/techniques/12-payment/payment-subscription.md |
| `授权证书` | pe-reverse | pe-reverse/techniques/10-license-keygen/06-cloud-license-frida-hook.md |
| `控制流平坦化` | ctf-website | ctf-website/techniques/27-js-reverse/01-ast-deobfuscation-pipeline.md |
| `搜索宽泛查询 q=*` | ctf-website | ctf-website/techniques/22-dos/10-api-abuse.md |
| `支付` | ctf-website/payment | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/12-payment/payment-digital-goods.md |
| `支付回调` | ctf-website/payment-callback | ctf-website/techniques/12-payment/payment-callback-async.md |
| `支付回调签名缺失` | ctf-website | ctf-website/techniques/24-database/06-card-platform.md |
| `支付绕过` | ctf-website/payment-bypass | ctf-website/techniques/12-payment/payment-bypass.md |
| `收据` | ctf-website/payment-digital-goods | ctf-website/techniques/12-payment/payment-digital-goods.md |
| `攻击路径` | ctf-website/attack-network | ctf-website/techniques/attack-network.md |
| `放大攻击` | ctf-website/dos | ctf-website/techniques/22-dos/01-application-layer-dos.md<br>ctf-website/techniques/22-dos/02-resource-exhaustion.md<br>ctf-website/techniques/22-dos/03-amplification-drdos.md |
| `效率` | general/methodology | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `数据库` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `数据库竞态` | ctf-website/race-lost-update | ctf-website/techniques/12-payment/payment-race-lost-update.md |
| `数据段填充漂移` | pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `数据段漂移` | pe-reverse | pe-reverse/techniques/10-license-keygen/10-multiversion-signature-narrowing.md |
| `数据行 分隔符行 标记行` | ctf-website | ctf-website/techniques/24-database/07-data-cleaning.md |
| `文件上传 inode 耗尽` | ctf-website | ctf-website/techniques/22-dos/10-api-abuse.md |
| `文件描述符耗尽 fd exhaustion` | ctf-website | ctf-website/techniques/22-dos/02-resource-exhaustion.md |
| `断点策略` | pe-reverse | pe-reverse/techniques/03-static-analysis/03-x64dbg-breakpoints.md |
| `方法论` | general/methodology | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `方法论通用性` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `无人值守` | ctf-website/24h-loop-orchestration | ctf-website/techniques/00-workflow/24h-loop-orchestration.md<br>ctf-website/techniques/attack-network.md |
| `无条件截断` | pe-reverse | pe-reverse/techniques/10-license-keygen/08-cross-version-aob-migration.md |
| `无模拟器运行 so` | general | general/methodology/01-headless-emulation-windows-android-handbook.md |
| `无痕注入` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/06-manual-map-injection.md |
| `无真实设备逆向` | general | general/methodology/01-headless-emulation-windows-android-handbook.md |
| `无真机` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `无真机逆向` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/10-nested-vm-matryoshka-reverse-and-defeat.md |
| `日志断点` | pe-reverse | pe-reverse/techniques/03-static-analysis/03-x64dbg-breakpoints.md |
| `时间检测` | apk-reverse | apk-reverse/techniques/07-packer/05-vmp-anti-debug-bypass.md |
| `时间线` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/08-procmon-patterns.md |
| `暴力破解` | ctf-website/rate-limit | ctf-website/techniques/16-rate-limit/01-rate-limit-bypass.md<br>ctf-website/techniques/16-rate-limit/02-brute-force-tactics.md |
| `替换验证` | pe-reverse | pe-reverse/techniques/10-license-keygen/05-keygen-frida-verification-loop.md |
| `最佳实践` | general/methodology | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `最小开销` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/04-naked-function-hook.md |
| `服务端校验` | pe-reverse | pe-reverse/techniques/10-license-keygen/06-cloud-license-frida-hook.md |
| `未知加密流` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/05-high-entropy-compression-vs-crypto-routing.md |
| `机器码生成` | pe-reverse | pe-reverse/techniques/03-static-analysis/02-disasm-jit-asm.md |
| `杀软绕过` | pe-reverse/av-evasion | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `极验` | ctf-website/captcha-bypass | ctf-website/techniques/01-recon/captcha-bypass.md |
| `校验串` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `校验函数` | pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `校验函数定位` | pe-reverse | pe-reverse/techniques/10-license-keygen/02-validation-function-location.md |
| `样本分类` | pe-reverse | pe-reverse/techniques/07-yara-sigma/01-yara-rule-writing.md |
| `模式匹配` | pe-reverse | pe-reverse/techniques/01-triage/01-aob-signature-scan.md |
| `模糊匹配误命中` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `正则回溯爆炸 backtracking` | ctf-website | ctf-website/techniques/22-dos/04-redos.md |
| `正则表达式拒绝服务` | ctf-website | ctf-website/techniques/22-dos/04-redos.md |
| `死锁 deadlock 回滚` | ctf-website | ctf-website/techniques/22-dos/13-database-dos.md |
| `汇编` | pe-reverse/static-analysis | pe-reverse/techniques/03-static-analysis/01-struct-reconstruction.md<br>pe-reverse/techniques/03-static-analysis/02-disasm-jit-asm.md<br>pe-reverse/techniques/03-static-analysis/03-x64dbg-breakpoints.md |
| `汉明距离极小但位置错误` | pe-reverse | pe-reverse/techniques/10-license-keygen/10-multiversion-signature-narrowing.md |
| `汉明距离误判` | pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `注入` | apk-reverse/dynamic-frida, ctf-website/database-attacks | apk-reverse/techniques/06-dynamic/01-memory-rw-hook.md<br>apk-reverse/techniques/06-dynamic/02-overlay-rendering-hook.md<br>apk-reverse/techniques/06-dynamic/03-touch-input-hook.md |
| `注册机` | pe-reverse | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md |
| `注册状态位` | pe-reverse | pe-reverse/techniques/10-license-keygen/05-keygen-frida-verification-loop.md |
| `注册码` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `注册码校验函数` | pe-reverse | pe-reverse/techniques/10-license-keygen/02-validation-function-location.md |
| `注册码生成` | pe-reverse | pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `注册表值名` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `注册表授权` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `混淆` | apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `混淆解密` | pe-reverse | pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `清单` | general/methodology | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `源码泄露` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `源站` | ctf-website/cloudflare-bypass | ctf-website/techniques/01-recon/cloudflare-bypass.md |
| `源站 ip 暴露 dns 历史` | ctf-website | ctf-website/techniques/22-dos/09-cache-cdn-dos.md |
| `滑动汉明距离` | pe-reverse | pe-reverse/techniques/10-license-keygen/10-multiversion-signature-narrowing.md |
| `滑块` | ctf-website/captcha-bypass | ctf-website/techniques/01-recon/captcha-bypass.md |
| `激活按钮回调` | pe-reverse | pe-reverse/techniques/10-license-keygen/02-validation-function-location.md |
| `激活码` | ctf-website/payment-digital-goods, pe-reverse, pe-reverse/license-keygen | ctf-website/techniques/12-payment/payment-digital-goods.md<br>pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md |
| `火绒绕过` | pe-reverse/av-evasion | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `特征提取` | pe-reverse | pe-reverse/techniques/07-yara-sigma/01-yara-rule-writing.md |
| `特征码` | pe-reverse/license-keygen, pe-reverse/triage | pe-reverse/techniques/01-triage/01-aob-signature-scan.md<br>pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md |
| `特征码唯一性` | pe-reverse | pe-reverse/techniques/10-license-keygen/10-multiversion-signature-narrowing.md |
| `特征码扫描` | pe-reverse | pe-reverse/techniques/01-triage/01-aob-signature-scan.md |
| `特征码收窄` | pe-reverse | pe-reverse/techniques/10-license-keygen/10-multiversion-signature-narrowing.md |
| `特征码迁移` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `状态伪造` | pe-reverse | pe-reverse/techniques/10-license-keygen/06-cloud-license-frida-hook.md |
| `状态文件` | pe-reverse | pe-reverse/techniques/10-license-keygen/06-cloud-license-frida-hook.md |
| `状态爆炸` | general | general/crypto/02-angr-symbolic-execution-solver.md |
| `环境依赖过强` | general | general/methodology/01-headless-emulation-windows-android-handbook.md |
| `环境链过长` | general/methodology | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `盲注` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `相对偏移表` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `真机部署` | general | general/methodology/02-remote-mcp-device-bridge-deployment.md |
| `硬件指纹` | pe-reverse | pe-reverse/techniques/10-license-keygen/05-keygen-frida-verification-loop.md |
| `硬编码偏移失效` | pe-reverse | pe-reverse/techniques/10-license-keygen/08-cross-version-aob-migration.md |
| `礼品卡` | ctf-website/payment-digital-goods | ctf-website/techniques/12-payment/payment-digital-goods.md |
| `积分` | ctf-website/payment-digital-goods | ctf-website/techniques/12-payment/payment-digital-goods.md |
| `空签名` | ctf-website/signature-algorithm | ctf-website/techniques/13-signature/01-algorithm.md |
| `竞争条件` | ctf-website/race-lost-update | ctf-website/techniques/12-payment/payment-race-lost-update.md |
| `笔记` | general/methodology | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `签名` | apk-reverse/patch-repack, ctf-website/signature | apk-reverse/techniques/08-patch-repack/01-so-injection-repack.md<br>ctf-website/techniques/13-signature/00-overview.md<br>ctf-website/techniques/13-signature/01-algorithm.md |
| `签名伪造` | ctf-website/signature | ctf-website/techniques/13-signature/00-overview.md<br>ctf-website/techniques/13-signature/01-algorithm.md<br>ctf-website/techniques/13-signature/02-implementation.md |
| `签名切片` | pe-reverse | pe-reverse/techniques/10-license-keygen/07-self-referencing-signature-convergence.md |
| `签名嵌入` | pe-reverse | pe-reverse/techniques/10-license-keygen/07-self-referencing-signature-convergence.md |
| `签名绕过` | ctf-website/payment-callback | ctf-website/techniques/12-payment/payment-callback-async.md |
| `签名链` | pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `算法降级` | ctf-website/signature-algorithm | ctf-website/techniques/13-signature/01-algorithm.md |
| `类型推断` | pe-reverse | pe-reverse/techniques/03-static-analysis/04-reclass-reconstruction.md |
| `精确锚点定位` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `系统调用` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/07-direct-syscall.md |
| `约束求解` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/10-nested-vm-matryoshka-reverse-and-defeat.md |
| `线程池饥饿 thread pool starvation` | ctf-website | ctf-website/techniques/22-dos/02-resource-exhaustion.md |
| `组织` | general/methodology | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `结构体重建` | pe-reverse | pe-reverse/techniques/03-static-analysis/01-struct-reconstruction.md<br>pe-reverse/techniques/03-static-analysis/04-reclass-reconstruction.md |
| `结算` | ctf-website/payment-callback | ctf-website/techniques/12-payment/payment-callback-async.md |
| `绕过` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/05-anti-debug-bypass.md |
| `绕过 hook` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/07-direct-syscall.md |
| `续费` | ctf-website/payment-subscription | ctf-website/techniques/12-payment/payment-subscription.md |
| `网络空间搜索引擎` | ctf-website/fofa | ctf-website/techniques/01-recon/fofa-hunting.md |
| `网络空间测绘` | ctf-website/fofa | ctf-website/techniques/01-recon/fofa-hunting.md |
| `置信度分级 确认 高 中 低` | ctf-website | ctf-website/techniques/24-database/07-data-cleaning.md |
| `脱壳` | apk-reverse, pe-reverse, pe-reverse/crypto-unpack | apk-reverse/techniques/07-packer/04-vmp-dump-trace-recovery.md<br>pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md |
| `脱库` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `自动映射缺失页` | general, general/methodology | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `自动续费` | ctf-website/payment-subscription | ctf-website/techniques/12-payment/payment-subscription.md |
| `自引用签名` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `自愈式仿真` | general, general/methodology, pe-reverse | general/methodology/01-headless-emulation-windows-android-handbook.md<br>general/methodology/02-remote-mcp-device-bridge-deployment.md<br>general/techniques/methodology/01-reverse-checklist-first-30-min.md |
| `自我复制` | pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `自研 vm` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `自签名 license` | pe-reverse | pe-reverse/techniques/10-license-keygen/04-signature-chain-pubkey-swap.md |
| `自解压` | apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `节区` | pe-reverse/pe-structure | pe-reverse/techniques/02-pe-structure/01-pe-header-parsing.md |
| `节区遍历` | pe-reverse | pe-reverse/techniques/02-pe-structure/01-pe-header-parsing.md |
| `花指令` | pe-reverse | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `虚拟化` | apk-reverse, apk-reverse/packer, pe-reverse | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `虚拟商品` | ctf-website/payment-digital-goods | ctf-website/techniques/12-payment/payment-digital-goods.md |
| `虚拟栈` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/07-modern-virtual-machine-devirtualization-mogvmp-llvm.md |
| `虚拟货币` | ctf-website/payment-digital-goods | ctf-website/techniques/12-payment/payment-digital-goods.md |
| `行为监控` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/08-procmon-patterns.md |
| `行锁等待 pg_locks` | ctf-website | ctf-website/techniques/22-dos/13-database-dos.md |
| `补环境` | ctf-website | ctf-website/techniques/27-js-reverse/02-browser-env-emulation-proxy-sandbox.md |
| `被动收集` | ctf-website/fofa | ctf-website/techniques/01-recon/fofa-hunting.md |
| `规范化` | ctf-website/signature-canonicalization | ctf-website/techniques/13-signature/04-canonicalization.md |
| `解映射` | pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `解释器` | apk-reverse, apk-reverse/packer | apk-reverse/techniques/07-packer/01-obfuscation-detection.md<br>apk-reverse/techniques/07-packer/02-self-extracting-payload.md<br>apk-reverse/techniques/07-packer/03-vmp-dex2c-detection.md |
| `计数器归一化 十六进制` | ctf-website | ctf-website/techniques/24-database/07-data-cleaning.md |
| `计量计费` | ctf-website/payment-subscription | ctf-website/techniques/12-payment/payment-subscription.md |
| `订单` | ctf-website/payment | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/12-payment/payment-digital-goods.md |
| `订单越权` | ctf-website/payment-bounce-idor | ctf-website/techniques/12-payment/payment-email-bounce-idor.md |
| `订阅` | ctf-website/payment-subscription | ctf-website/techniques/12-payment/payment-subscription.md |
| `证书链验证 cpu 高` | ctf-website | ctf-website/techniques/22-dos/08-tls-exhaustion.md |
| `试用` | ctf-website/payment-subscription | ctf-website/techniques/12-payment/payment-subscription.md |
| `试用重置` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `调用栈回溯` | pe-reverse | pe-reverse/techniques/10-license-keygen/02-validation-function-location.md |
| `调试器` | pe-reverse | pe-reverse/techniques/03-static-analysis/03-x64dbg-breakpoints.md |
| `资产测绘` | ctf-website/fofa | ctf-website/techniques/01-recon/fofa-hunting.md |
| `越权` | ctf-website/idor | ctf-website/techniques/14-idor/01-idor-enumeration.md<br>ctf-website/techniques/14-idor/02-bac-business-logic.md |
| `跨版本` | pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `跨版本补丁` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `跨版本迁移翻车` | pe-reverse | pe-reverse/techniques/10-license-keygen/10-multiversion-signature-narrowing.md |
| `跨进程` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/03-external-memory-rw.md |
| `跳板` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/02-trampoline-detour.md |
| `过滤规则` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/08-procmon-patterns.md |
| `运行时 vm 探测` | pe-reverse, pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `运行时定位` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `近邻偏移` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `进程内替换` | pe-reverse | pe-reverse/techniques/10-license-keygen/05-keygen-frida-verification-loop.md |
| `进程枚举` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/01-dll-injection.md |
| `进程注入免杀` | pe-reverse/av-evasion | pe-reverse/techniques/09-av-evasion/01-ai-powered-evasion.md |
| `远程mcp` | general | general/methodology/02-remote-mcp-device-bridge-deployment.md |
| `远程线程` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/01-dll-injection.md |
| `连接字符串` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `连接字符串泄露 .env` | ctf-website | ctf-website/techniques/24-database/00-overview.md |
| `连接池满 max_connections` | ctf-website | ctf-website/techniques/22-dos/02-resource-exhaustion.md |
| `迭代收敛` | pe-reverse | pe-reverse/techniques/10-license-keygen/07-self-referencing-signature-convergence.md |
| `退信` | ctf-website/payment-bounce-idor | ctf-website/techniques/12-payment/payment-email-bounce-idor.md |
| `退款` | ctf-website/payment | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/12-payment/payment-digital-goods.md |
| `透视` | general/cheating | general/techniques/cheating/01-memory-hacking.md<br>general/techniques/cheating/02-packet-interception.md<br>general/techniques/cheating/03-esp-wallhack-rendering.md |
| `递归 cte 炸弹` | ctf-website | ctf-website/techniques/22-dos/13-database-dos.md |
| `递归 ssrf self-call` | ctf-website | ctf-website/techniques/22-dos/12-ssrf-dos.md |
| `递归器 cache miss rate 100%` | ctf-website | ctf-website/techniques/22-dos/07-dns-dos.md |
| `逗号表达式` | ctf-website | ctf-website/techniques/27-js-reverse/01-ast-deobfuscation-pipeline.md |
| `速率限制` | ctf-website/rate-limit | ctf-website/techniques/16-rate-limit/01-rate-limit-bypass.md<br>ctf-website/techniques/16-rate-limit/02-brute-force-tactics.md |
| `配置写入激活` | pe-reverse | pe-reverse/techniques/10-license-keygen/05-keygen-frida-verification-loop.md |
| `配置污染` | windows | windows/techniques/notepadpp-config-injection.md |
| `配置注入` | ctf-website/notepadpp-config-injection | windows/techniques/notepadpp-config-injection.md |
| `重叠交替 a|aa` | ctf-website | ctf-website/techniques/22-dos/04-redos.md |
| `重启保持` | pe-reverse | pe-reverse/techniques/10-license-keygen/05-keygen-frida-verification-loop.md |
| `重复消费` | ctf-website/race-lost-update | ctf-website/techniques/12-payment/payment-race-lost-update.md |
| `重定位` | pe-reverse | pe-reverse/techniques/04-dynamic-analysis/06-manual-map-injection.md |
| `重定位指针` | pe-reverse | pe-reverse/techniques/10-license-keygen/08-cross-version-aob-migration.md |
| `重打包` | apk-reverse/patch-repack | apk-reverse/techniques/08-patch-repack/01-so-injection-repack.md |
| `重放` | ctf-website/signature-replay | ctf-website/techniques/13-signature/06-replay-nonce.md |
| `重编译` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `金额` | ctf-website/payment | ctf-website/techniques/12-payment/payment-bypass.md<br>ctf-website/techniques/12-payment/payment-callback-async.md<br>ctf-website/techniques/12-payment/payment-digital-goods.md |
| `锚点映射 ground truth` | ctf-website | ctf-website/techniques/24-database/07-data-cleaning.md |
| `长度扩展` | ctf-website/signature-length-extension | ctf-website/techniques/13-signature/05-length-extension.md |
| `间接分发` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/09-runtime-vm-detection-generic.md |
| `陈旧备份` | pe-reverse | pe-reverse/techniques/10-license-keygen/08-cross-version-aob-migration.md |
| `降级` | ctf-website/payment-subscription | ctf-website/techniques/12-payment/payment-subscription.md |
| `随机子域 water torture` | ctf-website | ctf-website/techniques/22-dos/07-dns-dos.md |
| `零元购` | ctf-website/payment-bypass | ctf-website/techniques/12-payment/payment-bypass.md |
| `零回归断言` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `静态 xref 断裂` | pe-reverse, pe-reverse/license-keygen | pe-reverse/techniques/10-license-keygen/01-license-mechanism-classification.md<br>pe-reverse/techniques/10-license-keygen/02-validation-function-location.md<br>pe-reverse/techniques/10-license-keygen/03-key-algorithm-recovery.md |
| `非均匀位移` | pe-reverse | pe-reverse/techniques/10-license-keygen/08-cross-version-aob-migration.md |
| `频道验证` | apk-reverse/network | apk-reverse/techniques/05-network/01-game-protocol-hook.md<br>apk-reverse/techniques/05-network/02-license-verification-bypass.md |
| `验签绕过` | pe-reverse | pe-reverse/techniques/10-license-keygen/04-signature-chain-pubkey-swap.md |
| `验证码` | ctf-website/captcha-bypass | ctf-website/techniques/01-recon/captcha-bypass.md |
| `验证码绕过` | ctf-website/captcha-bypass | ctf-website/techniques/01-recon/captcha-bypass.md |
| `高位熵 .data 段 (>7.9) 但非加密` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/04-twinbasic-compressed-resource-recovery.md |
| `高熵判定` | pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `高熵数据块 (>7.5)` | pe-reverse | pe-reverse/techniques/05-crypto-unpack/05-high-entropy-compression-vs-crypto-routing.md |
| `高熵非加密` | pe-reverse/crypto-unpack | pe-reverse/techniques/05-crypto-unpack/01-pe-unpack-dump.md<br>pe-reverse/techniques/05-crypto-unpack/02-vmp-virtualization-analysis.md<br>pe-reverse/techniques/05-crypto-unpack/03-vmp-devirtualization-toolchain.md |
| `默认密码` | ctf-website/database-attacks | ctf-website/techniques/24-database/00-overview.md<br>ctf-website/techniques/24-database/01-sqli-fundamentals.md<br>ctf-website/techniques/24-database/02-sqli-advanced.md |
| `默认密码 default credentials` | ctf-website | ctf-website/techniques/24-database/00-overview.md |
| `默认密码 root:root sa:sa` | ctf-website | ctf-website/techniques/24-database/04-config-exposure.md |