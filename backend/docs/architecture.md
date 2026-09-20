# Backend architecture

[English](architecture.md) | [한국어](architecture.ko.md)

Read for backend boundary decisions. Develop against root `contracts/graphql/`; do not inspect app implementation.

## Modular Monolith and domain boundaries

The backend uses a **GraphQL-first Modular Monolith**: domain modules run in one Go API process, with one backend deployment unit. A module is a domain boundary inside the application, not a separate service or a separate `go.mod`. Currently only `system` exists; the template establishes the boundary convention for additional domains when real requirements arise.

Use DDD's Bounded Context and domain ownership concepts to decide boundaries. A screen or endpoint alone does not justify a new domain. Add aggregates, domain events, repository interfaces, or other patterns only when an implemented requirement needs them.

| Location | Responsibility |
| --- | --- |
| `backend/internal/<domain>/domain` | Domain models and business rules; no HTTP, GraphQL, or SQL concerns |
| `backend/internal/<domain>/application` | Public use cases and coordination of domain logic and data access |
| `backend/internal/<domain>/repository` | The domain's data access through sqlc and pgx |
| `backend/internal/<domain>/graphql` | GraphQL adapter; delegates use cases to Application and maps API results |
| `backend/cmd/api/main.go` | Manually creates dependencies, connects adapters, and starts the API process |

The current request flow is:

```text
POST /graphql: systemStatus
  → system GraphQL resolver
  → application.Service.Status
  → repository.Repository.DatabaseReady
  → sqlc-generated query / pgx
  → PostgreSQL
```

This is the runtime call flow, not an instruction to make Domain depend on Application or Repository. The current small Application service uses a concrete repository; an interface is not required merely to label the architecture.

When more domains are added, call another domain only through its public Application API. Do not import its Repository, execute SQL against its owned data directly, or bypass it through generated database access. A shared PostgreSQL instance does not remove ownership boundaries. Use ordinary in-process Go calls between modules. Consider independent services and network protocols only when independent deployment, scaling, or fault isolation is actually needed; service extraction is not a goal by itself.

The GraphQL contract remains under `contracts/graphql/`, with domain-specific SDL files feeding one public API. Do not introduce `backend/graph/schema` as a second source. The current gqlgen output is under `system`; when a second context is needed, review resolver composition and generated-code placement as part of that change rather than routing new domain logic through `system`.

Use [backend development](../../.agents/skills/develop-backend/SKILL.md). Add dependencies only for current requirements; see [dependencies](dependencies.md).
