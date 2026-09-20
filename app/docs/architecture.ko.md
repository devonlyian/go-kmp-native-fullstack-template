# 앱 아키텍처

[English](architecture.md) | [한국어](architecture.ko.md)

앱은 Apollo Operation으로 루트 `contracts/graphql/`을 소비한다. 서버의 저장 방식이나 resolver 구현에 의존해서 앱을 설계하지 않는다. 앱 코드와 계약 설명만 읽는다.

| 위치 | 책임 |
| --- | --- |
| `app/shared/` | Domain 모델·Repository 계약·UseCase·Data/Network·생성 GraphQL 클라이언트 |
| `app/androidApp/` | Compose·Android ViewModel·lifecycle·Navigation·네이티브 UI 상태 |
| `app/iosApp/` | SwiftUI·네이티브 Observation·lifecycle·Navigation·네이티브 UI 상태 |
| `app/design/` | Component/Token 이름과 실제 매핑 예외 |

Shared에는 Presentation을 두지 않는다. 계약에서 이름을 정하며 Swift의 PascalCase 디렉터리도 동일 기능이다. `system`으로 시작하고 실제 요구가 있을 때만 도메인·Navigation을 추가한다. 백엔드 DDD 계층을 UI 모듈에 복제하지 않는다.

SDL에서 앱 소유 Operation과 fixture를 만들고 정상 false/빈 데이터·GraphQL 오류·전송 오류·취소를 구분한다. 실행 서비스가 없으면 계약에 맞춘 Repository 또는 HTTP 테스트 대역을 사용한다. 이는 개발·테스트 방식이며 독립 Mock 서버가 설치됐다는 뜻이 아니다. 제공된 endpoint로 확인하기 전까지 실제 API 통합은 미검증으로 기록한다.

UI 변경은 구현 전에 승인된 Figma나 합의된 디자인을 정하고 기존 네이티브 컴포넌트·의미 기반 Token을 재사용하며 실제 화면·글자 확대·다크 모드·접근성을 검토한다. 이 템플릿에는 승인된 Figma 파일이나 Code Connect 연결이 없으며 매핑은 픽셀 일치를 증명하지 않는다.

[develop-app](../../.agents/skills/develop-app/SKILL.ko.md), [앱 검사](checks.ko.md), 해당 [Android](android.ko.md) 또는 [iOS](ios.ko.md) 안내를 사용한다. 실기기 성능·카메라 동작·배터리·서명·배포에는 별도 증거가 필요하다.
