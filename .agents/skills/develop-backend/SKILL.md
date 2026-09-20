---
name: develop-backend
description: Implement Go/GraphQL/database behavior in backend using the root GraphQL contract. Do not implement or inspect app code; use for backend-scoped feature work.
---

# Develop the backend

[English](SKILL.md) | [한국어](SKILL.ko.md)

1. Read [backend rules](../../../backend/AGENTS.md), relevant `backend/docs/features/` notes and root `contracts/graphql/`. Read English except for paired-document maintenance or explicit requests. Do not load app source, app guides, or cross-scope feature records.
2. Specify backend behavior using [the backend template](../../../backend/docs/features/_template.md) for a new feature. The app scope drafts SDL changes from approved design data requirements; review the draft for implementability, nullability, and failure semantics, and settle the contract before implementation. Follow [contract handoff](../../../docs/architecture.md) only for that case. Never infer requirements from app code.
3. Implement the owned domain's Application/Repository/GraphQL path. Regenerate gqlgen; change SQL/schema and regenerate sqlc only when persistence changes, following [database](../../../backend/docs/database.md). Never edit generated files or applied migrations.
4. Use [backend checks](../../../backend/docs/checks.md) to format, regenerate, test GraphQL responses/errors and validate DB behavior. Run `./tools/verify.sh backend`; do not build clients. Load [dependencies](../../../backend/docs/dependencies.md) only for dependency changes.
5. Report backend evidence and remaining contract/consumer checks. A needed app change is a handoff, not permission to enter app. Update only relevant paired records with [sync-docs](../sync-docs/SKILL.md); commit/PR only when requested.
