---
name: verify-change
description: 요청된 백엔드·앱·문서 범위 안에서 검사를 선택한다. 상대 구현으로 범위를 넓히지 않고 계약 인계와 통합 미검증을 보고한다.
---

# 영역 내 검증

[English](SKILL.md) | [한국어](SKILL.ko.md)

번역 작업이나 명시적 요청 외에는 영어를 쓴다. 안내를 읽거나 도구를 실행하기 전에 요청 영역을 선택한다. 공통 SDL 변경이 상대 영역 빌드·코드 조사를 허가하지 않는다.

| 영역 | 검사와 자료 |
| --- | --- |
| Markdown만 변경 | [sync-docs](../sync-docs/SKILL.ko.md) 후 `./tools/verify.sh structure` |
| 백엔드 | [백엔드 검사](../../../backend/docs/checks.ko.md), `./tools/verify.sh backend`, 서버 GraphQL·DB만 재생성·검사 |
| 앱 Shared / Android | [앱 검사](../../../app/docs/checks.ko.md), `./tools/verify.sh app`, Shared 변경은 관련 KMP iOS 테스트·앱 빌드도 필요 |
| 앱 Swift / Apple 연동 | `./tools/verify.sh ios`, [iOS](../../../app/docs/ios.ko.md) 테스트, 백엔드 코드 조사 없음 |
| 명시적 전체 스택 통합 | 전체 `./tools/verify.sh`와 해당 통합에서 요청한 플랫폼·실행 검사, [공통 검사 선택](../../../docs/guides/checks.ko.md) |

일치 검사 전에 현재 영역만 재생성한다. 백엔드 통합에는 비밀정보를 노출하지 않고 `TEST_DATABASE_URL`을 제공한다. 준비 조건이 갖춰지면 `VERIFY_STRICT=1`, 아니면 생략 검사를 명시한다. 도구 버전 변경도 요청 영역에 한정한다.

앱 UI 변경은 관련 플랫폼 테스트와 실제 화면·접근성 검토가 필요하며 계약에 맞는 Mock이나 제공된 API를 사용한다. 기본 스크립트는 Android 연결 테스트·KMP iOS 테스트·네이티브 iOS 앱/UI 테스트·화면 검토를 실행하지 않는다. Mock은 실제 서버 호환성을 증명하지 않는다.

명령·날짜/환경·결과·한계를 해당 영역 기록에 남긴다. 계약 변경 뒤 상대 영역·소비 코드 검사는 인계하며 전체 호환성을 주장하거나 상대 영역을 몰래 수정하지 않는다. 과거 통합 기록은 명시적인 통합·이력 작업 때만 읽고 매번 로컬 수정 때 읽지 않는다.
