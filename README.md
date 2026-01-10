# AI Coding Agent Guidelines (Korean)

**한국어** | [English](README.en.md)

AI 코딩 에이전트 (Claude, GitHub Copilot, Codex 등)를 위한
전역 지침, 스킬, 프롬프트, 에이전트 모음입니다.

## Install

```bash
# 레포지토리 클론
git clone https://github.com/ririnto/agents-guidelines-ko.git
cd agents-guidelines-ko

# 설정 스크립트 실행
python setup-agents.py
```

### Installation Targets

| Target | Assets | Default Path | Env Override |
| --- | --- | --- | --- |
| Claude | agents, skills, prompts, rules | `~/.claude/` | - |
| Codex | agents, skills, prompts | `~/.codex/` | `CODEX_HOME` |
| GitHub Copilot (IntelliJ) | instructions(`global-copilot-instructions.md`, `global-git-commit-instructions.md`), agents, prompts | `~/.config/github-copilot/intellij/` | - |
| VS Code Copilot Chat | agents+prompts → `prompts/`, instructions paths added to `settings.json` | `~/Library/Application Support/Code/User/` | `VSCODE_USER_DATA` |

## Structure

### Instructions

| 파일 | 설명 |
| --- | --- |
| [copilot-instructions.md](.github/copilot-instructions.md) | 워크플로우, MCP 규칙 |
| [global-git-commit-instructions.md](.github/instructions/global-git-commit-instructions.md) | Conventional Commits |

### Claude-only Rules (.claude/rules)

| 파일 | 설명 |
| --- | --- |
| [agent-routing.md](.claude/rules/agent-routing.md) | 서브에이전트 라우팅 규칙 |
| [language-and-writing.md](.claude/rules/language-and-writing.md) | 기본 출력 언어 및 용어 보존 규칙 |

### Agents

`.claude/agents/`는 Claude용, `.github/agents/`는 GitHub Copilot/Codex용 에이전트가 있습니다. 대표 에이전트:

| 에이전트 | 용도 | MCP/도구 예시 |
| --- | --- | --- |
| [code-reviewer](.claude/agents/code-reviewer.md) | 코드 리뷰 | git, serena |
| [implementer](.claude/agents/implementer.md) | 다중 파일 구현 | serena, jetbrains, git |
| [single-file-implementer](.claude/agents/single-file-implementer.md) | 단일 파일 수정 | jetbrains, serena |
| [test-runner](.claude/agents/test-runner.md) | 테스트 실행/수정 | jetbrains, bash |

### Skills

| 스킬 | 트리거 예시 |
| --- | --- |
| [code-review](.github/skills/code-review/SKILL.md) | "코드 리뷰해줘" |
| [explain-code](.github/skills/explain-code/SKILL.md) | "이 코드 설명해줘" |
| [generate-tests](.github/skills/generate-tests/SKILL.md) | "테스트 코드 작성해줘" |
| [implement-code](.github/skills/implement-code/SKILL.md) | "기능 구현해줘" |
| [refactor](.github/skills/refactor/SKILL.md) | "리팩토링해줘" |
| [debug](.github/skills/debug/SKILL.md) | "디버깅해줘" |
| [conventional-commit](.github/skills/conventional-commit/SKILL.md) | "커밋 메시지 작성" |

### Prompts

| 프롬프트 | 용도 |
| --- | --- |
| [fix-error](.github/prompts/fix-error.prompt.md) | 에러 분석/수정 |
| [explain](.github/prompts/explain.prompt.md) | 코드/개념 설명 |
| [optimize](.github/prompts/optimize.prompt.md) | 성능 최적화 |
| [document](.github/prompts/document.prompt.md) | 문서 생성 |
| [implement](.github/prompts/implement.prompt.md) | 기능 구현 |
| [create-pr](.github/prompts/create-pr.prompt.md) | PR 설명 생성 |
| [continue-without-confirmation](.github/prompts/continue-without-confirmation.prompt.md) | 계속 진행 |

## Usage

### VS Code + GitHub Copilot

After install, instructions apply automatically in Copilot Chat.

### Claude Code / Codex

```text
# Skills auto-trigger in conversation
"이 코드 리뷰해줘"  # code-review skill

# Prompts explicitly
/fix-error
/create-pr

# Agents via @
@code-reviewer src/ 디렉토리 변경사항 검토해줘
@test-generator UserService 테스트 생성해줘
```

## Customization

### Modify Instructions

1. `.md` 파일 수정
2. `python setup-agents.py` 재실행 (복사 대상: `.github/**/*`, `.claude/**/*`, `.github/prompts/**/*`)
3. Claude 전용 규칙은 `.claude/rules/`, Copilot/Codex 전용 에이전트는 `.github/agents/`를 수정

### Add New Skill

```text
.github/skills/
└── my-skill/
    └── SKILL.md
```

### Add New Agent

```text
.github/agents/       # Copilot/Codex용
.claude/agents/       # Claude용
└── my-agent.md
```

### Add New Prompt

```text
.github/prompts/
└── my-prompt.prompt.md
```

### Python Script Test

설정 스크립트는 추가 의존성이 없습니다. 변경 후 간단 검증:

```bash
python -m compileall setup-agents.py
```

## MCP Integration

| MCP 서버 | 용도 |
| --- | --- |
| context7 | 라이브러리/API 문서 |
| serena | 심볼 탐색, 코드 분석 |
| jetbrains | IDE 통합 |
| git | 버전 관리 |
| sequential-thinking | 복잡한 문제 해결 |
| fetch | 외부 웹 콘텐츠 |
| markitdown | 문서 변환 |

## Principles

- 자연어는 한국어로 출력하며, 아래 항목은 원문 유지:
    - code block, backtick content
    - CamelCase / snake_case identifier
    - path(`.`, `/`, `[]` 포함)
    - ALL_CAPS acronym
    - proper noun, reserved word

## References

### Official Docs

#### GitHub Copilot

- [Custom Instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions) - VS Code Copilot
  커스텀 지침 설정
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

### Community Resources

- [agents.md](https://agents.md/) - 에이전트 설정 표준 스펙
- [agentskills/agentskills](https://github.com/agentskills/agentskills) - 에이전트 스킬 컬렉션

## License

MIT
