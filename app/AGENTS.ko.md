# 앱 규칙

[English](AGENTS.md) | [한국어](AGENTS.ko.md)

범위는 `app/`(Shared·Android·iOS), 해당 문서·앱 도구/설정, 루트 `contracts/graphql/`이다. 앱 동작을 추측하려고 Go resolver·Repository·DB Schema·백엔드 문서를 읽지 않는다. SDL과 그 설명을 소비하며 계약의 빈 부분은 추측하거나 서버를 구현하는 대신 보고한다.

- KMP는 Domain/Data/Network만 공유한다. `shared/`에 Compose·SwiftUI·ViewModel·Navigation·화면 상태를 두지 않는다. Android는 Compose/ViewModel, iOS는 SwiftUI/네이티브 `@Observable` 상태를 쓴다.
- Shared·Android `feature/<domain>`과 Swift `Features/<Domain>`의 이름을 계약에 맞춘다. 짧은 소문자 단수형 이름을 쓰고 Swift는 PascalCase다. 초기 기능은 `system`이며 예시 비즈니스 도메인을 추가하지 않는다.
- Apollo는 루트 SDL을 직접 읽는다. 앱 소유 Operation만 수정하고 클라이언트 타입을 생성한다. 생성 Kotlin은 빌드 산출물에 둔다. 백엔드 구현이나 DB 변경은 앱 작업에 포함되지 않는다.
- API가 없으면 계약에 맞는 응답·Mock으로 개발하고 데이터·GraphQL/전송 오류·nullability·취소를 다룬다. 연결 검사는 제공된 API endpoint가 있을 때 사용한다. Mock은 서버 호환성 증거가 아니며 UI 작업을 진행하려고 백엔드 개발을 시작하지 않는다.
- UI는 승인된 Figma나 합의된 디자인을 기록하고 같은 이름의 네이티브 컴포넌트와 `design/design-system-map.yaml` Token을 재사용하며 실제 예외만 매핑한다. 의미 기반 색·간격·반경은 Design System에 둔다.

[develop-app](../.agents/skills/develop-app/SKILL.ko.md)과 [앱 문서](docs/index.ko.md)를 사용한다. Shared/Android는 `./tools/verify.sh app`, Swift/Apple 연동은 `./tools/verify.sh ios`와 관련 플랫폼 테스트·실제 화면/접근성 검토를 실행한다. Shared 변경은 양쪽 앱 플랫폼 검사가 필요할 수 있지만 백엔드 검사는 필요하지 않다. 서버·앱 전체 통합은 명시적으로 요청된 별도 작업이다.

디자인 전용 작업은 [디자인 규칙](design/AGENTS.ko.md)과 [design-app](../.agents/skills/design-app/SKILL.ko.md)을 따르며 앱 구현·빌드 없이 디자인을 인계한다. 앱 역할은 승인된 인계를 구현하고 새 디자인 결정은 디자인 역할에 전달한다.
