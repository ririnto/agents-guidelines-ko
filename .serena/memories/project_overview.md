# Project Overview: agents-guidelines-ko

## Purpose

AI 코딩 에이전트 (Claude, GitHub Copilot, Codex 등)를 위한 전역 지침, 스킬, 프롬프트, 에이전트 모음 저장소입니다. 한국어 사용자를 위한 AI 코딩 에이전트 설정을 제공합니다.

## Tech Stack

- **Language**: Python 3, Markdown, Bash
- **Dependencies**: pytest (테스트용)
- **Platform**: macOS (Darwin) 지원, 크로스 플랫폼 가능
- **Integration**: MCP servers (context7, serena, git, ripgrep, fetch, markitdown)

## Project Structure

```
.
├── .claude/               # Claude Code 설정
│   ├── agents/           # Claude 전용 에이전트 정의
│   ├── rules/            # 라우팅, 언어 규칙
│   ├── hooks/            # Post-tool-call 훅
│   └── settings.local.json
├── .github/
│   ├── agents/           # GitHub Copilot 에이전트
│   ├── skills/           # 공용 스킬 정의
│   ├── prompts/          # 재사용 프롬프트
│   └── instructions/     # 전역 지침
├── setup-agents.py       # 설치 스크립트
├── test_setup_agents.py  # 테스트
├── requirements.txt      # Python 의존성
└── README.md            # 문서 (한국어)
```

## Key Components

### Instructions (지침)
- `copilot-instructions.md`: 워크플로우, MCP 규칙
- `global-git-commit-instructions.md`: Conventional Commits 가이드

### Agents (에이전트)
- `code-reviewer`, `test-generator`, `documentation-writer`, `refactoring-expert`
- Claude 전용: `architect`, `scout`, `implementer`, `security-auditor` 등 40+ 전문 에이전트

### Skills (스킬)
- `code-review`, `explain-code`, `generate-tests`, `implement-code`, `refactor`, `debug`, `conventional-commit`

### Prompts (프롬프트)
- `fix-error`, `explain`, `optimize`, `document`, `implement`, `create-pr`, `continue-without-confirmation`

## Target Environments

설치 스크립트가 지원하는 대상:
1. **VS Code** (GitHub Copilot) - `~/Library/Application Support/Code/User/`
2. **Claude Code** - `~/.claude/`
3. **OpenAI Codex** - `~/.codex/`
4. **IntelliJ** (GitHub Copilot) - `~/.config/github-copilot/intellij/`
