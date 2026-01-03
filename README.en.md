# AI Coding Agent Guidelines (Korean)

[한국어](README.md) | **English**

A collection of global instructions, skills, prompts, and agents
for AI coding agents (Claude, GitHub Copilot, Codex, etc.).

## Installation

```bash
# Clone repository
git clone https://github.com/ririnto/agents-guidelines-ko.git
cd agents-guidelines-ko

# Run setup script
python setup-agents.py
```

### Installation Targets

| Target               | Location                                   |
| -------------------- | ------------------------------------------ |
| Copilot Instructions | `~/.config/github-copilot/intellij/`       |
| VS Code Settings     | `settings.json` update                     |
| Claude Skills        | `~/.claude/skills/`                        |
| Codex Skills         | `~/.codex/skills/`                         |
| Prompts              | `~/.claude/commands/`, `~/.codex/prompts/` |
| Agents               | `~/.claude/agents/`, `~/.codex/agents/`    |

## Structure

### Global Instructions

| File                                    | Description          |
| --------------------------------------- | -------------------- |
| [copilot-instructions.md]               | Workflow, MCP rules  |
| [global-git-commit-instructions.md]     | Conventional Commits |

[copilot-instructions.md]: .github/copilot-instructions.md
[global-git-commit-instructions.md]: .github/instructions/global-git-commit-instructions.md

### Agents

| Agent                  | Purpose     | MCP Tools        |
| ---------------------- | ----------- | ---------------- |
| [code-reviewer]        | Code review | git, serena      |
| [test-generator]       | Test gen    | serena, context7 |
| [security-analyzer]    | Security    | serena, ripgrep  |
| [documentation-writer] | Docs        | serena, context7 |
| [refactoring-expert]   | Refactoring | serena, git      |

[code-reviewer]: .github/agents/code-reviewer.agent.md
[test-generator]: .github/agents/test-generator.agent.md
[security-analyzer]: .github/agents/security-analyzer.agent.md
[documentation-writer]: .github/agents/documentation-writer.agent.md
[refactoring-expert]: .github/agents/refactoring-expert.agent.md

### Skills

| Skill                 | Trigger Examples       |
| --------------------- | ---------------------- |
| [code-review]         | "review code"          |
| [explain-code]        | "explain this code"    |
| [generate-tests]      | "write tests"          |
| [implement-code]      | "implement feature"    |
| [refactor]            | "refactor this"        |
| [debug]               | "debug this"           |
| [conventional-commit] | "write commit message" |

[code-review]: .github/skills/code-review/
[explain-code]: .github/skills/explain-code/
[generate-tests]: .github/skills/generate-tests/
[implement-code]: .github/skills/implement-code/
[refactor]: .github/skills/refactor/
[debug]: .github/skills/debug/
[conventional-commit]: .github/skills/conventional-commit/

### Prompts

| Prompt                          | Purpose        |
| ------------------------------- | -------------- |
| [fix-error]                     | Error fix      |
| [explain]                       | Explanation    |
| [optimize]                      | Optimization   |
| [document]                      | Documentation  |
| [implement]                     | Implementation |
| [create-pr]                     | PR desc        |
| [continue-without-confirmation] | Continue work  |

[fix-error]: .github/prompts/fix-error.prompt.md
[explain]: .github/prompts/explain.prompt.md
[optimize]: .github/prompts/optimize.prompt.md
[document]: .github/prompts/document.prompt.md
[implement]: .github/prompts/implement.prompt.md
[create-pr]: .github/prompts/create-pr.prompt.md
[continue-without-confirmation]: .github/prompts/continue-without-confirmation.prompt.md

## Usage

### VS Code + GitHub Copilot

After installation, instructions apply automatically in Copilot Chat.

### Claude Code / Codex

```bash
# Skills are auto-triggered during conversation
"review this code"  # activates code-review skill

# Prompts are explicitly invoked
/fix-error
/create-pr

# Agents are called with @
@code-reviewer review changes in src/
@test-generator create tests for UserService
```

## Customization

### Modify Instructions

1. Edit `.md` files
2. Re-run `python setup-agents.py`
   (symlinks auto-reflect changes)

### Add New Skill

```text
.github/skills/
└── my-skill/
    └── SKILL.md
```

### Add New Agent

```text
.github/agents/
└── my-agent.agent.md
```

### Add New Prompt

```text
.github/prompts/
└── my-prompt.prompt.md
```

## MCP Integration

Skills and agents integrate with these MCP servers:

| MCP Server          | Purpose              |
| ------------------- | -------------------- |
| context7            | Library/API docs     |
| serena              | Symbol nav, analysis |
| jetbrains           | IDE integration      |
| git                 | Version control      |
| ripgrep             | Fast text search     |
| sequential-thinking | Complex problem      |
| fetch               | External web content |
| markitdown          | Document conversion  |

## Principles

### Korean Output

- Natural language parts in Korean
- Code, identifiers, technical terms remain in English

### Protected Terms

Terms that should not be translated:

- Languages: JavaScript, TypeScript, Python, Go, etc.
- Frameworks: React, Spring, Django, etc.
- Patterns: MVC, DDD, CQRS, etc.
- Agent terms: Claude, Copilot, MCP, etc.

## License

MIT
