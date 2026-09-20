# Backend dependencies

[English](dependencies.md) | [한국어](dependencies.ko.md)

Start with the standard library and add a dependency only for a current requirement. Do not preinstall authentication, caching, messaging, observability, alternative databases, or DI.

The application directly imports `gqlgen`, `pgx/v5`, and `gqlparser/v2`. `gqlgen` and `sqlc` are also pinned generators. Their indirect dependencies, including MySQL, SQLite, gRPC, and Zap, are tool dependencies, not selected application infrastructure. Let Go manage `// indirect` entries.

Before changing a dependency, inspect its use:

```sh
(cd backend && go mod why -m github.com/jackc/pgx/v5 && go list -deps ./cmd/api && go mod tidy -diff)
```

Replace `github.com/jackc/pgx/v5` with the module being evaluated. When removal is justified, run `go mod tidy`, regenerate, and run [backend checks](checks.md).
