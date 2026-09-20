---
name: develop-app
description: Implement KMP/Android/iOS app behavior from the root GraphQL contract and contract-aligned Mocks. Do not inspect or implement the Go backend.
---

# Develop the app

[English](SKILL.md) | [한국어](SKILL.ko.md)

1. Read [app rules](../../../app/AGENTS.md), relevant `app/docs/features/` notes and root `contracts/graphql/`. Use English except for paired-document maintenance or explicit requests. Do not load backend source, SQL, server guides, or cross-scope feature records.
2. For a new feature use [the app template](../../../app/docs/features/_template.md). Record flow, loading/error/retry/cancellation, platforms, and acceptance criteria. Reuse the existing contract. Report missing fields or semantics as a contract gap; settle necessary contract changes separately instead of implementing the server or guessing responses.
3. For UI, record approved Figma or agreed design, reuse existing components and Tokens, and map only real exceptions. Use an approved handoff; route new design decisions to [design-app](../design-app/SKILL.md) instead of silently redesigning. Create/edit Figma only when requested; review a new design before implementation unless already approved. Without an approved reference, do not claim visual parity.
4. Update app-owned GraphQL Operations and regenerate Apollo via [app checks](../../../app/docs/checks.md). Implement Shared Domain/Data/Network and the requested native platforms. Use contract-aligned repository/HTTP Mocks when no service is available; this does not require adding a Mock server or starting the backend.
5. Run app-only checks and affected platform tests, then review actual screens and accessibility. Shared changes may require both Android and iOS. Use a provided API endpoint for authorized connection checks; report Mock coverage separately from real integration. Record evidence and counterpart handoff with [sync-docs](../sync-docs/SKILL.md). Do not run backend checks or fix Go code as part of app development.
