# App architecture

[English](architecture.md) | [한국어](architecture.ko.md)

The app consumes root `contracts/graphql/` through Apollo Operations and drafts SDL changes from approved design data requirements; the backend scope reviews a draft and settles the contract before server implementation. Its design does not depend on how the server stores data or implements resolvers. Read only app source and contract descriptions.

| Location | Responsibility |
| --- | --- |
| `app/shared/` | Domain models, repository contracts, use cases, Data/Network, generated GraphQL clients |
| `app/androidApp/` | Compose, Android ViewModel, lifecycle, navigation, native UI state |
| `app/iosApp/` | SwiftUI, native Observation, lifecycle, navigation, native UI state |
| `app/design/` | Component/Token naming and actual mapping exceptions |

Shared contains no presentation. Use contract-derived names; PascalCase Swift directories are the same feature. Start with `system`; add domains/navigation only for actual requirements. Do not copy backend DDD layers into UI modules.

Build app-owned Operations and fixtures from the SDL; distinguish valid false/empty data, GraphQL errors, transport errors, and cancellation. Without a running service, use contract-aligned repository or HTTP test doubles. This is a development/testing approach, not an installed standalone Mock server. Record real API integration as unverified until checked against an available endpoint.

For UI changes, establish approved Figma or agreed design before implementation, reuse existing native components and semantic Tokens, and review actual screens, text scaling, dark mode, and accessibility. This template has no approved Figma file or Code Connect connection; mapping does not prove pixel parity.

Use [develop-app](../../.agents/skills/develop-app/SKILL.md), [app checks](checks.md), and the relevant [Android](android.md) or [iOS](ios.md) guide. Physical-device performance, camera behavior, battery use, signing, and distribution require their own evidence.
