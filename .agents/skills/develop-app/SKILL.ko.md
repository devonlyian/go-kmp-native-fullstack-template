---
name: develop-app
description: 승인된 디자인과 토큰 매핑으로 네이티브 KMP·Android·iOS 앱 흐름을 구현·검증한 뒤 필요한 GraphQL 계약을 작성하고 합의된 SDL로 연동한다. Go 백엔드를 조사하거나 구현하지 않는다.
---

# 앱 개발

[English](SKILL.md) | [한국어](SKILL.ko.md)

1. [앱 규칙](../../../app/AGENTS.ko.md)과 관련 `app/docs/features/` 메모를 읽고 UI 작업에는 승인된 디자인·Design System·토큰 인계도 읽는다. 기존 작업은 요청된 단계부터 진행하며 승인된 Figma나 합의된 로컬 기준을 다시 만들지 않고 재사용한다. 문서 쌍 관리나 명시적 요청 외에는 영어를 사용한다. API 계약을 재사용하거나 만들 때 루트 `contracts/graphql/`을 읽으며 기능 계약이 없어도 네이티브 앱 개발은 진행한다. 백엔드 코드·SQL·서버 안내는 읽지 않는다. 공통 API 기록은 요청된 계약 인계 때만 읽는다.
2. 새 기능은 [앱 양식](../../../app/docs/features/_template.ko.md)을 사용한다. 흐름·로딩/오류/재시도/취소·플랫폼·완료 조건을 기록한다. UI 작업은 승인된 Figma 파일·합의된 로컬 명세를 확정된 Design System·토큰 대응에 따라 네이티브 Compose·SwiftUI로 구현한다. 기존 컴포넌트를 재사용하고 계획된 네이티브 심볼은 구현한 뒤 실제 매핑 예외에 기록한다. 새 디자인 결정은 [design-app](../design-app/SKILL.ko.md)에 전달한다. Figma 생성·수정은 요청된 경우에만 하며 작업을 포함하는 기존 승인을 재사용한다. 승인된 기준이 없으면 화면 일치를 주장하지 않는다.
3. 앱 소유 로컬 fixture나 Repository 테스트 대역으로 동작하는 화면·Navigation·상태·로컬 동작과 필요한 Shared Domain/Data 모델을 구현·검증한다. 기능 API가 아직 합의되지 않았다면 임시 데이터임을 표시하고 가정·관찰된 데이터 요구를 기록하며 새 API Operation을 생성하거나 서버 의미를 확정됐다고 주장하지 않는다. 이 단계는 화면 뼈대 제작에 그치지 않으며 백엔드 기동이나 Mock 서버가 필요하지 않다. 기존 계약으로 기능을 충족하면 해당 계약과 계약에 맞춘 Mock을 재사용한다.
4. 앱 흐름 검증 뒤 요청된 별도 계약 단계에서 필요한 GraphQL 계약을 만든다. 확인한 동작·데이터·nullability·실패 요구로 루트 SDL을 작성하고 [계약 인계](../../../docs/architecture.ko.md)를 따른다. backend는 앱 소스를 읽지 않고 구현 가능성을 검토한다. 제품·UX 변경은 기획·디자인으로 되돌린다. 합의되면 앱 모델·fixture를 맞추고 앱 소유 Operation 수정, [앱 검사](../../../app/docs/checks.ko.md)에 따른 Apollo 재생성, GraphQL Data/Network adapter 연결을 진행한다. 합의 전에는 로컬 테스트 대역을 유지하고 인계 사항을 기록한다. 완전히 로컬인 기능에는 GraphQL 작업이 필요하지 않다.
5. 앱 검사·관련 플랫폼 테스트 후 승인된 기준에 따라 실제 화면·접근성을 검토한다. Shared 변경은 Android·iOS 모두 필요할 수 있다. 임시 fixture·계약에 맞춘 Mock·실제 API 증거를 구분해 보고한다. 백엔드 완성 뒤 요청된 연결 검사는 제공된 endpoint로 하며 전체 통합은 별도 요청 작업으로 유지한다. [sync-docs](../sync-docs/SKILL.ko.md)로 증거와 남은 작업을 기록한다. 앱 개발의 일부로 백엔드 검사를 실행하거나 Go 코드를 고치지 않는다.
