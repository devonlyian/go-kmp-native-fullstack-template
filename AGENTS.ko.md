# 공통 프로젝트 규칙

[English](AGENTS.md) | [한국어](AGENTS.ko.md)

- 기본으로 영어를 읽고 한국어는 번역 수정·검토 또는 명시적 요청 때만 읽는다. 대화는 한국어로 한다. Markdown 변경은 [sync-docs](.agents/skills/sync-docs/SKILL.ko.md)를 사용해 두 언어를 검토하고 기록한다.
- 요청된 한 영역에서 작업한다: [기획](.agents/skills/plan-feature/SKILL.ko.md), [백엔드](backend/AGENTS.ko.md), [앱](app/AGENTS.ko.md), [디자인](app/design/AGENTS.ko.md). 해당 영역의 읽기·쓰기 경계를 따르며 기획은 구현이나 공통 계약을 조사하지 않는다. 사용자가 명시적으로 요청하지 않으면 다른 영역으로 확장하지 않는다. 대상이 불명확하면 구현 전에 확인한다.
- 새 기능 순서는 승인된 기획 → Figma Make 디자인 → Make 산출물 기반 Design System → 디자인 토큰 매칭 → 네이티브 앱 개발 → GraphQL 계약 생성 → 백엔드 개발이다. [작업 흐름과 계약 경계](docs/architecture.ko.md)를 따르며 기존 기능은 승인된 산출물을 재사용하고 요청된 단계부터 진행한다.
- `contracts/graphql/`이 유일한 공통 API 기준이다. 새 계약을 만들기 전에 로컬 fixture·테스트 대역으로 앱 흐름을 검증하며 이 데이터는 임시 앱 데이터이지 API 보장이 아니다. GraphQL 연동이나 의존하는 백엔드 구현 전에 입력·출력·nullability·실패 의미를 합의하고 동작은 SDL 설명으로 정의한다. 계약 변경과 인계는 따로 처리하며 상대 구현을 역추적하거나 몰래 함께 바꾸지 않는다.
- 생성 코드를 직접 수정하지 않는다. 기존 코드를 재사용하고 현재 요구에 필요한 의존성만 추가한다. 사용자 작업과 hook을 보존하며 비밀정보·로컬 환경 파일·자격 증명·빌드 산출물을 노출하거나 커밋하지 않는다.
- 기존 `dev`에서 `feat/`, `fix/`, `chore/`, `docs/`로 분기하고 PR은 `dev`, 릴리스는 `dev` → `main`을 따른다. 사용자 요청 없이 commit·push·PR·remote 생성·라이선스 선택을 하지 않는다.

README는 교체 가능한 프로젝트 정보이며 에이전트 지침 원본이 아니다. [docs/index.ko.md](docs/index.ko.md)에서 자기 영역의 문서를 선택한다. 영역별 검사를 실행하며 전체 스택 검증은 명시적으로 요청된 별도 작업이다. 문서만 변경하면 `./tools/verify.sh structure`를 사용한다.

위임할 때는 `.codex/agents/`의 해당 `planning`·`backend`·`app`·`design` 역할을 쓰고 모든 역할을 자동으로 실행하지 않는다. 한정된 작업·허용 경로·관련 기획/계약/디자인 참조·완료 조건만 전달하고 새 문맥을 사용할 수 있으면 전체 이력 복사를 피한다. 설정이나 훅 관리 때만 [자동화](docs/guides/automation.ko.md)를 읽는다.
