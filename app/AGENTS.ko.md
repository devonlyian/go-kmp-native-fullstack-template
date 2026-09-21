# 앱 규칙

[English](AGENTS.md) | [한국어](AGENTS.ko.md)

범위는 `app/`(Shared·Android·iOS), 해당 문서·앱 도구/설정, 이 범위가 소유하는 루트 `contracts/graphql/` 계약 draft이다. 앱 동작을 추측하려고 Go resolver·Repository·DB Schema·백엔드 문서를 읽지 않는다. SDL과 그 설명을 소비하며 계약의 빈 부분은 추측하거나 서버를 구현하는 대신 보고한다.

- KMP는 Domain/Data/Network만 공유한다. `shared/`에 Compose·SwiftUI·ViewModel·Navigation·화면 상태를 두지 않는다. Android는 Compose/ViewModel, iOS는 SwiftUI/네이티브 `@Observable` 상태를 쓴다.
- Shared·Android `feature/<domain>`과 Swift `Features/<Domain>`에서 기능 이름을 일관되게 사용한다. 계약 전에는 승인된 제품 개념에서 이름을 정하고 계약 확정 때 조율한다. 짧은 소문자 단수형 이름을 쓰고 Swift는 PascalCase다. 초기 기능은 `system`이며 예시 비즈니스 도메인을 추가하지 않는다.
- UI 작업은 디자인·Design System·토큰 대응이 승인되면 네이티브 흐름을 개발하며 Make 산출물·기존 승인 Figma·합의된 로컬 명세를 사용한다. 계약 전용·GraphQL 연결·그 밖의 비-UI 변경은 디자인 선행 조건 없이 요청된 단계부터 진행한다. 새 API 계약이 없어도 로컬 fixture·Repository 테스트 대역으로 동작하는 화면·Navigation·상태·로컬 동작을 구현하고 데이터·원격 동작 가정은 임시로 표시한다. 계약이 없다고 앱 작업을 뼈대 제작에 제한하지 않는다. 해당하는 기존 계약과 계약에 맞춘 Mock이 있으면 재사용한다.
- 앱 흐름 검증 뒤 요청된 계약 단계에서 확인된 데이터 요구로 필요한 루트 SDL 변경 draft를 작성한다. backend 영역은 구현 가능성을 검토하고 서버 작업 전에 app과 계약을 확정한다. 합의 뒤 앱 모델·fixture를 맞추고 앱 소유 Operation 수정, Apollo 재생성, GraphQL adapter 연결을 진행한다. Apollo는 루트 SDL을 직접 읽으며 생성 Kotlin은 빌드 산출물에 둔다. 백엔드 구현·DB 변경은 앱 작업이 아니다.
- UI는 승인된 Make 산출물·기존 승인 Figma 디자인·합의된 로컬 명세 중 해당 원본과 Design System 참조를 사용하며 네이티브 컴포넌트와 `design/design-system-map.yaml` Token을 재사용한다. 토큰 매칭은 앱 개발보다 앞서며 GraphQL 승인이 필요하지 않다. 계획된 네이티브 심볼은 구현한 뒤 실제 매핑 예외에 기록한다. 의미 기반 색·타이포그래피·간격·반경은 Design System에 둔다.

[develop-app](../.agents/skills/develop-app/SKILL.ko.md)과 [앱 문서](docs/index.ko.md)를 사용한다. Shared/Android는 `./tools/verify.sh app`, Swift/Apple 연동은 `./tools/verify.sh ios`와 관련 플랫폼 테스트·실제 화면/접근성 검토를 실행한다. Shared 변경은 양쪽 앱 플랫폼 검사가 필요할 수 있지만 백엔드 검사는 필요하지 않다. 임시 fixture·계약에 맞춘 Mock·실제 endpoint 증거를 구분하고 관련 nullability·오류·취소를 다룬다. Mock은 서버 호환성 증거가 아니다. 백엔드 완성 뒤 제공된 endpoint로 요청된 연결 검사를 마무리하며 서버·앱 전체 통합은 명시적으로 요청된 별도 작업이다.

디자인 전용 작업은 [디자인 규칙](design/AGENTS.ko.md)과 [design-app](../.agents/skills/design-app/SKILL.ko.md)을 따르며 앱 구현·빌드 없이 디자인을 인계한다. 앱 역할은 승인된 인계를 구현하고 새 디자인 결정은 디자인 역할에 전달한다.
