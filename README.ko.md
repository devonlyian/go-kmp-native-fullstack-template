# KMP Native Fullstack Template

[English](README.md) | [한국어](README.ko.md)

네이티브 Android·iOS 앱, Kotlin 공통 로직, Go GraphQL 백엔드를 사용하는 프로젝트의 최소 시작점이다.

## 템플릿 구성

- Android Compose·iOS SwiftUI 화면과 Domain/Data/Network를 공유하는 KMP.
- PostgreSQL과 단일 루트 SDL 계약을 사용하는 GraphQL 우선 Go 모듈러 모놀리스.
- DB·API·공통 로직·양쪽 앱을 연결하는 최소 `systemStatus` 기능.
- 코드 생성, 빌드·테스트 스크립트, 영어·한국어 개발 문서.
- `.agents/skills/` 아래 vendored [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) 스킬(MIT). 디자인 영역이 스타일·팔레트·폰트 조합·UX 규칙을 검색하는 디자인 지능 참고 자료로 사용한다. 검색 스크립트에는 Python 3가 필요하다.

vendored 스킬을 갱신하려면 CLI를 설치하고 저장소 루트에서 업데이터를 실행한다.

```sh
npm install -g ui-ux-pro-max-cli
uipro update            # 이 저장소의 .agents/skills/를 갱신한다
# 또는 재설치: uipro init --ai codex --force
```

결과 diff를 검토한 뒤 커밋한다.

인증, 제품 도메인, 배포 workflow, 라이선스는 템플릿에서 선택하지 않는다. 로컬 검증은 운영 준비나 실기기 검증을 의미하지 않는다.

이 README는 템플릿을 설명한다. 파생 저장소에서는 영어·한국어 README를 실제 프로젝트의 목적·기능·사용자 안내로 교체한다. 개발 지침은 README와 독립적으로 `AGENTS.md`, `.agents/skills/`, `docs/`에 유지한다.
