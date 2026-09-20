# Backend checks

[English](checks.md) | [한국어](checks.ko.md)

Run commands from the repository root. The root SDL remains the only schema source; generated Go is versioned and must not be edited by hand.

```sh
(cd backend && go tool gqlgen generate && go tool sqlc generate && go fmt ./...)
./tools/verify.sh backend
```

The backend verification runs Go format, vet, race tests, build, and a disposable gqlgen/sqlc diff. With Atlas it validates migration checksums; with Docker it also checks schema drift. Live PostgreSQL integration tests run only when `TEST_DATABASE_URL` is supplied:

```sh
set -a; . ./.env; set +a
TEST_DATABASE_URL="$DATABASE_URL" ./tools/verify.sh backend
```

It does not build or test Android, shared KMP, or iOS. Hand off any required app compatibility checks; do not run them as part of backend work.
