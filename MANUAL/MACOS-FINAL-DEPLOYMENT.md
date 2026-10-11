# Correction - Pi Desktop registration
The previous report tested standalone MCP processes, not Desktop registration. Pi Desktop 0.16.0 uses ~/.agents/servers/*.json, not ~/.pi/agent/mcp.json. On 2026-10-04, seep and ghidra were registered via host-core mcp.upsert and confirmed via mcp.list. Reopen Global MCP settings. Desktop conversation calls remain to be verified. See labs/pi-crackme/README.md.

# macOS deployment acceptance - 2026-10-04

Installed location: ~/projects/Seep-Reverse-Lab

## Verified in this handoff
- seep MCP: stdio initialize and tools/list passed, 23 tools. seep_status called.
- ghidra MCP: stdio initialize and tools/list passed, 222 tools.
- GhidraMCP 6.0.0 headless: HTTP health healthy; LaunchAgent running.
- Native PE test rasm2.exe: 357 functions; decompile_function returned C for sdb_atoi.
- Radare2 6.1.8 native Darwin x86_64 runs.
- Mono 6.12.0.206: fresh mcs compilation and mono execution returned MONO_ACCEPT_PASS.
- Local verifier exited 0. See MACOS-FINAL-VERIFY.log.

## Changes
- Backed up ~/.pi/agent/mcp.json before adding explicit PATH to seep/ghidra env.
- Added setup/verify-macos-local.sh; no shell startup files changed.
- Corrected the outdated Mono installation statement in MACOS-GHIDRA-MCP.md.

## Remaining desktop activation
The MCP tests used fresh processes with the saved Pi configuration.
The running PI-Desktop was not terminated to avoid interrupting unsaved work.
Save work and restart PI-Desktop to reload the updated MCP environment.
Desktop UI tool invocation after reload has not been verified.

## Scope and limits
- IDA Pro for Mac is not installed; Ghidra is the native-code alternative.
- Mono does not provide Windows WPF or a modern .NET SDK.
- The previous session recorded BoosterX WPF/initialization failures; this handoff did not retry or modify that application.
- playwright and js-reverse remain disabled as previously configured; not accepted as deployed services.
- Pydantic emits IncompleteFieldDefinitionWarning; MCP handshakes and tested calls succeeded.

Repeat: bash ~/projects/Seep-Reverse-Lab/setup/verify-macos-local.sh
