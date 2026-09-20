# Database changes

[English](database.md) | [한국어](database.ko.md)

Complete [backend setup](setup.md). `backend/db/schema/` and `backend/db/migration/` define the database contract; `contracts/graphql/` remains the sole GraphQL SDL source.

After changing persistent schema or SQL queries, create, review, apply, and generate from the repository root:

```sh
set -a; . ./.env; set +a
(cd backend && ../.tools/atlas migrate diff add_feature --env local)
(cd backend && ../.tools/atlas migrate apply --env local)
(cd backend && go tool sqlc generate)
```

`migrate diff` uses Docker's temporary development database. Never modify an applied migration or its checksum, and never edit sqlc output. Finish with [backend checks](checks.md).
