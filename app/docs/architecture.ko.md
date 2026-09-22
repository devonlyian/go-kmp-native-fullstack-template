# 앱 아키텍처

[English](architecture.md) | [한국어](architecture.ko.md)

UI 작업은 승인된 Figma 파일·합의된 로컬 명세를 사용한 승인 디자인·Design System·토큰 대응에서 시작한다. 계약 전용·GraphQL 연결·그 밖의 비-UI 작업에는 디자인 선행 조건이 필요하지 않다. 새 GraphQL 계약을 만들기 전에 로컬 fixture·테스트 대역으로 네이티브 흐름을 구현·검증한다. 흐름 검증 뒤 app이 필요한 루트 `contracts/graphql/` 변경을 작성하고 backend가 검토해 서버 구현 전에 app과 확정한다. 이후 앱은 Apollo Operation으로 합의된 SDL을 소비한다. 서버의 저장 방식이나 resolver 구현에 의존해서 앱을 설계하지 않는다. 앱 코드와 관련 계약 설명만 읽는다.

| 위치 | 책임 |
| --- | --- |
| `app/shared/` | Domain 모델·Repository 계약·UseCase·Data/Network·생성 GraphQL 클라이언트 |
| `app/androidApp/` | Compose·Android ViewModel·lifecycle·Navigation·네이티브 UI 상태 |
| `app/iosApp/` | SwiftUI·네이티브 Observation·lifecycle·Navigation·네이티브 UI 상태 |
| `app/design/` | Component/Token 이름과 실제 매핑 예외 |

Shared에는 Presentation을 두지 않는다. 계약 전에는 승인된 제품 개념에서 이름을 정하고 계약 확정 때 조율하며 Swift의 PascalCase 디렉터리도 동일 기능이다. `system`으로 시작하고 실제 요구가 있을 때만 도메인·Navigation을 추가한다. 백엔드 DDD 계층을 UI 모듈에 복제하지 않는다.

계약 합의 전에는 앱 소유 모델·로컬 Repository 테스트 대역으로 실제 Navigation·상태·로컬 동작을 검증한다. fixture와 원격 동작 가정은 임시로 표시하며 두 번째 API 명세가 아니다. 합의 뒤 모델·fixture를 맞추고 루트 SDL에서 앱 소유 Operation을 생성해 GraphQL adapter를 연결한다. 정상 false/빈 데이터·GraphQL 오류·전송 오류·취소를 구분한다. 실행 서비스가 없으면 계약에 맞춘 Repository 또는 HTTP 테스트 대역을 사용하며 독립 Mock 서버는 필요하지 않다. 백엔드 완성 뒤 제공된 endpoint에서 요청된 검사가 통과할 때까지 실제 API 통합은 미검증으로 기록한다.

UI 변경은 승인된 Figma 파일·합의된 로컬 명세 중 해당 원본과 Design System 참조를 사용한다. GraphQL과 독립적으로 앱 개발 전에 의미 기반 Token·컴포넌트를 맞추고 계획된 네이티브 심볼은 구현 전까지 디자인 인계에 두며 실제 매핑 예외만 기록한다. 실제 화면·글자 확대·다크 모드·접근성을 검토한다. 이 템플릿에는 승인된 Figma 파일이나 Code Connect 연결이 없으며 매핑은 픽셀 일치를 증명하지 않는다.

[develop-app](../../.agents/skills/develop-app/SKILL.ko.md), [앱 검사](checks.ko.md), 해당 [Android](android.ko.md) 또는 [iOS](ios.ko.md) 안내를 사용한다. 실기기 성능·카메라 동작·배터리·서명·배포에는 별도 증거가 필요하다.
