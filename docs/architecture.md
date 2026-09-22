# Feature workflow and shared contract boundary

[English](architecture.md) | [한국어](architecture.ko.md)

## New feature workflow

| Stage | Owner | Output for the next stage |
| --- | --- | --- |
| 1. Planning | `planning` | Approved product scope, flows, states, and acceptance in `docs/plans/` |
| 2. Figma design | `design` | Reviewed design drawn directly in Figma via the Figma MCP tools, with file/node references and platform differences; an optional ui-ux-pro-max direction seed precedes drawing when no visual direction is approved |
| 3. Design System creation | `design` | Approved Figma components, variants, and semantic tokens derived from the approved Figma file |
| 4. Design token matching | `design` | Figma-to-native token/component correspondence; actual exceptions in `app/design/design-system-map.yaml`, planned new symbols in the handoff |
| 5. Native app development | `app` | Working Compose/SwiftUI flows with local fixtures/test doubles, platform and visual evidence, and demonstrated data needs |
| 6. GraphQL contract creation | `app` drafts, `backend` reviews | Agreed root SDL with inputs, outputs, nullability, and failure semantics based on the implemented app flows |
| 7. Backend development | `backend` | Server implementation and backend checks against the agreed contract; endpoint and consumer handoff |

Token matching does not wait for GraphQL. Inspect the actual approved Figma file before deriving the Design System; do not claim that a direction seed or an unapproved draft already supplies an approved component library or native app implementation. Reuse existing approvals. Record unresolved design or data decisions in the owning handoff.

Before the contract exists, app work includes native screens, navigation, state, local behavior, and app-owned models/test doubles needed to validate the flow. Provisional fixtures describe UX examples, not server response guarantees. During contract handoff, align app models, Operations, and fixtures with the settled SDL and regenerate Apollo before GraphQL integration. After backend delivery, complete the requested app connection and integration checks; the earlier app stage does not prove live integration. Entirely local features need no artificial GraphQL contract or backend work.

Use these stages for new features, not as mandatory restarts for existing features or scoped fixes. Reuse a current contract when it fits. A stage handoff does not authorize starting the next scope automatically; follow the user's requested work. Implementation details stay in their own scopes: [backend](../backend/docs/architecture.md) or [app](../app/docs/architecture.md). Read only the relevant one.

## Shared contract ownership

Backend and app are independent development scopes. Their shared API agreement is the single SDL source at `contracts/graphql/`, including descriptions of behavior. After app flow validation, the app scope owns the needed SDL drafts; the backend scope reviews implementability and settles the contract with app before server implementation. GraphQL-first describes the server's contract-before-implementation rule, not the order of product design and app prototyping.

## Contract changes and handoff

1. Reuse the current contract when it covers the requirement. Do not discover API behavior by reading the other implementation.
2. If an input, field, nullability rule, or failure behavior is missing, validate the app flow with explicitly provisional local fixtures first, then draft the needed SDL change. The backend scope reviews it for implementability using the contract handoff, not app source. Settle the contract before GraphQL integration and dependent backend implementation; use SDL descriptions for semantics that types cannot express. Contract review that changes product or UX decisions returns to planning/design; fixtures alone do not establish server behavior.
3. Keep changes compatible where possible. A breaking proposal must identify migration/rollout needs; a schema edit alone does not prove consumer compatibility. Do not rewrite the other implementation as part of a one-scope task.
4. Regenerate and test only the current scope. Hand off the contract diff, expected request/response/error behavior, local evidence, and remaining counterpart/integration checks. The receiving scope uses the contract rather than the sender's source code.
5. Cross-scope investigation, implementation, and end-to-end verification require an explicit integration task. Mocks and separate tests are not evidence that both deployed sides interoperate.

For a contract decision, use [the shared feature record](features/_template.md). Keep implementation notes under the owning scope's `docs/features/`. The existing [system record](features/system.md) is a cross-scope integration reference, not required reading for routine backend or app development.

## Common limits

Reference documents are options, not dependency installation lists. Add infrastructure only for an implemented need; do not add example product domains. The structure checker detects selected boundaries, not a complete architecture or access-control policy. These reading rules do not create a filesystem sandbox.
