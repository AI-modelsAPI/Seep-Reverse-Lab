# ctf-website 技术库目录

> 本目录由 `kb_maintain.py --sync-index` 自动生成（2026-10-17）
> 共 27 类 / 116 篇

## 完整目录

### 00-workflow — workflow（1）

- [`00-workflow/24h-loop-orchestration.md`](00-workflow/24h-loop-orchestration.md) — h Loop Orchestration

### 01-recon — recon（5）

- [`01-recon/captcha-bypass.md`](01-recon/captcha-bypass.md) — 验证码绕过技术与自动化
- [`01-recon/cloudflare-bypass.md`](01-recon/cloudflare-bypass.md) — Cloudflare 绕过：寻找真实源服务器 IP
- [`01-recon/fofa-hunting.md`](01-recon/fofa-hunting.md) — FOFA 资产测绘与漏洞狩猎
- [`01-recon/recon-routing.md`](01-recon/recon-routing.md) — Recon & 路由绕过
- [`01-recon/version-fingerprinting.md`](01-recon/version-fingerprinting.md) — 版本指纹识别

### 02-auth — auth（4）

- [`02-auth/host-header.md`](02-auth/host-header.md) — Host Header 攻击
- [`02-auth/ldap-injection.md`](02-auth/ldap-injection.md) — LDAP Injection
- [`02-auth/oauth-sso.md`](02-auth/oauth-sso.md) — OAuth 2.0 / OIDC 攻击实战
- [`02-auth/saml-attacks.md`](02-auth/saml-attacks.md) — SAML 2.0 攻击

### 03-injection — injection（7）

- [`03-injection/graphql.md`](03-injection/graphql.md) — GraphQL 攻击实战
- [`03-injection/grpc-protobuf.md`](03-injection/grpc-protobuf.md) — gRPC / Protobuf 攻击
- [`03-injection/hpp-crlf.md`](03-injection/hpp-crlf.md) — HPP / CRLF Injection / Header Injection
- [`03-injection/prototype-pollution.md`](03-injection/prototype-pollution.md) — Prototype Pollution (原型链污染)
- [`03-injection/redos-timing.md`](03-injection/redos-timing.md) — ReDoS & 时序攻击
- [`03-injection/sqli-nosqli.md`](03-injection/sqli-nosqli.md) — SQLi & NoSQLi (数据库注入高阶实战)
- [`03-injection/ssti.md`](03-injection/ssti.md) — SSTI (Server-Side Template Injection)

### 04-ssrf — ssrf（2）

- [`04-ssrf/open-redirect.md`](04-ssrf/open-redirect.md) — Open Redirect & Redirect Chain Attacks
- [`04-ssrf/ssrf.md`](04-ssrf/ssrf.md) — SSRF (Server-Side Request Forgery)

### 05-deserialization — deserialization（1）

- [`05-deserialization/deserialization.md`](05-deserialization/deserialization.md) — Deserialization Vulnerabilities

### 06-file-attacks — file-attacks（1）

- [`06-file-attacks/file-upload-xxe-lfi.md`](06-file-attacks/file-upload-xxe-lfi.md) — File Upload / XXE / LFI / Path Traversal

### 07-client — client（6）

- [`07-client/admin-bot-xss.md`](07-client/admin-bot-xss.md) — Admin Bot / XSS 实战
- [`07-client/cors-csrf.md`](07-client/cors-csrf.md) — CORS / CSRF 高级攻击
- [`07-client/js-runtime.md`](07-client/js-runtime.md) — JS Runtime / Browser Reversing
- [`07-client/postmessage.md`](07-client/postmessage.md) — PostMessage / 跨域通信攻击
- [`07-client/web-crypto-abuse.md`](07-client/web-crypto-abuse.md) — Web Crypto API 滥用
- [`07-client/websocket.md`](07-client/websocket.md) — WebSocket 攻击实战

### 08-infra — infra（3）

- [`08-infra/http2-attacks.md`](08-infra/http2-attacks.md) — HTTP/2 攻击
- [`08-infra/race-cache-smuggling.md`](08-infra/race-cache-smuggling.md) — Race Condition / Cache Poisoning / Request Smuggling
- [`08-infra/web-cache-deception.md`](08-infra/web-cache-deception.md) — Web Cache Deception

### 09-cve — cve（10）

