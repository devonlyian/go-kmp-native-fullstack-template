# 디자인 규칙

[English](AGENTS.md) | [한국어](AGENTS.ko.md)

범위는 `app/design/`의 디자인 명세, `design-system-map.yaml`, 그리고 권한이 있는 Figma 디자인 작업이다. 디자인 에이전트는 백엔드·앱 에이전트와 분리한다.

- 디자인 중에는 백엔드 소스와 루트 GraphQL SDL을 읽지 않고 프로덕션 앱 코드, 공통 로직, GraphQL, 생성 파일을 수정하지 않는다. 승인된 기능 기획과 사용자 요구사항에서 시작한다. 재사용과 시각 검토를 위해 기존 Android/iOS 디자인 시스템 컴포넌트와 대상 화면을 필요한 범위에서 읽을 수 있다.
- 승인된 기능 기획 → 디자인 초안·검토·확정 → Design System 정의 → app 범위가 작성하는 GraphQL 명세 draft → `design-system-map.yaml` 갱신 순서로 작업한다. 기존 GraphQL로 디자인을 미리 제한하지 않는다. 계약 작업에서 제품·UX의 빈 부분이 드러나면 디자인 범위 안에서 임의로 해결하지 않고 기획·디자인 결정으로 되돌린다.
- 승인된 Figma를 시각 기준으로 다룬다. 사용자가 권한을 준 Figma 수정은 반복 승인 없이 진행할 수 있다. 그 외에는 로컬에서 작업하고, 접근할 수 없을 때 파일·노드·토큰·컴포넌트의 존재를 추정하지 않는다.
- Figma와 코드에서 `Component`, `Token`, `Layout` 이름을 맞춘다. 기존 네이티브 컴포넌트를 먼저 검색한다. 디자인·Design System·GraphQL 명세가 확정된 뒤에만 최종 플랫폼 매핑 또는 실제 이름·동작 예외를 `design-system-map.yaml`에 갱신하며, 이 맵에는 GraphQL 필드를 넣지 않는다.
- Android는 Compose/Material, iOS는 SwiftUI/HIG에 맞게 설계한다. 여러 기능에서 실제 재사용되기 전까지 기능 컴포넌트는 기능 범위에 둔다.
- 승인된 디자인은 상태, 매핑, 예외, 스크린샷 기반 Visual QA 기준과 함께 앱 에이전트에 인계한다. 렌더링된 스크린샷은 시각 검토의 근거이며 Mock은 시각적 일치의 증거가 아니다.

작업 흐름은 [design-app](../../.agents/skills/design-app/SKILL.ko.md)을 사용한다.
