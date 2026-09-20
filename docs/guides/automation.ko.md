# 프로젝트 에이전트와 종료 훅

[English](automation.md) | [한국어](automation.ko.md)

자동화 설정·관리 때만 읽는다. 실행 지침은 영어이며 한국어 문서는 사용자에게 같은 설정을 설명한다. README는 제품·템플릿 소개로 유지한다.

## 역할과 인계

Codex는 `.codex/agents/`에서 프로젝트 역할을 찾는다. 부모의 모델·권한을 상속하며 템플릿이 모델을 고정하거나 권한을 늘리거나 플러그인을 설치하지 않는다.

| 역할 | 담당 | 진입점 |
| --- | --- | --- |
| `planning` | 제품 가치·범위·흐름·규칙·완료 조건·승인 상태 | [plan-feature](../../.agents/skills/plan-feature/SKILL.ko.md) |
| `backend` | Go·DB·서버 검증과 앱이 작성한 GraphQL 계약 draft의 검토·확정 | [develop-backend](../../.agents/skills/develop-backend/SKILL.ko.md) |
| `app` | KMP·Compose·SwiftUI 구현, SDL draft, 앱 검증 | [develop-app](../../.agents/skills/develop-app/SKILL.ko.md) |
| `design` | 디자인 명세·매핑, 허용된 Figma 작업, 시각 검토 | [design-app](../../.agents/skills/design-app/SKILL.ko.md) |

요청된 역할만 사용한다. 한정된 작업·허용 경로·관련 기획/계약/디자인 참조·완료 조건만 전달하고 지원되는 경우 새 문맥을 사용한다. 매 작업마다 모든 역할을 실행하거나 작업자에게 재위임을 요구하지 않는다. 메인 에이전트가 범위를 정하고 간결한 결과를 통합한다. 동시에 수정하는 작업자에게 기획 문서·디자인 매핑·번역 검토 기록을 포함해 겹치지 않는 소유권을 준다.

기획은 `docs/plans/`에 구현 방식과 독립된 초안을 두며 Figma·GraphQL·데이터베이스·백엔드·앱 구현을 조사하거나 수정하지 않는다. 백엔드와 앱은 상대 구현 대신 루트 GraphQL SDL로 소통한다: 앱 영역이 승인된 디자인의 데이터 요구사항으로 SDL draft를 작성하고 backend 영역이 서버 구현 전에 검토·확정한다. 디자인은 재사용·검토를 위해 대상 네이티브 컴포넌트·화면을 읽을 수 있지만 프로덕션 코드를 수정하지 않는다. 새 디자인 결정은 앱 구현 전에 검토받고 승인된 기준은 반복 승인하지 않는다. 부족한 기획·계약이나 사용할 수 없는 도구는 동작을 지어내지 않고 보고한다. 역할 지침은 안내이며 파일 시스템 접근 통제가 아니다.

요청 예시: “planning으로 이 기능 기획을 작성하고 검토해줘”, “backend로 합의된 Query를 구현해줘”, “design으로 승인된 네이티브 흐름 초안을 만들어줘”, “app으로 이 계약과 승인된 디자인을 구현해줘”. 전체 영역 통합은 별도로 요청한다.

## 종료 훅

[`.codex/hooks.json`](../../.codex/hooks.json)이 메인 에이전트의 턴이 끝날 때 [`tools/codex-stop.py`](../../tools/codex-stop.py)를 호출한다. 하위 폴더에서 Codex를 시작해도 저장소 루트를 찾는다. Python 3와 Git이 필요하다.

- staged·unstaged·untracked Markdown 변경과 `docs/.translations.json`, `tools/check-docs.py` 변경을 확인한다. 첫 커밋이 없는 저장소도 지원한다. 작업별 편집 이력이 아닌 작업 트리 변경이므로 기존 변경도 검사 계기가 될 수 있다.
- 기존 읽기 전용 문서 검사기만 실행한다. 번역 쌍 누락·갱신 여부와 검토 해시를 확인하며 번역 의미·링크 정확성·코드 동작·시각 품질은 판단하지 않는다. 검토 기록·파일 수정·커밋·양쪽 구현 빌드를 자동 실행하지 않는다.
- 성공하면 조용히 끝난다. 실패하면 길이를 제한한 진단과 함께 한 번의 후속 작업을 요청한다. `stop_hook_active`에서는 검사·후속 작업을 다시 요청하지 않아 반복을 막는다. 수정 후 수동으로 재검사하고 남은 실패를 보고한다. Git·명령 오류나 시간 초과도 한 번의 후속 작업을 요청해 수동 검사하거나 검사 불가를 보고하게 하며 성공으로 간주하지 않는다. 이 가벼운 훅은 캐시를 두지 않으므로 이후 독립된 턴에서 같은 미커밋 파일을 다시 검사할 수 있다.

Codex가 프로젝트와 정확한 훅 정의를 불러오고 신뢰한 뒤에만 자동 실행된다. CLI에서는 이 저장소에서 Codex를 시작하고 `/hooks`로 확인·신뢰한다. 정의가 바뀌면 다시 검토해야 한다. 신뢰는 훅 정의를 대상으로 하므로 템플릿 업데이트나 브랜치 전환 시 참조하는 저장소 스크립트도 검토한다. 신뢰 검토를 우회하지 않는다. 파일 생성이나 스크립트 테스트 통과가 현재 데스크톱 세션의 로딩을 증명하지는 않는다. 프로젝트를 다시 불러온 뒤 클라이언트에서 역할 제공 여부와 훅 신뢰 상태를 확인한다.

저장소 루트에서 수동 검증한다.

```sh
python3 tools/check-docs.py
python3 -m unittest discover -s tools -p 'test_*.py'
./tools/verify.sh structure
```

기존 CI의 구조 검사 단계는 로컬 훅 신뢰와 독립적으로 검사기·도구 테스트를 실행한다. 이것만으로 모든 플랫폼·실행 검사가 통과했다는 뜻은 아니다.

출처: OpenAI 공식 [사용자 정의 에이전트](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents), [훅](https://learn.chatgpt.com/docs/hooks) 문서. 문서화된 형식과 로컬 CLI 0.154.0을 기준으로 구성을 확인했으며 실제 탐색·신뢰는 로컬 클라이언트가 결정한다.
