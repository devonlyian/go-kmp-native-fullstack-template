---
name: develop-backend
description: 루트 GraphQL 계약을 기준으로 backend의 Go·GraphQL·DB 동작을 구현한다. 앱 코드를 구현·조사하지 않으며 백엔드 범위의 기능 작업에 사용한다.
---

# 백엔드 개발

[English](SKILL.md) | [한국어](SKILL.ko.md)

1. [백엔드 규칙](../../../backend/AGENTS.ko.md), 관련 `backend/docs/features/` 메모와 루트 `contracts/graphql/`을 읽는다. 문서 쌍 관리나 명시적 요청 외에는 영어를 읽는다. app 코드·앱 안내는 불러오지 않으며 공통 API 기록은 요청된 계약 인계 때만 읽는다.
2. 새 기능은 [백엔드 양식](../../../backend/docs/features/_template.ko.md)으로 서버 동작을 정한다. 네이티브 앱 흐름 검증 뒤 app이 확인된 데이터 요구로 필요한 SDL 변경을 작성한다. 계약 인계의 구현 가능성·nullability·실패 의미를 검토하고 서버 구현 전에 app과 확정한다. 그때 [계약 인계](../../../docs/architecture.ko.md)를 따른다. 임시 fixture는 합의된 서버 동작이 아닌 예시다. 제품·UX 변경은 기획·디자인으로 되돌리며 앱 코드에서 요구를 추측하지 않는다. 계약 전용 검토에서는 서버 구현을 시작하지 않고 결정·남은 빈 부분을 보고한다.
3. 소유 도메인의 Application/Repository/GraphQL 경로를 구현하고 gqlgen을 재생성한다. 영속 데이터가 바뀔 때만 [DB](../../../backend/docs/database.ko.md)에 따라 SQL/Schema 수정과 sqlc 재생성을 한다. 생성 파일이나 적용된 Migration을 수정하지 않는다.
4. [백엔드 검사](../../../backend/docs/checks.ko.md)로 포맷·재생성·GraphQL 응답/오류·DB 동작을 검증한다. `./tools/verify.sh backend`를 실행하며 클라이언트를 빌드하지 않는다. 의존성 변경 때만 [의존성](../../../backend/docs/dependencies.ko.md)을 읽는다.
5. 백엔드 증거와 남은 계약·소비 코드 검사를 보고한다. 필요한 앱 변경은 app에 들어갈 권한이 아니라 인계 사항이다. [sync-docs](../sync-docs/SKILL.ko.md)로 관련 문서 쌍만 갱신하고 commit·PR은 요청받았을 때만 한다.
