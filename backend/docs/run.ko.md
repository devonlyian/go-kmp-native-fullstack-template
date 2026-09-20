# API 실행

[English](run.md) | [한국어](run.ko.md)

[백엔드 설정](setup.ko.md)을 마친 뒤 저장소 루트에서 로컬 migration을 적용하고 API를 시작한다.

```sh
set -a; . ./.env; set +a
(cd backend && ../.tools/atlas migrate apply --env local && go run ./cmd/api)
```

다른 터미널에서 실행한다.

```sh
curl --fail http://localhost:8080/livez
curl --fail http://localhost:8080/readyz
curl --fail http://localhost:8080/graphql -H 'Content-Type: application/json' \
  --data '{"query":"query { systemStatus { databaseReady } }"}'
```

DB가 연결되면 `databaseReady`는 `true`이고 `/readyz`는 204다. DB가 없으면 `/livez`는 204이지만 `/readyz`는 503이고 GraphQL은 `databaseReady: false`를 반환한다. API는 기본으로 loopback에 바인딩한다. Ctrl+C로 API를 멈추고 `docker compose stop`으로 PostgreSQL을 멈춘다. 두 명령 모두 데이터 volume을 지우지 않는다.

통합 작업을 요청받은 경우 앱은 이미 실행 중인 이 contract endpoint를 사용할 수 있다. 앱 단독 또는 mock 개발에는 API 실행이 필요하지 않다.
