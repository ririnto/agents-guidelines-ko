# AI Coding Agent Guidelines (Korean)

**한국어** | [English](README.en.md)

AI 코딩 에이전트 (Claude, GitHub Copilot, Codex 등)를 위한
전역 지침과 스킬 모음입니다.

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
| Claude | skills, `copilot-instructions.md` → `CLAUDE.md` | `~/.claude/` | - |
| Codex | skills, `copilot-instructions.md` → `AGENTS.md` | `~/.codex/` | `CODEX_HOME` |
| GitHub Copilot (IntelliJ) | instructions(`global-copilot-instructions.md`, `global-git-commit-instructions.md`), skills | `~/.config/github-copilot/intellij/` | - |
| VS Code Copilot Chat | instructions paths added to `settings.json` | `~/Library/Application Support/Code/User/` | `VSCODE_USER_DATA` |

## Structure

### Instructions

| 파일 | 설명 |
| --- | --- |
| [copilot-instructions.md](.github/copilot-instructions.md) | 워크플로우, MCP 규칙 |
| [global-git-commit-instructions.md](.github/instructions/global-git-commit-instructions.md) | Conventional Commits |

### Skills

| 스킬 | 트리거 예시 |
| --- | --- |
| [conventional-commit](.github/skills/conventional-commit/SKILL.md) | "커밋 메시지 작성" |

## Usage

### VS Code + GitHub Copilot

After install, instructions apply automatically in Copilot Chat.

### Claude Code / Codex

```text
# Skills auto-trigger in conversation
"커밋 메시지 작성해줘"  # conventional-commit skill
```

## Customization

### Modify Instructions

1. `.md` 파일 수정
2. `python setup-agents.py` 재실행
3. 필요시 `.github/copilot-instructions.md` 수정

### Add New Skill

```text
.github/skills/
└── my-skill/
    └── SKILL.md
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
| fetch | 외부 웹 콘텐츠 |
| exa | AI 기반 웹 검색 |
| grep-app | GitHub 코드 검색 |

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
- [github/awesome-copilot](https://github.com/github.com/github/awesome-copilot) - Copilot 리소스 모음

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
