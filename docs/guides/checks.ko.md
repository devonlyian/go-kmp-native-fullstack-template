# 생성, 포맷, 검증

[English](checks.md) | [한국어](checks.ko.md)

변경한 범위를 선택해 그 범위의 검사만 실행한다.

- [백엔드 검사](../../backend/docs/checks.ko.md)는 gqlgen/sqlc를 생성하고 백엔드만 검증한다.
- [앱 검사](../../app/docs/checks.ko.md)는 Apollo 소스를 생성하고 shared KMP, Android 또는 iOS 작업만 검증한다.

명시적으로 요청된 통합 변경에 전체 저장소 검사가 필요할 때만 범위 없이 `./tools/verify.sh`를 실행한다. 플랫폼 UI 테스트와 live 백엔드 작업은 별도 선택 작업이다.
