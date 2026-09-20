# 백엔드 검사

[English](checks.md) | [한국어](checks.ko.md)

명령은 저장소 루트에서 실행한다. 루트 SDL만 schema 원본이며, 생성된 Go 코드는 버전 관리하고 직접 수정하지 않는다.

```sh
(cd backend && go tool gqlgen generate && go tool sqlc generate && go fmt ./...)
./tools/verify.sh backend
```

백엔드 검증은 Go 포맷, vet, race test, build와 일회용 gqlgen/sqlc diff를 실행한다. Atlas가 있으면 migration checksum을 검증하고 Docker가 있으면 schema drift도 검사한다. live PostgreSQL 통합 테스트는 `TEST_DATABASE_URL`을 제공할 때만 실행한다.

```sh
set -a; . ./.env; set +a
TEST_DATABASE_URL="$DATABASE_URL" ./tools/verify.sh backend
```

Android, shared KMP, iOS는 빌드하거나 테스트하지 않는다. 필요한 앱 호환성 검사는 인계하고 백엔드 작업의 일부로 실행하지 않는다.
