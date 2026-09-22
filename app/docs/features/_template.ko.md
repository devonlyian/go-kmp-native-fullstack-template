# 앱 기능: <feature>

[English](_template.md) | [한국어](_template.ko.md)

## 흐름과 계약

- 현재 단계: 임시 fixture를 쓰는 네이티브 앱 / 계약 인계 / GraphQL 연결:
- 사용자 가치·대상 플랫폼·범위/제외:
- 진입/행동/결과/재시도, 로딩/빈 데이터/오류/오프라인/취소:
- 확인된 데이터 요구와 임시 가정, 합의 뒤 루트 SDL/Operation·결과/nullability/오류(그전에는 보류 또는 불필요):

## 앱 구현

- Shared Domain/Data/Network와 네이티브 Presentation 경로:
- 승인된 원본(승인된 Figma 파일 / 합의된 로컬 명세)과 Design System 참조, 토큰 대응·기존/계획된 네이티브 심볼·실제 매핑 예외:
- 임시 로컬 fixture·테스트 대역, 계약에 맞춘 Mock, 제공된 API endpoint 중 해당 증거 종류:

## 앱 완료 조건

- [ ] 공통 테스트·관련 플랫폼 빌드/테스트, 합의된 GraphQL 작업의 Apollo 생성·모델/fixture 정합성
- [ ] 실제 화면·재시도·글자 확대·다크 모드·VoiceOver/TalkBack
- [ ] 임시 데이터·계약에 맞춘 Mock·실제 API의 구분된 증거·날짜/환경·생략·계약/백엔드/연결 인계 기록

Go·SQL 조사나 서버 구현은 필요하지 않다. 계약 생성 전에 네이티브 흐름 검증을 마칠 수 있으며 API 연결·실제 통합은 별도로 확인할 때까지 보류한다. Mock 성공은 실제 통합의 증거가 아니다.
