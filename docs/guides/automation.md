# Project agents and Stop hook

[English](automation.md) | [한국어](automation.ko.md)

Read only for automation setup or maintenance. Runtime instructions are English; this guide's Korean companion explains the same setup to the user. README remains product/template information.

## Roles and handoff

Codex discovers project roles in `.codex/agents/`. They inherit the parent model and permissions; the template does not pin a model, grant extra access, or install plugins.

| Role | Owns | Entry |
| --- | --- | --- |
| `planning` | Product value, scope, flows, rules, acceptance, and approval state | [plan-feature](../../.agents/skills/plan-feature/SKILL.md) |
| `backend` | Go, DB, server verification; review and settlement of app-drafted GraphQL contract changes | [develop-backend](../../.agents/skills/develop-backend/SKILL.md) |
| `app` | Native flow implementation/validation with local fixtures, subsequent SDL drafting and GraphQL integration | [develop-app](../../.agents/skills/develop-app/SKILL.md) |
| `design` | Figma Make design, Design System from its artifacts, token matching before app development, visual review | [design-app](../../.agents/skills/design-app/SKILL.md) |

Use the requested role only. Send a bounded task, allowed paths, relevant plan/contract/design reference and acceptance criteria; use a fresh context when supported. Do not spawn all roles for every task or ask workers to redelegate. The main agent resolves scope and integrates concise results. Give concurrent writers disjoint ownership, including planning documents, design mapping files, and translation review records.

Follow [the feature workflow](../architecture.md): planning → Figma Make design → Design System from Make artifacts → token matching → native app development → GraphQL contract creation → backend development. These are handoff stages within the existing roles, not a command to spawn every role or add an orchestrator. Reuse completed approvals and start at the requested stage for existing work.

Planning keeps implementation-neutral drafts in `docs/plans/`; it does not inspect or change Figma, GraphQL, database, backend, or app implementation. Design uses actual Make artifacts to establish the approved Design System and token correspondence before app development, independently of GraphQL. It may read targeted native components/screens for reuse and review, but neither reads GraphQL nor edits production code. App validates working native flows with provisional local fixtures, then drafts needed root SDL in the requested contract step. Backend reviews the contract handoff and settles it with app before server implementation; neither side reads the other's source. App aligns its models/fixtures and Apollo Operations after agreement and performs requested connection checks after backend delivery. Report fixture, contract-aligned Mock, and live evidence separately. New design decisions need review; approved references need no repeat approval. Report gaps or unavailable tools instead of inventing behavior. Role instructions are guidance, not filesystem access controls.

Example requests: “Use planning to draft this feature plan”; “Use design to derive a Design System and token mapping from these approved Figma Make files”; “Use app to implement and validate the approved native flow with local data”; “Use app to draft the GraphQL contract from the validated flow and backend to review only the contract”; “Use backend to implement this agreed Query.” Request all-scope integration separately.

## Stop hook

[`.codex/hooks.json`](../../.codex/hooks.json) invokes [`tools/codex-stop.py`](../../tools/codex-stop.py) at the end of a main-agent turn. It resolves the repository root even when Codex starts in a subdirectory. Python 3 and Git are required.

- Checks staged, unstaged and untracked Markdown changes, `docs/.translations.json`, or `tools/check-docs.py`, including repositories with no initial commit. These are working-tree changes, not a per-task edit log; pre-existing changes may also trigger the check.
- Runs only the existing read-only document checker. It checks missing/stale translation pairs and review hashes, not translation meaning, link correctness, code behavior or visual quality. It never records reviews, repairs files, commits or builds either implementation.
- Success is quiet. Failure requests one continuation with bounded diagnostics. `stop_hook_active` skips another check/continuation to prevent a loop; manually rerun after fixing and report any remaining failure. Git/command errors and timeouts also request one continuation to run the check manually or report it unavailable; they never imply success. This lightweight hook has no cache; a later independent turn can check the same dirty files again.

The hook runs automatically only after Codex has loaded and trusted the project and the exact hook definition. In the CLI, start Codex here and use `/hooks` to inspect and trust it; changed definitions require review again. Trust covers the hook definition; review referenced repository scripts when adopting template updates or switching branches. Do not bypass trust. Creating files or passing the script tests does not prove that the current desktop session has loaded them. After reloading the project, confirm role availability and hook trust in the client.

For manual validation from the repository root:

```sh
python3 tools/check-docs.py
python3 -m unittest discover -s tools -p 'test_*.py'
./tools/verify.sh structure
```

The existing CI structure step runs the checker and tool tests independently of local hook trust. It does not establish that every platform/runtime check passed.

Sources: official OpenAI documentation for [custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents) and [hooks](https://learn.chatgpt.com/docs/hooks). This configuration was checked against the documented format and local CLI 0.154.0; local clients still control discovery and trust.
