# 백엔드 아키텍처

[English](architecture.md) | [한국어](architecture.ko.md)

백엔드 경계 결정 때 읽는다. 루트 `contracts/graphql/`을 기준으로 개발하고 앱 구현을 조사하지 않는다.

## 모듈러 모놀리스와 도메인 경계

백엔드는 **GraphQL 우선 모듈러 모놀리스(Modular Monolith)**를 사용한다. 도메인 모듈들이 하나의 Go API 프로세스 안에서 실행되며 백엔드 배포 단위도 하나다. 모듈은 애플리케이션 내부의 도메인 경계이며 별도 서비스나 별도 `go.mod`가 아니다. 현재는 `system`만 존재하며, 실제 요구사항에 따라 도메인을 추가할 때 사용할 경계 규칙을 제공한다.

DDD의 Bounded Context와 도메인 소유권 개념으로 경계를 정한다. 화면이나 endpoint 하나만으로 새 도메인을 만들지는 않는다. Aggregate, Domain Event, Repository interface 등은 지금 구현하는 요구사항에 필요할 때만 추가한다.

| 위치 | 책임 |
| --- | --- |
| `backend/internal/<domain>/domain` | 도메인 모델과 비즈니스 규칙. HTTP·GraphQL·SQL 관심사를 포함하지 않음 |
| `backend/internal/<domain>/application` | 공개 UseCase, 도메인 로직과 데이터 접근의 조율 |
| `backend/internal/<domain>/repository` | sqlc·pgx를 통한 해당 도메인의 데이터 접근 |
| `backend/internal/<domain>/graphql` | GraphQL 어댑터. Application에 UseCase를 위임하고 API 결과를 매핑 |
| `backend/cmd/api/main.go` | 의존성을 수동 생성·연결하고 API 프로세스를 시작 |

현재 요청의 실행 흐름은 다음과 같다.

```text
POST /graphql: systemStatus
  → system GraphQL resolver
  → application.Service.Status
  → repository.Repository.DatabaseReady
  → sqlc-generated query / pgx
  → PostgreSQL
```

이것은 실행 중 호출 순서이며 Domain이 Application이나 Repository에 의존하라는 의미가 아니다. 현재의 작은 Application service는 구체 Repository를 사용하며 아키텍처 이름을 맞추기 위해 interface를 추가할 필요는 없다.

도메인이 늘어나면 다른 도메인은 공개 Application API를 통해서만 호출한다. 다른 도메인의 Repository를 import하거나 소유 데이터에 직접 SQL을 실행하거나 생성된 DB 접근 코드로 경계를 우회하지 않는다. PostgreSQL 인스턴스를 공유해도 데이터 소유권 경계는 유지한다. 모듈 사이에는 일반 Go 함수 호출을 사용한다. 독립 배포·확장·장애 격리가 실제로 필요할 때 독립 서비스와 네트워크 프로토콜을 검토하며, 서비스 분리 자체를 목표로 삼지 않는다.

GraphQL 계약은 `contracts/graphql/`의 도메인별 SDL 파일로 관리하고 하나의 공개 API를 구성한다. `backend/graph/schema`를 두 번째 원본으로 추가하지 않는다. 현재 gqlgen 생성 결과는 `system` 아래에 있다. 두 번째 Context가 필요해지면 새 도메인 로직을 `system`에 몰아넣지 말고 해당 변경에서 resolver 조립과 생성 코드 위치를 함께 검토한다.

[백엔드 개발](../../.agents/skills/develop-backend/SKILL.ko.md)을 따른다. 현재 요구에 필요한 의존성만 추가하며 [의존성](dependencies.ko.md)을 참고한다.
