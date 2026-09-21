# 백엔드 규칙

[English](AGENTS.md) | [한국어](AGENTS.ko.md)

범위는 `backend/`, 해당 문서·백엔드 도구/설정, 앱이 작성한 루트 `contracts/graphql/` draft의 검토·확정이다. API 요구를 알아내려고 `app/`를 읽거나 수정하지 않는다. SDL과 그 설명이 앱에 제공하는 계약이며 부족한 동작 정의는 구현 전에 기록한다.

- GraphQL 우선 모듈러 모놀리스: 하나의 API 프로세스에 `internal/<domain>/{domain,application,repository}`를 두고, gqlgen 생성 코드와 스키마별 resolver 파일을 담는 공유 GraphQL transport 패키지 `internal/graphql`을 함께 둔다. Resolver는 Application을 호출하고 Repository가 pgx/sqlc를 담당한다. `cmd/api`에서 수동 연결하며 다른 도메인은 공개 Application API로 호출하고 Repository나 직접 SQL로 접근하지 않는다.
- 네이티브 앱 흐름 검증 뒤 앱 범위가 확인된 데이터 요구로 필요한 SDL draft를 작성한다. 계약 인계의 구현 가능성·nullability·실패 의미를 검토한 뒤 백엔드 구현 전에 app과 계약을 확정한다. 임시 앱 fixture는 합의된 서버 동작이 아닌 예시로 다룬다. 불가능하거나 모호한 요구는 표시하고 제품·UX 변경은 기획·디자인으로 되돌린다. 계약 전용 검토에서는 서버 구현을 시작하지 않는다.
- 계약과 같은 짧은 소문자 단수형 도메인 이름을 쓴다. 초기 도메인은 `system`, Operation은 `systemStatus`다. 예시 비즈니스 도메인이나 사용하지 않는 DDD 패턴은 추가하지 않는다.
- 루트 SDL에서 gqlgen으로 Go를, sqlc로 SQL 접근 코드를 생성한다. 생성 Go는 버전 관리한다. 고정 `.tools/atlas`로 추가형 Migration을 관리하며 적용된 Migration을 수정하거나 checksum으로 감추지 않는다.
- 기존 코드와 표준 라이브러리를 우선한다. 의존성 변경 때만 [의존성](docs/dependencies.ko.md)을 읽는다. HTTP 검사는 `net/http/httptest`, DB 통합은 `TEST_DATABASE_URL`을 사용하고 없으면 생략한다. 연결 URL을 출력하지 않는다.

구현은 [develop-backend](../.agents/skills/develop-backend/SKILL.ko.md), 설치·아키텍처·검사는 [백엔드 문서](docs/index.ko.md)를 따른다. 기본 검증은 루트의 `./tools/verify.sh backend`다. 클라이언트를 빌드하지 않고 GraphQL 요청·응답을 자체 검사한다. 앱 호환성 검사는 완료로 주장하거나 작업에 자동 추가하지 말고 인계할 미검증 항목으로 보고한다.
