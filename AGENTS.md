# Common project rules

[English](AGENTS.md) | [한국어](AGENTS.ko.md)

- Read English by default; Korean companions are for translation edits/review or explicit requests. Respond in Korean. For Markdown changes use [sync-docs](.agents/skills/sync-docs/SKILL.md); review both languages and record the pair.
- Work in one requested scope: [planning](.agents/skills/plan-feature/SKILL.md), [backend](backend/AGENTS.md), [app](app/AGENTS.md), or [design](app/design/AGENTS.md). Follow that scope's read/write boundaries; planning does not inspect implementation or the shared contract. Do not expand into another scope unless the user explicitly requests it. If the target is unclear, clarify it before implementation.
- `contracts/graphql/` is the only shared API source of truth. Agree inputs, outputs, nullability, and failure semantics before implementation; use SDL descriptions for behavior. Missing details are contract gaps, not reasons to reverse-engineer the other side. Handle needed contract changes and handoff separately; do not silently change both implementations. See [contract boundaries](docs/architecture.md) only when needed.
- Never hand-edit generated code. Reuse existing code and add dependencies only for current requirements. Preserve user work and hooks; never expose or commit secrets, local environment files, credentials, or build outputs.
- Branch from existing `dev` using `feat/`, `fix/`, `chore/`, or `docs/`; PRs target `dev`, releases use `dev` → `main`. No commit, push, PR, remote creation, or license choice without a user request.

README is replaceable project information, not an agent instruction source. Select scope-specific documentation from [docs/index.md](docs/index.md). Run scoped checks; full-stack verification is a separate explicitly requested task. Document-only changes use `./tools/verify.sh structure`.

For delegated work use the matching `planning`, `backend`, `app`, or `design` role in `.codex/agents/`; do not start every role automatically. Send only the bounded task, allowed paths, relevant plan/contract/design references, and acceptance criteria; avoid copying full history when a fresh context is available. See [automation](docs/guides/automation.md) only for setup or hook maintenance.
