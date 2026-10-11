# Seep Reverse Lab - local Pi Desktop entry
For authorized reverse-engineering tasks, read ~/.agents/skills/softseep/SKILL.md and follow its local macOS routing. The user may describe the goal in plain language. Confirm unclear target/scope, not tool names.

## Local Pi Desktop macOS routing (2026-10-04)
For natural-language requests to analyze a file, restore an algorithm, or solve an authorized self-authored crackme, choose the tools yourself. Do not ask the user for MCP names or addresses.
- Discover tools with ToolSearch before invocation; on-demand tools are available on the next turn.
- Call seep_status, then seep_auto_triage/seep_r2_info to identify the actual target platform.
- For macOS Mach-O use seep for recon and ghidra for C pseudocode. Native PE/ELF may also be analyzed statically; execution requires a compatible OS.
- Use list_open_programs and switch_program; load_program only if the target is not already imported. Never decompile the wrong current program.
- Search the KB as needed. Prove claims with actual tool results and negative/positive execution tests. Hash before and after execution.
- Use Chinese for Chinese requests. The lab prefix is a workflow hint, not a permission or safety override.
- IDA is not installed. Mono does not provide Windows WPF. JS-Reverse/Playwright are not enabled. Do not claim these are available.
- Do not change model safety settings or install BLOCK_NONE/interception extensions. They are not needed for this authorized workflow.
