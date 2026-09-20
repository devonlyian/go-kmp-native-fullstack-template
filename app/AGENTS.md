# App rules

[English](AGENTS.md) | [한국어](AGENTS.ko.md)

Scope: `app/` (Shared, Android, iOS), its documentation, app tools/configuration, and the root `contracts/graphql/` contract drafts this scope owns. Do not read Go resolvers, repositories, DB schema, or backend docs to infer app behavior. Consume the SDL and its descriptions; report contract gaps instead of guessing or implementing the server.

- KMP shares Domain/Data/Network only. No Compose, SwiftUI, ViewModel, navigation, or screen state in `shared/`. Android uses Compose/ViewModel; iOS uses SwiftUI/native `@Observable` state.
- Match feature names to the contract across Shared and Android `feature/<domain>` and Swift `Features/<Domain>`. Use short singular lowercase names, PascalCase in Swift. Initial feature: `system`; no example business domains.
- Apollo reads root SDL directly. Update app-owned Operations and SDL drafts from the approved design's data requirements; generate client types and keep generated Kotlin in build outputs. The backend scope reviews the draft for implementability and owns server behavior; a backend implementation or DB change is not part of app work.
- Develop against contract-aligned responses/Mocks when no API is available; model data, GraphQL/transport errors, nullability, and cancellation. Screens and ViewModels may be scaffolded from the approved design's data concepts before the SDL is settled; wire repositories only against the confirmed contract. Use an existing API endpoint for connection checks when available. Mocks do not prove server compatibility; do not start backend work just to unblock UI.
- For UI, record approved Figma or agreed design, reuse same-named native components and `design/design-system-map.yaml` Tokens, and map only real exceptions. Keep semantic colors, spacing, and radii in the Design System.

Use [develop-app](../.agents/skills/develop-app/SKILL.md) and [app docs](docs/index.md). Run `./tools/verify.sh app` for Shared/Android and `./tools/verify.sh ios` for Swift/Apple interop, plus affected platform tests and actual UI/accessibility review. Shared changes may require both app platforms; they do not require backend tests. Full server/app integration is a separate explicitly requested task.

Design-only tasks use [design rules](design/AGENTS.md) and [design-app](../.agents/skills/design-app/SKILL.md); they produce a design handoff without implementing or building the app. The app role implements an approved handoff and reports new design decisions to design.
