# App architecture

[English](architecture.md) | [한국어](architecture.ko.md)

For UI work, the app starts with an approved design, the Design System, and token correspondence using Make artifacts, existing approved Figma, or an agreed local specification. Contract-only, GraphQL connection, and other non-UI work need no design prerequisite. It implements and validates native flows with local fixtures/test doubles before creating a new GraphQL contract. After flow validation, app drafts needed root `contracts/graphql/` changes and backend reviews and settles them with app before server implementation. The app then consumes agreed SDL through Apollo Operations. Its design does not depend on server storage or resolver implementation. Read only app source and relevant contract descriptions.

| Location | Responsibility |
| --- | --- |
| `app/shared/` | Domain models, repository contracts, use cases, Data/Network, generated GraphQL clients |
| `app/androidApp/` | Compose, Android ViewModel, lifecycle, navigation, native UI state |
| `app/iosApp/` | SwiftUI, native Observation, lifecycle, navigation, native UI state |
| `app/design/` | Component/Token naming and actual mapping exceptions |

Shared contains no presentation. Derive names from approved product concepts before a contract exists and reconcile them at contract settlement; PascalCase Swift directories are the same feature. Start with `system`; add domains/navigation only for actual requirements. Do not copy backend DDD layers into UI modules.

Before contract agreement, use app-owned models and local repository test doubles to exercise real navigation, state, and local behavior. Mark fixtures and remote behavior assumptions as provisional; they are not a second API specification. After agreement, align models/fixtures, generate app-owned Operations from root SDL, and connect GraphQL adapters. Distinguish valid false/empty data, GraphQL errors, transport errors, and cancellation. Without a running service, use contract-aligned repository or HTTP test doubles; no standalone Mock server is required. After backend delivery, record real API integration as unverified until the requested checks pass against a provided endpoint.

For UI changes, use approved Make artifacts, existing approved Figma designs, or an agreed local specification with the Design System reference. Match semantic Tokens and components before app development, independently of GraphQL; keep planned native symbols in the design handoff until implemented and record only actual mapping exceptions. Review actual screens, text scaling, dark mode, and accessibility. This template has no approved Figma file or Code Connect connection; mapping does not prove pixel parity.

Use [develop-app](../../.agents/skills/develop-app/SKILL.md), [app checks](checks.md), and the relevant [Android](android.md) or [iOS](ios.md) guide. Physical-device performance, camera behavior, battery use, signing, and distribution require their own evidence.