- [`09-cve/01-browser-sandbox-escape.md`](09-cve/01-browser-sandbox-escape.md) — Blink UAF：CSSFontFeatureValuesMap 迭代器悬空指针（CVE-2026-2441）
- [`09-cve/02-redis-zipmap-rce.md`](09-cve/02-redis-zipmap-rce.md) — Redis/Valkey RESTORE：zipmap 长度前缀步长不一致（CVE-2026-25243）
- [`09-cve/03-cpanel-caldav-traversal.md`](09-cve/03-cpanel-caldav-traversal.md) — cPanel CalDAV 预认证路径穿越（CVE-2026-29205）
- [`09-cve/04-nezha-path-traversal-jwt.md`](09-cve/04-nezha-path-traversal-jwt.md) — Nezha Monitoring：路径遍历 + JWT 伪造管理员接管（CVE-2026-53519）
- [`09-cve/05-litellm-privesc.md`](09-cve/05-litellm-privesc.md) — LiteLLM：API Key 生成绕过角色限制 + 自提权（CVE-2026-47101）
- [`09-cve/06-nginx-rewrite-heapoverflow.md`](09-cve/06-nginx-rewrite-heapoverflow.md) — NGINX rewrite 模块：set 缓冲区长度错配堆溢出（CVE-2026-42945）
- [`09-cve/README.md`](09-cve/README.md) — CVE 技术库（Web / 内核 / 本地）
- [`09-cve/cve-correlation-graph.md`](09-cve/cve-correlation-graph.md) — CVE Correlation Graph（CVE 关联网）
- [`09-cve/cve-workflow.md`](09-cve/cve-workflow.md) — CVE Workflow For World-Class Web CTF
- [`09-cve/multi-cve-chain-playbook.md`](09-cve/multi-cve-chain-playbook.md) — Multi-CVE Chain Playbook（多 CVE 组合联合利用）

### 10-cloud — cloud（8）

- [`10-cloud/aws-iam-privesc.md`](10-cloud/aws-iam-privesc.md) — AWS IAM 权限枚举与提权路径
- [`10-cloud/ci-cd-pipeline.md`](10-cloud/ci-cd-pipeline.md) — CI/CD Pipeline 攻击
- [`10-cloud/container-runtime-escape.md`](10-cloud/container-runtime-escape.md) — 容器运行时逃逸打点
- [`10-cloud/github-actions-abuse-paths.md`](10-cloud/github-actions-abuse-paths.md) — GitHub Actions 滥用路径
- [`10-cloud/k8s-rbac-attack-paths.md`](10-cloud/k8s-rbac-attack-paths.md) — Kubernetes RBAC 攻击路径
- [`10-cloud/kubernetes-container.md`](10-cloud/kubernetes-container.md) — Kubernetes & 容器逃逸
- [`10-cloud/serverless-lambda.md`](10-cloud/serverless-lambda.md) — Serverless / Lambda 攻击
- [`10-cloud/terraform-state-secrets.md`](10-cloud/terraform-state-secrets.md) — Terraform State 与 IaC 凭证泄露

### 11-dos — dos（2）

- [`11-dos/01-valkey-resp-dos.md`](11-dos/01-valkey-resp-dos.md) — Valkey RESP 协议：预认证断言失败 DoS（CVE-2026-27623）
- [`11-dos/README.md`](11-dos/README.md) — DoS 拒绝服务技术库

### 11-supply-chain — supply-chain（1）

- [`11-supply-chain/dependency-confusion.md`](11-supply-chain/dependency-confusion.md) — Dependency Confusion & 供应链攻击

### 12-payment — payment（11）

- [`12-payment/README.md`](12-payment/README.md) — payment — 支付、订单与票务业务逻辑
- [`12-payment/payment-bypass.md`](12-payment/payment-bypass.md) — Payment Bypass — 支付绕过深度技术手册
- [`12-payment/payment-callback-async.md`](12-payment/payment-callback-async.md) — Payment Callback & Async Attack — 支付回调与异步攻击深度手册
- [`12-payment/payment-digital-goods.md`](12-payment/payment-digital-goods.md) — Payment Digital Goods & IAP — 虚拟商品/内购攻击手册
- [`12-payment/payment-email-bounce-idor.md`](12-payment/payment-email-bounce-idor.md) — 退信滥用 + 订单号授权绕过窃取卡密
- [`12-payment/payment-logic.md`](12-payment/payment-logic.md) — Payment Logic Attacks — 支付类 Web CTF 技术手册
- [`12-payment/payment-php.md`](12-payment/payment-php.md) — PHP Payment Attacks — PHP 支付专项攻击手册
- [`12-payment/payment-race-lost-update.md`](12-payment/payment-race-lost-update.md) — Payment Race / Lost Update — 余额扣减丢失更新
- [`12-payment/payment-subscription.md`](12-payment/payment-subscription.md) — Payment Subscription — 订阅/定期付款攻击深度手册
- [`12-payment/platform-fingerprints.md`](12-payment/platform-fingerprints.md) — PHP 发卡/电商平台指纹库
- [`12-payment/ticket-rush-api-reversing.md`](12-payment/ticket-rush-api-reversing.md) — Ticket Rush API Reversing — 票务抢购状态机、Token 与风控参数

