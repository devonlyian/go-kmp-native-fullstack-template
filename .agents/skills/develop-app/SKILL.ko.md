---
name: develop-app
description: 루트 GraphQL 계약과 계약에 맞는 Mock으로 KMP·Android·iOS 앱 동작을 구현한다. Go 백엔드를 조사하거나 구현하지 않는다.
---

# 앱 개발

[English](SKILL.md) | [한국어](SKILL.ko.md)

1. [앱 규칙](../../../app/AGENTS.ko.md), 관련 `app/docs/features/` 메모와 루트 `contracts/graphql/`을 읽는다. 문서 쌍 관리나 명시적 요청 외에는 영어를 사용한다. 백엔드 코드·SQL·서버 안내·영역 간 기능 기록은 읽지 않는다.
2. 새 기능은 [앱 양식](../../../app/docs/features/_template.ko.md)을 사용한다. 흐름·로딩/오류/재시도/취소·플랫폼·완료 조건을 기록하고 기존 계약을 재사용한다. 필드나 의미가 부족하면 승인된 디자인의 데이터 요구사항으로 SDL 변경 draft를 작성하고 backend 범위가 구현 가능성을 검토한다. 서버를 구현하거나 응답을 추측하지 않는다.
3. UI는 승인된 Figma나 합의된 디자인을 기록하고 기존 컴포넌트·Token을 재사용하며 실제 예외만 매핑한다. 승인된 인계를 사용하고 새 디자인 결정은 임의로 재설계하지 말고 [design-app](../design-app/SKILL.ko.md)에 전달한다. Figma 생성·수정은 요청된 경우에만 하고 새 디자인은 이미 승인되지 않았다면 구현 전 검토받는다. 승인된 기준이 없으면 화면 일치를 주장하지 않는다.
4. 앱 소유 GraphQL Operation을 수정하고 [앱 검사](../../../app/docs/checks.ko.md)로 Apollo를 재생성한다. 계약 확정 전에도 승인된 디자인의 데이터 개념으로 화면과 ViewModel을 스캐폴드할 수 있지만 Repository 연결은 확정된 계약에 대해서만 한다. Shared Domain/Data/Network와 요청된 네이티브 플랫폼을 구현한다. 서비스가 없으면 계약에 맞춘 Repository/HTTP Mock을 사용한다. Mock 서버 추가나 백엔드 기동이 필수는 아니다.
5. 앱 검사·관련 플랫폼 테스트 후 실제 화면·접근성을 검토한다. Shared 변경은 Android·iOS 모두 필요할 수 있다. 허용된 연결 검사는 제공된 API endpoint로 하고 Mock 검증과 실제 통합을 분리해 보고한다. [sync-docs](../sync-docs/SKILL.ko.md)로 증거와 상대 영역 인계를 기록한다. 앱 개발의 일부로 백엔드 검사를 실행하거나 Go 코드를 고치지 않는다.
