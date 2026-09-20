# 데이터베이스 변경

[English](database.md) | [한국어](database.ko.md)

[백엔드 설정](setup.ko.md)을 마친다. `backend/db/schema/`와 `backend/db/migration/`이 데이터베이스 계약이고 `contracts/graphql/`는 GraphQL SDL의 유일한 원본이다.

영속 schema 또는 SQL query를 바꾼 뒤 저장소 루트에서 migration을 만들고 검토·적용하고 생성한다.

```sh
set -a; . ./.env; set +a
(cd backend && ../.tools/atlas migrate diff add_feature --env local)
(cd backend && ../.tools/atlas migrate apply --env local)
(cd backend && go tool sqlc generate)
```

`migrate diff`는 Docker의 임시 개발 데이터베이스를 사용한다. 이미 적용된 migration이나 checksum을 수정하지 않고 sqlc 출력도 직접 수정하지 않는다. 마지막으로 [백엔드 검사](checks.ko.md)를 실행한다.
