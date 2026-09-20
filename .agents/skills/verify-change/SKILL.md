---
name: verify-change
description: Select checks within the requested backend, app, or documentation scope. Report contract handoff and integration gaps without expanding to the other implementation.
---

# Verify within scope

[English](SKILL.md) | [한국어](SKILL.ko.md)

Use English except for translation work or explicit requests. Select the requested scope before reading guides or running tools. A changed shared SDL does not authorize the other scope's build or source inspection.

| Scope | Checks and references |
| --- | --- |
| Markdown only | [sync-docs](../sync-docs/SKILL.md), then `./tools/verify.sh structure` |
| Backend | [Backend checks](../../../backend/docs/checks.md), `./tools/verify.sh backend`; regenerate/test server GraphQL and DB only |
| App Shared / Android | [App checks](../../../app/docs/checks.md), `./tools/verify.sh app`; Shared changes also require relevant KMP iOS tests and app builds |
| App Swift / Apple interop | `./tools/verify.sh ios`, [iOS](../../../app/docs/ios.md) tests; inspect no backend code |
| Explicit full-stack integration | Full `./tools/verify.sh` plus platform/runtime checks requested for that integration; [common check routing](../../../docs/guides/checks.md) |

Regenerate the current scope before consistency checks. For backend integration provide `TEST_DATABASE_URL` without exposing secrets. Use `VERIFY_STRICT=1` when prerequisites are available; otherwise name skipped checks. Toolchain work also stays in its requested scope.

App UI changes require relevant platform tests and real screen/accessibility review; use contract-aligned Mocks or a supplied API. The basic script does not run Android connected tests, KMP iOS tests, native iOS app/UI tests, or visual review. Mocks do not prove live server compatibility.

Report commands, date/environment, results, and limits in the owning scope's records. Hand off any counterpart/consumer checks after a contract change; do not claim full compatibility or silently fix the other scope. Historical integration records are read only for an explicit integration/history task, not every local fix.
