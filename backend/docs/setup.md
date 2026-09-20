# Backend setup

[English](setup.md) | [한국어](setup.ko.md)

Run commands from the repository root. Install the Go version declared by `backend/go.mod`, Docker with Compose, and Python 3. Docker runs only the local PostgreSQL service; Python supports structure checks.

Install the pinned Atlas v1.3.0 locally, with SHA-256 verification:

```sh
./tools/install-atlas.sh
```

For a local database, create the local environment file only when it is absent, then start PostgreSQL:

```sh
test -f .env || cp .env.example .env
docker compose up -d --wait
```

The `.env.example` password is a public local-development value and must never be used in production. Compose binds PostgreSQL to loopback. Next: [run the API](run.md) or [change the database](database.md).
