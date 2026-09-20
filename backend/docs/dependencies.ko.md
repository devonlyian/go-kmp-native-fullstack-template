# 백엔드 의존성

[English](dependencies.md) | [한국어](dependencies.ko.md)

표준 라이브러리로 시작하고 현재 요구사항에 필요할 때만 의존성을 추가한다. 인증, 캐시, 메시징, 관측 도구, 다른 데이터베이스, DI를 미리 설치하지 않는다.

애플리케이션이 직접 import하는 것은 `gqlgen`, `pgx/v5`, `gqlparser/v2`다. `gqlgen`과 `sqlc`는 고정된 생성 도구이기도 하다. MySQL, SQLite, gRPC, Zap을 포함한 간접 의존성은 선택한 앱 인프라가 아니라 도구 의존성이다. `// indirect` 항목은 Go가 관리하게 둔다.

의존성을 바꾸기 전 사용처를 확인한다.

```sh
(cd backend && go mod why -m github.com/jackc/pgx/v5 && go list -deps ./cmd/api && go mod tidy -diff)
```

`github.com/jackc/pgx/v5`는 검토할 모듈로 바꾼다. 제거가 타당하면 `go mod tidy`를 실행하고 다시 생성한 뒤 [백엔드 검사](checks.ko.md)를 실행한다.
