# Shared contract boundary

[English](architecture.md) | [한국어](architecture.ko.md)

Backend and app are independent development scopes. Their shared API agreement is the single SDL source at `contracts/graphql/`, including descriptions of behavior. The app scope owns SDL drafts driven by approved design data requirements; the backend scope reviews them for implementability and settles the contract before server implementation. Implementation details stay in their own scopes: [backend](../backend/docs/architecture.md) or [app](../app/docs/architecture.md). Read only the relevant one.

## Contract changes and handoff

1. Reuse the current contract when it covers the requirement. Do not discover API behavior by reading the other implementation.
2. If an input, field, nullability rule, or failure behavior is missing, the app scope drafts the SDL change from the approved design's data requirements and the backend scope reviews it for implementability. Settle the contract before dependent backend implementation; use SDL descriptions for semantics that types cannot express. Do not invent server behavior in an app Mock.
3. Keep changes compatible where possible. A breaking proposal must identify migration/rollout needs; a schema edit alone does not prove consumer compatibility. Do not rewrite the other implementation as part of a one-scope task.
4. Regenerate and test only the current scope. Hand off the contract diff, expected request/response/error behavior, local evidence, and remaining counterpart/integration checks. The receiving scope uses the contract rather than the sender's source code.
5. Cross-scope investigation, implementation, and end-to-end verification require an explicit integration task. Mocks and separate tests are not evidence that both deployed sides interoperate.

For a contract decision, use [the shared feature record](features/_template.md). Keep implementation notes under the owning scope's `docs/features/`. The existing [system record](features/system.md) is a cross-scope integration reference, not required reading for routine backend or app development.

## Common limits

Reference documents are options, not dependency installation lists. Add infrastructure only for an implemented need; do not add example product domains. The structure checker detects selected boundaries, not a complete architecture or access-control policy. These reading rules do not create a filesystem sandbox.
