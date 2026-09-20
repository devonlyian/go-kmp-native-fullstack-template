# Feature: system

[English](system.md) | [한국어](system.ko.md)

명시적으로 요청된 서버·앱 end-to-end 작업용 통합 참고 자료다. 일반 백엔드·앱 개발은 자기 영역 기록과 루트 SDL을 사용하며 이 영역 간 구현 기록을 읽을 필요가 없다.

## 목표와 사용자 가치

앱에서 서버의 PostgreSQL 연결 상태를 확인하고, 장애 복구 후 `Refresh`로 최신 상태를 다시 확인한다. 이 기능은 GraphQL → KMP → Android/iOS 화면 연결을 검증하는 템플릿의 최소 기능이다.

범위는 현재 연결 상태 조회와 수동 새로고침이다. 인증, 제품 데이터, 상태 이력, 자동 polling, 운영 모니터링은 포함하지 않는다.

## User Flow와 화면 목록

Android와 iOS 모두 `SystemStatusScreen`에서 다음 흐름을 제공한다.

화면 진입 → 로딩 → DB 상태 또는 요청 오류 표시 → `Refresh` → 로딩 → 최신 결과 표시.

| 조건 | 계약 및 서버 응답 | Android·iOS에서 확인할 결과 |
| --- | --- | --- |
| API와 DB 정상 | `databaseReady: true`, `/livez` 204, `/readyz` 204 | `Database ready` |
| API는 실행 중이고 DB 연결 실패 | `databaseReady: false`, `/livez` 204, `/readyz` 503 | `Database not ready` |
| DB 연결 복구 후 `Refresh` | `databaseReady: true`, `/readyz` 204 | `Database not ready`가 `Database ready`로 바뀜 |
| API 중단·오프라인 또는 GraphQL 요청 오류 | 유효한 상태 결과를 얻지 못함 | `Unable to load system status.` |
| API 연결과 DB 정상 복구 후 `Refresh` | `databaseReady: true` | 오류 문구가 사라지고 `Database ready`로 바뀜 |

조회 중에는 로딩 표시와 `Loading system status` 접근성 레이블을 제공한다. 요청 중 반복해서 누른 `Refresh`는 중복 요청을 시작하지 않는다. 자동 재시도는 없으며, 서버 상태가 바뀐 뒤 사용자가 다시 조회한다.

DB 연결 실패는 정상적으로 조회한 `false` 데이터다. API 연결 실패나 GraphQL 오류와 구분한다. 결과가 단일 non-null 상태이므로 별도 빈 목록 화면은 없다. 요청 오류에는 연결 URL이나 내부 오류 내용을 표시하지 않는다.

## Domain 및 필요한 데이터

- Backend 경계: `backend/internal/system`; 공개 Application 진입점은 `Service.Status(ctx)`다.
- Shared 경계: `app/shared/src/commonMain/kotlin/com/example/template/shared/feature/system`; `GetSystemStatusUseCase`가 repository를 통해 상태를 조회한다.
- Android 경계: `app/androidApp/src/main/kotlin/com/example/template/feature/system`; iOS 경계: `app/iosApp/Sources/Features/System`이다. `System`은 Swift 표기이며 동일한 `system` 기능이다.
- `SystemStatus.databaseReady`는 조회 시점의 pgx/sqlc `SELECT 1` 성공 여부다. 저장된 상태 이력이나 모든 서버 기능의 정상 여부를 뜻하지 않는다.
- 조회 인자와 사용자 입력은 없다. 상태 응답에 개인정보나 자격 증명을 포함하지 않는다.

## GraphQL Operation과 Mock 전략

계약 원본은 [system.graphqls](../../contracts/graphql/system.graphqls)다. `Query.systemStatus: SystemStatus!`, `SystemStatus.databaseReady: Boolean!`을 사용한다. 이번 명세 작성으로 SDL이나 DB schema/migration/sqlc query를 변경하지 않는다.

클라이언트 Operation은 [SystemStatus.graphql](../../app/shared/src/commonMain/graphql/com/example/template/shared/system/SystemStatus.graphql)의 `query SystemStatus`다. 클라이언트는 GraphQL errors가 있거나 필수 데이터가 없으면 요청 실패로 처리한다.

Mock 응답도 이 Operation을 따른다. `true`와 `false` 성공 응답, GraphQL 오류, 전송 실패, 실패 후 성공을 구분해 검증한다. 취소를 일반 요청 실패로 바꾸지 않는지도 확인한다. UI 상태 주입이나 Mock 성공만으로 실제 API·DB 연결을 검증했다고 기록하지 않는다.

