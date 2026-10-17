---
id: "ctf-website/checklists/evidence"
title: "Evidence Checklist"
evidence: "inferred"
validated_by: "方法论/描述性（未标记实测）"
---
# Evidence Checklist

For every meaningful finding, capture:

- Full request and response.
- Timestamp and target URL.
- Cookie/session identity used.
- Payload and exact encoding.
- Server-side visible effect: error, file content, row count, flag, callback, state change.
- Tool command or script path.
- If browser-side: screenshot, network trace, JS hook output, storage/cookie snapshot.
- If race: number of requests, timing, success/failure ratio.

Evidence is stronger when it is replayable from a clean session.