### 13-signature — signature（8）

- [`13-signature/00-overview.md`](13-signature/00-overview.md) — Signature Forgery — 签名伪造与验证绕过全景手册
- [`13-signature/01-algorithm.md`](13-signature/01-algorithm.md) — Signature Algorithm Attacks — 签名算法降级/混淆/None 攻击深度手册
- [`13-signature/02-implementation.md`](13-signature/02-implementation.md) — Signature Implementation Bugs — 签名实现缺陷深度手册
- [`13-signature/03-key-attacks.md`](13-signature/03-key-attacks.md) — Key Attacks — 签名密钥攻击深度技术手册
- [`13-signature/04-canonicalization.md`](13-signature/04-canonicalization.md) — Canonicalization Attacks — 签名规范化绕过
- [`13-signature/05-length-extension.md`](13-signature/05-length-extension.md) — Hash Length Extension 攻击 — 深度技术手册
- [`13-signature/06-replay-nonce.md`](13-signature/06-replay-nonce.md) — Replay / Nonce / Timestamp — 重放攻击深度技术手册
- [`13-signature/README.md`](13-signature/README.md) — signature — 签名伪造与验证绕过

### 14-idor — idor（2）

- [`14-idor/01-idor-enumeration.md`](14-idor/01-idor-enumeration.md) — IDOR 深度枚举与利用 — 水平/垂直越权实战方法论
- [`14-idor/02-bac-business-logic.md`](14-idor/02-bac-business-logic.md) — 功能级访问控制缺失 (BAC) — 垂直越权与业务逻辑绕过

### 15-mass-assignment — mass-assignment（2）

- [`15-mass-assignment/01-mass-assignment.md`](15-mass-assignment/01-mass-assignment.md) — 批量赋值与属性注入深度利用手册
- [`15-mass-assignment/02-parameter-tampering.md`](15-mass-assignment/02-parameter-tampering.md) — 参数篡改全链 — 价格/数量/优惠券/竞态深度攻击

### 16-rate-limit — rate-limit（2）

- [`16-rate-limit/01-rate-limit-bypass.md`](16-rate-limit/01-rate-limit-bypass.md) — 速率限制绕过 — IP 轮换、Header 操纵与应用层绕过
- [`16-rate-limit/02-brute-force-tactics.md`](16-rate-limit/02-brute-force-tactics.md) — 高级暴力破解 — 凭证喷洒、MFA 疲劳、Hash 策略

### 17-api-attacks — api-attacks（2）

- [`17-api-attacks/01-api-discovery-leak.md`](17-api-attacks/01-api-discovery-leak.md) — API 发现与信息泄露 — Swagger、GraphQL、Source Map 与移动端提取
- [`17-api-attacks/02-api-key-leak.md`](17-api-attacks/02-api-key-leak.md) — API 密钥泄露与利用 — GitHub Dorking、客户端密钥链、云服务滥用

### 18-cors-csp-advanced — cors-csp-advanced（2）

- [`18-cors-csp-advanced/01-csp-bypass.md`](18-cors-csp-advanced/01-csp-bypass.md) — CSP 绕过全技术栈
- [`18-cors-csp-advanced/02-xs-leaks-browser-sidechannels.md`](18-cors-csp-advanced/02-xs-leaks-browser-sidechannels.md) — XS-Leaks 浏览器侧信道攻击

### 19-dns-email — dns-email（2）

- [`19-dns-email/01-subdomain-takeover.md`](19-dns-email/01-subdomain-takeover.md) — 子域名接管深度
- [`19-dns-email/02-email-spoofing.md`](19-dns-email/02-email-spoofing.md) — 邮件伪造与 SPF / DKIM / DMARC

### 20-oauth-deep — oauth-deep（2）

- [`20-oauth-deep/01-oauth-attack-chains.md`](20-oauth-deep/01-oauth-attack-chains.md) — OAuth 2.0 攻击全链
- [`20-oauth-deep/02-session-fixation-attacks.md`](20-oauth-deep/02-session-fixation-attacks.md) — Session 固定与 SSO 劫持

### 21-mobile-bridge — mobile-bridge（2）

- [`21-mobile-bridge/01-webview-attacks.md`](21-mobile-bridge/01-webview-attacks.md) — WebView 攻击全技术
- [`21-mobile-bridge/02-cordova-reactnative.md`](21-mobile-bridge/02-cordova-reactnative.md) — 跨平台框架攻击面 — Cordova / React Native / Flutter / Electron

### 22-dos — dos（13）

