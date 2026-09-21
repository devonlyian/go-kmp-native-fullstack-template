---
name: develop-backend
description: Implement Go/GraphQL/database behavior in backend using the root GraphQL contract. Do not implement or inspect app code; use for backend-scoped feature work.
---

# Develop the backend

[English](SKILL.md) | [한국어](SKILL.ko.md)

1. Read [backend rules](../../../backend/AGENTS.md), relevant `backend/docs/features/` notes and root `contracts/graphql/`. Read English except for paired-document maintenance or explicit requests. Do not load app source or app guides; shared API records are read only for the requested contract handoff.
2. Specify backend behavior using [the backend template](../../../backend/docs/features/_template.md) for a new feature. After native app flow validation, app drafts needed SDL changes from demonstrated data requirements. Review the contract handoff for implementability, nullability, and failure semantics, then settle it with app before server implementation. Follow [contract handoff](../../../docs/architecture.md) for that case. Provisional fixtures are examples, not agreed server behavior. Return product/UX changes to planning/design; never infer requirements from app code. For contract-only review, report decisions and remaining gaps without starting server implementation.
3. Implement the owned domain's Application/Repository/GraphQL path. Regenerate gqlgen; change SQL/schema and regenerate sqlc only when persistence changes, following [database](../../../backend/docs/database.md). Never edit generated files or applied migrations.
4. Use [backend checks](../../../backend/docs/checks.md) to format, regenerate, test GraphQL responses/errors and validate DB behavior. Run `./tools/verify.sh backend`; do not build clients. Load [dependencies](../../../backend/docs/dependencies.md) only for dependency changes.
5. Report backend evidence and remaining contract/consumer checks. A needed app change is a handoff, not permission to enter app. Update only relevant paired records with [sync-docs](../sync-docs/SKILL.md); commit/PR only when requested.