## Android·iOS 차이와 완료 조건

Android는 `SystemStatusViewModel`의 `StateFlow`를 lifecycle에 맞춰 수집하고 Compose로 렌더링한다. iOS는 네이티브 `@Observable` 상태와 SwiftUI `.task`를 사용한다. UI·ViewModel·화면 상태는 공유하지 않는다. 이 기능에는 화면 간 Navigation이 없다.

두 플랫폼은 기존 `AppButton`, `AppColors`, `AppSpacing`을 사용한다. 이름·Token 대응은 [design-system-map.yaml](../../app/design/design-system-map.yaml)을 참고한다. 승인된 Figma 화면은 아직 없으므로 Figma 일치 여부는 미검증으로 남기고, 기준 화면이 승인되면 비교 결과를 기록한다.

아래 항목은 완료 판정 기준이다. 체크는 해당 변경과 환경에 대한 실행 증거를 확보한 뒤 한다.

- [ ] **기본 검증:** Feature 이름·계약 일치, codegen, 구조 검사, Backend·Shared 테스트, Android·iOS 빌드가 통과한다. 실제 PostgreSQL 통합 테스트와 skip 여부를 별도로 기록한다.
- [ ] **플랫폼 테스트:** Android 기기 테스트, KMP iOS 테스트, Swift 상태 테스트와 iOS UI 테스트를 별도로 실행한다. 성공 화면 또는 오류 화면 중 하나만 나타나는 검사는 DB 정상 연결의 증거로 사용하지 않는다.
- [ ] **실제 연결과 복구:** 위 표의 다섯 조건을 Android와 iOS 각각에서 확인한다. 특히 DB 실패 시 `Database not ready`, 복구 후 `Refresh` 시 `Database ready` 전환을 캡처한다. API 실패·복구도 같은 방식으로 확인한다.
- [ ] **화면과 접근성:** 로딩·중복 요청 차단·새로고침을 확인하고, 큰 글자·다크 모드·안전 영역·TalkBack/VoiceOver에서 상태와 버튼을 사용할 수 있는지 확인한다. Figma 비교의 수행 여부도 기록한다.
- [ ] **검증 증거:** 실행 날짜, 대상 변경, 기기·OS, 명령·결과, 화면 캡처 위치, 생략·미검증 항목을 [검증 기록](../verification.ko.md)에 남긴다. PR을 작성할 때 같은 범위를 요약한다.

### 실제 연결 검증 절차

[서버 실행](../../backend/docs/run.ko.md), [Android 실행](../../app/docs/android.ko.md), [iOS 실행](../../app/docs/ios.ko.md)에 따라 로컬 검증 환경을 준비한다. Android와 iOS가 동일한 검증 API를 바라보는지 먼저 확인한다.

1. API와 DB가 정상인 상태에서 양쪽 앱을 열어 `Database ready`와 정상 health 응답을 기록한다.
2. API를 유지한 채 검증용 DB만 중지한다. 양쪽 앱에서 `Refresh`를 누르고 `Database not ready`, `/livez` 204, `/readyz` 503, `databaseReady: false`를 기록한다.
3. 같은 DB를 다시 기동한다. API를 재시작하지 않고 양쪽 앱에서 `Refresh`를 눌러 `Database ready`, `/readyz` 204, `databaseReady: true`로 복구되는지 기록한다.
4. 검증 API를 중지하고 양쪽 앱에서 `Refresh`를 눌러 요청 오류 화면을 기록한다.
5. API를 다시 기동하고 DB 정상 연결을 확인한 뒤 양쪽 앱에서 `Refresh`를 눌러 정상 화면 복구를 기록한다. 검증 환경을 정상 상태로 마친다.

기본 검증 명령은 `./tools/verify.sh`이며 `VERIFY_STRICT=1`은 스크립트가 집계한 skip을 실패로 처리한다. 기본 검증의 `skip 0`은 플랫폼 테스트나 위 수동 시나리오의 실행을 뜻하지 않는다. 플랫폼별 테스트 명령은 [Android 테스트](../../app/docs/android.ko.md)와 [iOS 테스트](../../app/docs/ios.ko.md)을 따른다.

### 이번 명세 작성의 검증 범위

2026-09-18: 현재 계약·서버·Shared·양 플랫폼 화면 구현을 읽고 기대 결과를 명세했다. 기존 실행 결과는 [검증 기록](../verification.ko.md)에 있으며, 이번 문서 작성에서 장애·복구 시나리오나 플랫폼 테스트를 다시 실행한 것은 아니다. 위 체크리스트를 새 검증 완료로 표시하지 않는다.