- [`22-dos/01-application-layer-dos.md`](22-dos/01-application-layer-dos.md) — Application-Layer DoS
- [`22-dos/02-resource-exhaustion.md`](22-dos/02-resource-exhaustion.md) — Resource Exhaustion & Algorithm Complexity Attacks
- [`22-dos/03-amplification-drdos.md`](22-dos/03-amplification-drdos.md) — Amplification / DRDoS Attacks
- [`22-dos/04-redos.md`](22-dos/04-redos.md) — ReDoS — 正则表达式拒绝服务
- [`22-dos/05-http2-continuation.md`](22-dos/05-http2-continuation.md) — HTTP/2 CONTINUATION Flood & H2/H3 高级攻击
- [`22-dos/06-tcp-state-exhaustion.md`](22-dos/06-tcp-state-exhaustion.md) — TCP 协议栈状态耗尽
- [`22-dos/07-dns-dos.md`](22-dos/07-dns-dos.md) — DNS 拒绝服务攻击
- [`22-dos/08-tls-exhaustion.md`](22-dos/08-tls-exhaustion.md) — TLS/SSL 握手耗尽
- [`22-dos/09-cache-cdn-dos.md`](22-dos/09-cache-cdn-dos.md) — 缓存 / CDN 拒绝服务
- [`22-dos/10-api-abuse.md`](22-dos/10-api-abuse.md) — API 滥用拒绝服务
- [`22-dos/11-cloud-container-dos.md`](22-dos/11-cloud-container-dos.md) — 云原生 / 容器拒绝服务
- [`22-dos/12-ssrf-dos.md`](22-dos/12-ssrf-dos.md) — SSRF 驱动的拒绝服务
- [`22-dos/13-database-dos.md`](22-dos/13-database-dos.md) — 数据库层拒绝服务

### 23-paywall-bypass — paywall-bypass（5）

- [`23-paywall-bypass/01-paywall-detection-bypass.md`](23-paywall-bypass/01-paywall-detection-bypass.md) — Paywall 检测与绕过总览
- [`23-paywall-bypass/02-http-header-manipulation.md`](23-paywall-bypass/02-http-header-manipulation.md) — HTTP 请求头伪装
- [`23-paywall-bypass/03-network-rule-blocking.md`](23-paywall-bypass/03-network-rule-blocking.md) — Network 规则拦截 — 阻止 Paywall 脚本加载
- [`23-paywall-bypass/04-content-extraction.md`](23-paywall-bypass/04-content-extraction.md) — 内容提取 — JSON-LD / Next.js / archive.is
- [`23-paywall-bypass/05-dom-css-manipulation.md`](23-paywall-bypass/05-dom-css-manipulation.md) — DOM / CSS / Storage 操作

### 24-database — database（9）

- [`24-database/00-overview.md`](24-database/00-overview.md) — Database Attack Surface — 数据库攻击全景与决策树
- [`24-database/01-sqli-fundamentals.md`](24-database/01-sqli-fundamentals.md) — SQL Injection Core — SQL 注入基础与全类型覆盖
- [`24-database/02-sqli-advanced.md`](24-database/02-sqli-advanced.md) — Advanced SQLi & WAF Bypass — 高级注入与绕过技术
- [`24-database/03-nosql-injection.md`](24-database/03-nosql-injection.md) — NoSQL Injection — NoSQL 注入攻击
- [`24-database/04-config-exposure.md`](24-database/04-config-exposure.md) — Database Config Exposure — 数据库配置泄露
- [`24-database/05-backup-log-leak.md`](24-database/05-backup-log-leak.md) — Database Backup & Log Leak — 数据库备份与日志泄露
- [`24-database/06-card-platform.md`](24-database/06-card-platform.md) — Card-Selling Platform Exploitation — 自动发卡平台攻击手册
- [`24-database/07-data-cleaning.md`](24-database/07-data-cleaning.md) — Database Dump Cleaning — 泄露数据清洗方法论
- [`24-database/README.md`](24-database/README.md) — database — 数据库攻击技术

### 27-js-reverse — 前端 JS/AST 逆向与补环境（3）

- [`27-js-reverse/01-ast-deobfuscation-pipeline.md`](27-js-reverse/01-ast-deobfuscation-pipeline.md) — 现代 JS AST 自动化解混淆实战与规则工装
- [`27-js-reverse/02-browser-env-emulation-proxy-sandbox.md`](27-js-reverse/02-browser-env-emulation-proxy-sandbox.md) — Node.js 浏览器补环境标准 Proxy 探针与防风控对抗手册
- [`27-js-reverse/03-sourcemap-unpack-and-webpack-hijacking.md`](27-js-reverse/03-sourcemap-unpack-and-webpack-hijacking.md) — 现代前端 SourceMap 泄露源码还原与 Webpack 闭包劫持
