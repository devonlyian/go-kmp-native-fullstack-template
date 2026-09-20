---
name: design-app
description: 네이티브 앱 흐름·Figma 컴포넌트·화면 명세를 설계하거나 실제 UI를 검토하고, 프로덕션 코드를 바꾸지 않은 채 승인된 디자인을 앱 구현에 인계한다.
---

# 앱 디자인

[English](SKILL.md) | [한국어](SKILL.ko.md)

[디자인 규칙](../../../app/design/AGENTS.ko.md)을 따른다. 번역 관리 외에는 영어를 읽는다. 디자인 기록은 `app/design/`에 두며 백엔드 구현을 읽거나 앱 코드·GraphQL을 수정하지 않는다.

1. 디자인 전에 승인된 기능 기획에서 사용자 가치·흐름·대상 플랫폼·요청 화면·콘텐츠·UI 데이터 개념을 확인한다. 초안 제안과 이미 승인된 Figma·합의한 로컬 명세를 구분한다. GraphQL이나 백엔드 구현을 디자인 입력으로 읽지 않는다. 기존 API로 디자인을 미리 제한하지 말고 모호한 제품 결정은 기획의 빈 부분으로 기록한다.
2. 요청된 디자인 초안을 만들고 검토·확정한다. 기존 Foundation과 Figma 컴포넌트/Variant·Variable·Auto Layout은 재사용할 수 있지만 아직 `design-system-map.yaml`을 갱신하지 않는다. 상호작용을 억지로 같게 만들지 말고 Android/Material과 iOS/HIG의 네이티브 Navigation·Sheet·Picker·Safe Area를 유지한다. 관련 로딩·빈 데이터·오류·재시도·비활성·오프라인 상태를 포함한다. 새 디자인 결정은 다음 단계 전에 검토받되 기존 승인에 포함된 작업은 그 승인을 재사용한다. Figma 도구 호출 전에는 사용 가능한 기능을 확인하고 해당 작업에 필요한 선행 skill만 읽는다. 새 파일은 `figma-create-new-file`, 파일 문맥 읽기/쓰기는 `figma-use`, 레이아웃은 `figma-generate-design`, 컴포넌트/Token은 `figma-generate-library`, 디자인 문맥 조회 전에는 `figma-design-to-code`다. SwiftUI 변환에는 `figma-swiftui`를 사용한다. 각 skill의 선행 조건을 따른다. Figma 쓰기는 작업 권한이 필요하지만 이미 허용된 작업에 반복 확인을 요구하지 않는다. 도구나 접근 권한이 없으면 로컬 명세를 만들고 누락된 접근을 알리며 Figma 파일·노드를 지어내지 않는다. 유료 Code Connect는 선택 사항이며 요청되고 사용 가능할 때만 쓴다.
3. 디자인 확정 뒤 Design System을 만들거나 갱신한다. 기존 Foundation과 대상 네이티브 컴포넌트·화면을 살펴보고 Figma와 코드의 공용 `Component`, `Token`, `Layout` 이름을 확정한다. 화면마다 임의의 값을 쓰지 않고 의미 기반 색·타이포그래피·간격·반경 Token을 정의한다. 기능 전용 컴포넌트는 기능 안에 두며 실제 재사용이 필요한 공용 컴포넌트만 Design System에 둔다. 코드 추가는 앱 역할에 인계한다. 이 단계에서는 아직 `design-system-map.yaml`을 갱신하지 않는다.
4. 디자인과 Design System이 확정되면 필요한 입력·출력·nullability·실패 상태·동작 의미를 포함한 UI 데이터 요구사항을 GraphQL 명세 draft를 작성하는 app 범위에 인계한다. 디자인 역할은 GraphQL을 읽거나 수정하지 않는다. 계약 검토로 제품·UX 변경이 필요해지면 디자인을 조용히 바꾸지 말고 기획·디자인 검토로 돌아가 승인을 받는다.
5. GraphQL 명세가 확정된 뒤 마지막으로 `design-system-map.yaml`을 갱신한다. 승인된 Figma/Design System 이름, 실제 Android/iOS 컴포넌트·Token 이름, 실제 이름·동작 예외만 기록하며 GraphQL 필드는 맵에 넣지 않는다. 이후 Figma URL/노드 또는 합의한 로컬 명세, 승인 상태, 플랫폼 차이, Component/Token 이름, 매핑 예외, 상호작용 상태, 데이터 요구사항, 완료 조건을 인계한다. 시각 검토에서는 실제 Android/iOS 렌더링을 기준과 비교한다. 간격·글꼴/행간·줄바꿈·색·반경·Safe Area·다크 모드·글자 확대·접근성을 확인한다. 차이와 증거는 플랫폼별로 보고한다. 없는 렌더링은 앱 작업에 요청하고 백엔드 작업을 시작하지 않는다. Mock·매핑·렌더링하지 않은 디자인이 시각적 일치의 증거라고 주장하지 않는다.
