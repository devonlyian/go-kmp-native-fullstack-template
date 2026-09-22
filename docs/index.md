# Development scopes

[English](index.md) | [한국어](index.ko.md)

Choose one scope. Read English only except for translation work or explicit requests. The README remains project information, not a development entrypoint.

For a new feature, follow [the workflow](architecture.md): planning → Figma design via Figma MCP → Design System from the approved file → token matching → native app development → GraphQL contract creation → backend development. Reuse approved outputs and existing contracts; enter at the requested stage for scoped fixes.

| Work | Entry |
| --- | --- |
| Planning: product value, scope, flows, and acceptance | [plan-feature](../.agents/skills/plan-feature/SKILL.md), [plan template](plans/_template.md) |
| Backend: Go, GraphQL server, DB | [Backend docs](../backend/docs/index.md) |
| App: KMP, Android, iOS | [App docs](../app/docs/index.md) |
| Design: Figma design, Design System, token matching, visual handoff | [Design rules](../app/design/AGENTS.md), [design-app](../.agents/skills/design-app/SKILL.md) |
| Agents and Stop hook setup | [Automation](guides/automation.md) |
| Shared API decision or handoff | Root `contracts/graphql/` and [contract boundary](architecture.md) |
| New repository setup | [Template adoption](guides/new-project.md) |
| Document maintenance | [sync-docs](../.agents/skills/sync-docs/SKILL.md) |

Backend and app do not read each other's implementation to develop. App validates native flows with provisional local fixtures before contract creation; GraphQL integration and backend implementation use agreed SDL. Record missing counterpart work as a handoff. Full-stack integration is requested separately.

Read [version evidence](versions.md) only for version research, and [historical verification](verification.md) or [system integration scenarios](features/system.md) only for integration/history tasks. These are not mandatory starting documents.
