# Pi Desktop acceptance audit - 2026-10-04
Reference: https://github.com/AI-modelsAPI/Seep-Reverse-Lab
Local HEAD matches reference: 59dbb1d5b9ad4858770d2ac0cda336a1696d7f49. Local macOS fixes retained.

## Crackme
Reviewed session 24f4fd68-12a1-4cd0-af93-829a1b375c79.
Real Pi calls: ToolSearch, Seep info/strings, Ghidra decompile/read_memory/search_instructions.
Key Pi-Lab-2026!: ACCESS GRANTED, exit 0.
Wrong key Pi-Lab-2025!: ACCESS DENIED, exit 1.
Independent rerun confirmed both; before/after hash unchanged and matches the session:
803e43a954d3f308b1b117fe68dd0aed9bed9349d505d459e372d758d1d22ad7
Early tool-not-found and invalid search arguments were corrected in the session.

## Fixes and tests
- Desktop softseep: macOS Mach-O now routes to Seep/Ghidra, not unsupported iOS.
- Added project AGENTS.md for plain-language routing and tool discovery.
- JADX classpath fixed from 1.5.1 to 1.5.6; actual Java decompilation passed.
- Nonzero exit with stdout now reports failure.
- JADX/Apktool MCP bad-input tests return isError=true, not false success.
- Apktool 2.11.0 resources-only decoding passed. Bundled plain.apk has invalid DEX, so full Android decompilation is not accepted from this fixture.
- Full-file hash replaces 50MiB prefix hash; 51MiB regression passed.
- Triage no longer asserts keyword matches without evidence.
- KB query, native triage, local verifier passed.

## Use and remaining verification
Save work and restart Pi to reload Seep. Open this project and start a new conversation. Ask in plain language to analyze your authorized binary, derive its key, and verify without modifying it.
The successful session explicitly named tools; a fresh plain-language-only conversation has NOT yet been observed.
Not accepted: IDA Mac, Windows WPF, Android Frida device injection, full APK rebuild/sign/install, JS-Reverse, Playwright.
Backups: local-backups/. Test outputs: labs/deployment-smoke-20261004/.
