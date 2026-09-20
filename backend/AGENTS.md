# Backend rules

[English](AGENTS.md) | [한국어](AGENTS.ko.md)

Scope: `backend/`, its documentation, backend tools/configuration, and root `contracts/graphql/`. Do not read or change `app/` to discover API requirements. The SDL and its descriptions are the app-facing contract; document any missing behavior before implementation.

- Use a GraphQL-first Modular Monolith: one API process with `internal/<domain>/{domain,application,repository,graphql}`. Resolvers call Application; Repository owns pgx/sqlc. Wire dependencies manually in `cmd/api`; other domains use public Application APIs, never another Repository or direct SQL.
- Use short singular lowercase domain names matching the contract. Initial domain: `system`, operation: `systemStatus`. Do not add example business domains or unused DDD patterns.
- Generate Go from root SDL with gqlgen; generate SQL access with sqlc. Keep generated Go versioned. Use pinned `.tools/atlas` for append-only migrations; never edit applied migrations or hide edits with checksums.
- Prefer existing code and the standard library. Read [dependencies](docs/dependencies.md) only for dependency changes. Use `net/http/httptest` for HTTP tests; DB integration uses `TEST_DATABASE_URL` and skips if absent. Never print connection URLs.

Use [develop-backend](../.agents/skills/develop-backend/SKILL.md) for implementation and [backend docs](docs/index.md) for setup, architecture, and checks. Default verification is `./tools/verify.sh backend` from the root. Test GraphQL requests/responses locally without building clients. Report any app compatibility check as pending handoff, not completed or automatically added to this task.
