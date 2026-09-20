# 새 프로젝트 시작

[English](new-project.md) | [한국어](new-project.ko.md)

이 폴더는 템플릿 원본이고 GitHub 기본·릴리스 브랜치는 `main`이다. 소유자가 GitHub에 업로드한 뒤 Settings → General → **Template repository**를 켜고 **Use this template**으로 저장소를 만든다. 기능 작업 전 `main`에서 `dev`를 만든다. 공개 재사용 전 라이선스는 소유자가 선택한다.

`README.md`와 `README.ko.md`를 실제 프로젝트 설명으로 교체한다. README는 사용자용 소개이며 에이전트 지침 진입점이 아니다. 개발 작업의 읽을 경로는 [개발 문서 목차](../index.ko.md), AGENTS, 스킬에 유지한다.

기본값을 교체한다.

| 검색 | 변경 |
| --- | --- |
| `TemplateApp` | 표시 이름, Xcode target·scheme·project 이름 |
| `com.example.template` | Android namespace/applicationId, Kotlin package, iOS bundle identifier |
| `example.com/template/backend` | Go module과 import |
| `template-app`, `kmp-native-fullstack-template` | Gradle 프로젝트 이름, 문서의 저장소 이름 |
| `api.example.com` | 운영 HTTPS API 주소 |

```sh
rg -n 'TemplateApp|com\.example\.template|example\.com/template/backend|template-app|kmp-native-fullstack-template|api\.example\.com' .
```

Kotlin package를 바꾸면 해당 디렉터리도 옮긴다. Xcode scheme/project 이름과 `tools/verify.sh`의 대응 경로를 갱신한다. 생성 코드를 직접 수정하지 말고 [검사](checks.ko.md)를 따른다.

제품 작업은 [백엔드 개발](../../.agents/skills/develop-backend/SKILL.ko.md) 또는 [앱 개발](../../.agents/skills/develop-app/SKILL.ko.md)을 선택하고 기본으로 양쪽을 읽지 않는다. 이 저장소는 Figma 파일이나 Code Connect 연결을 만들지 않는다. 실제 화면을 렌더링해 글자 확대·다크 모드·접근성·승인된 디자인과의 차이를 검토한다. 매핑만으로 픽셀 일치를 증명할 수 없다.

다음: 새 프로젝트의 경계를 이해하려면 [아키텍처](../architecture.ko.md)를 읽는다.
