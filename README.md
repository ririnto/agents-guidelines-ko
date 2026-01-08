# AI 코딩 에이전트 가이드라인 (한국어)

**한국어** | [English](README.en.md)

AI 코딩 에이전트 (Claude, GitHub Copilot, Codex 등)를 위한
전역 지침, 스킬, 프롬프트, 에이전트 모음입니다.

## 설치

```bash
# 레포지토리 클론
git clone https://github.com/ririnto/agents-guidelines-ko.git
cd agents-guidelines-ko

# 설정 스크립트 실행
python setup-agents.py
```

### 설치 대상

| 대상         | 위치                                       |
| ------------ | ------------------------------------------ |
| Copilot 지침 | `~/.config/github-copilot/intellij/`       |
| VS Code 설정 | `settings.json` 업데이트                   |
| Claude 스킬  | `~/.claude/skills/`                        |
| Codex 스킬   | `~/.codex/skills/`                         |
| 프롬프트     | `~/.claude/commands/`, `~/.codex/prompts/` |
| 에이전트     | `~/.claude/agents/`, `~/.codex/agents/`    |

## 구성

### 전역 지침 (Instructions)

| 파일                                    | 설명                 |
| --------------------------------------- | -------------------- |
| [copilot-instructions.md]               | 워크플로우, MCP 규칙 |
| [global-git-commit-instructions.md]     | Conventional Commits |

[copilot-instructions.md]: .github/copilot-instructions.md
[global-git-commit-instructions.md]: .github/instructions/global-git-commit-instructions.md

### 에이전트 (Agents)

| 에이전트               | 용도        | MCP 도구         |
| ---------------------- | ----------- | ---------------- |
| [code-reviewer]        | 코드 리뷰   | git, serena      |
| [test-generator]       | 테스트 생성 | serena, context7 |
| [documentation-writer] | 문서 생성   | serena, context7 |
| [refactoring-expert]   | 리팩토링    | serena, git      |

[code-reviewer]: .github/agents/code-reviewer.agent.md
[test-generator]: .github/agents/test-generator.agent.md
[documentation-writer]: .github/agents/documentation-writer.agent.md
[refactoring-expert]: .github/agents/refactoring-expert.agent.md

### 스킬 (Skills)

| 스킬                  | 트리거 예시            |
| --------------------- | ---------------------- |
| [code-review]         | "코드 리뷰해줘"        |
| [explain-code]        | "이 코드 설명해줘"     |
| [generate-tests]      | "테스트 코드 작성해줘" |
| [implement-code]      | "기능 구현해줘"        |
| [refactor]            | "리팩토링해줘"         |
| [debug]               | "디버깅해줘"           |
| [conventional-commit] | "커밋 메시지 작성"     |

[code-review]: .github/skills/code-review/
[explain-code]: .github/skills/explain-code/
[generate-tests]: .github/skills/generate-tests/
[implement-code]: .github/skills/implement-code/
[refactor]: .github/skills/refactor/
[debug]: .github/skills/debug/
[conventional-commit]: .github/skills/conventional-commit/

### 프롬프트 (Prompts)

| 프롬프트                        | 용도           |
| ------------------------------- | -------------- |
| [fix-error]                     | 에러 분석/수정 |
| [explain]                       | 코드/개념 설명 |
| [optimize]                      | 성능 최적화    |
| [document]                      | 문서 생성      |
| [implement]                     | 기능 구현      |
| [create-pr]                     | PR 설명 생성   |
| [continue-without-confirmation] | 계속 진행      |

[fix-error]: .github/prompts/fix-error.prompt.md
[explain]: .github/prompts/explain.prompt.md
[optimize]: .github/prompts/optimize.prompt.md
[document]: .github/prompts/document.prompt.md
[implement]: .github/prompts/implement.prompt.md
[create-pr]: .github/prompts/create-pr.prompt.md
[continue-without-confirmation]: .github/prompts/continue-without-confirmation.prompt.md

## 사용법

### VS Code + GitHub Copilot

설치 후 Copilot Chat에서 자동으로 지침이 적용됩니다.

### Claude Code / Codex

```bash
# 스킬은 대화 중 자동 트리거
"이 코드 리뷰해줘"  # code-review 스킬 활성화

# 프롬프트는 명시적 호출
/fix-error
/create-pr

# 에이전트는 @ 호출
@code-reviewer src/ 디렉토리 변경사항 검토해줘
@test-generator UserService 테스트 생성해줘
```

## 커스터마이징

### 지침 수정

1. `.md` 파일 수정
2. `python setup-agents.py` 재실행 (파일이 복사되므로 변경사항 반영 필요)

### 새 스킬 추가

```text
.github/skills/
└── my-skill/
    └── SKILL.md
```

### 새 에이전트 추가

```text
.github/agents/
└── my-agent.agent.md
```

### 새 프롬프트 추가

```text
.github/prompts/
└── my-prompt.prompt.md
```

## MCP 통합

스킬과 에이전트는 다음 MCP 서버와 연동됩니다:

| MCP 서버            | 용도                 |
| ------------------- | -------------------- |
| context7            | 라이브러리/API 문서  |
| serena              | 심볼 탐색, 코드 분석 |
| jetbrains           | IDE 통합             |
| git                 | 버전 관리            |
| ripgrep             | 텍스트 검색          |
| sequential-thinking | 복잡한 문제 해결     |
| fetch               | 외부 웹 콘텐츠       |
| markitdown          | 문서 변환            |

## 원칙

### 한국어 출력

- 자연어 부분은 한국어로 출력
- 코드, 식별자, 기술 용어는 원어 유지

### 보호 용어

번역하지 않는 용어:

- 언어: JavaScript, TypeScript, Python, Go 등
- 프레임워크: React, Spring, Django 등
- 패턴: MVC, DDD, CQRS 등
- 에이전트: Claude, Copilot, MCP 등

## 참고 자료

### 공식 문서

#### GitHub Copilot
- [Custom Instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions) - VS Code Copilot 커스텀 지침 설정
- [Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills) - Copilot 에이전트 스킬 개발
- [github/awesome-copilot](https://github.com/github/awesome-copilot) - Copilot 리소스 모음

#### Claude
- [Skills 문서](https://code.claude.com/docs/ko/skills) - Claude 스킬 작성 가이드
- [Memory 기능](https://code.claude.com/docs/ko/memory) - Claude 메모리 활용
- [anthropics/skills](https://github.com/anthropics/skills) - Anthropic 공식 스킬

#### OpenAI Codex
- [Agents.md 가이드](https://developers.openai.com/codex/guides/agents-md) - Codex 에이전트 설정
- [Skills 개발](https://developers.openai.com/codex/skills/) - Codex 스킬 작성
- [openai/skills](https://github.com/openai/skills) - OpenAI 공식 스킬

### 커뮤니티 리소스

- [agents.md](https://agents.md/) - 에이전트 설정 표준 스펙
- [agentskills/agentskills](https://github.com/agentskills/agentskills) - 에이전트 스킬 컬렉션

## 라이선스

MIT
