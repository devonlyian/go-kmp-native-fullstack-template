# 개발 영역

[English](index.md) | [한국어](index.ko.md)

한 영역을 선택한다. 번역 작업이나 명시적 요청 외에는 영어만 읽는다. README는 프로젝트 소개이며 개발 진입점이 아니다.

새 기능은 [작업 흐름](architecture.ko.md)에 따라 기획 → Figma Make 디자인 → Make 산출물 기반 Design System → 토큰 매칭 → 네이티브 앱 개발 → GraphQL 계약 생성 → 백엔드 개발 순서로 진행한다. 승인된 산출물·기존 계약은 재사용하고 한정된 수정은 요청된 단계부터 진행한다.

| 작업 | 진입점 |
| --- | --- |
| 기획: 제품 가치·범위·흐름·완료 조건 | [plan-feature](../.agents/skills/plan-feature/SKILL.ko.md), [기획 양식](plans/_template.ko.md) |
| 백엔드: Go·GraphQL 서버·DB | [백엔드 문서](../backend/docs/index.ko.md) |
| 앱: KMP·Android·iOS | [앱 문서](../app/docs/index.ko.md) |
| 디자인: Figma Make 산출물·Design System·토큰 매칭·시각 명세 인계 | [디자인 규칙](../app/design/AGENTS.ko.md), [design-app](../.agents/skills/design-app/SKILL.ko.md) |
| 에이전트·종료 훅 설정 | [자동화](guides/automation.ko.md) |
| 공통 API 결정·인계 | 루트 `contracts/graphql/`과 [계약 경계](architecture.ko.md) |
| 새 저장소 설정 | [템플릿 사용](guides/new-project.ko.md) |
| 문서 관리 | [sync-docs](../.agents/skills/sync-docs/SKILL.ko.md) |

백엔드와 앱은 서로의 구현을 읽어 개발하지 않는다. 앱은 계약 생성 전에 임시 로컬 fixture로 네이티브 흐름을 검증하고 GraphQL 연동·백엔드 구현에는 합의된 SDL을 사용한다. 상대 영역의 남은 일은 인계한다. 전체 스택 통합은 별도로 요청한다.

[버전 근거](versions.ko.md)는 버전 조사 때만, [과거 검증](verification.ko.md)이나 [system 통합 시나리오](features/system.ko.md)는 통합·이력 작업 때만 읽는다. 필수 시작 문서가 아니다.
