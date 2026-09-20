# Run the API

[English](run.md) | [한국어](run.ko.md)

Complete [backend setup](setup.md), then apply local migrations and start the API from the repository root:

```sh
set -a; . ./.env; set +a
(cd backend && ../.tools/atlas migrate apply --env local && go run ./cmd/api)
```

In another terminal:

```sh
curl --fail http://localhost:8080/livez
curl --fail http://localhost:8080/readyz
curl --fail http://localhost:8080/graphql -H 'Content-Type: application/json' \
  --data '{"query":"query { systemStatus { databaseReady } }"}'
```

With a database, `databaseReady` is `true` and `/readyz` returns 204. Without one, `/livez` remains 204, `/readyz` returns 503, and GraphQL returns `databaseReady: false`. The API binds to loopback by default. Stop it with Ctrl+C and stop PostgreSQL with `docker compose stop`; neither command deletes the data volume.

An app can consume this already running contract endpoint when integration is requested. Running it is not a prerequisite for app-only or mock development.
