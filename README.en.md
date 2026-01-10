# AI Coding Agent Guidelines (English)

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

| Target | Assets | Default Path | Env Override |
| --- | --- | --- | --- |
| Claude | agents, skills, prompts, rules | `~/.claude/` | - |
| Codex | agents, skills, prompts | `~/.codex/` | `CODEX_HOME` |
| GitHub Copilot (IntelliJ) | instructions(`global-copilot-instructions.md`, `global-git-commit-instructions.md`), agents, prompts | `~/.config/github-copilot/intellij/` | - |
| VS Code Copilot Chat | agents+prompts → `prompts/`, instruction paths added to `settings.json` | `~/Library/Application Support/Code/User/` | `VSCODE_USER_DATA` |

## Structure

### Global Instructions

| File | Description |
| --- | --- |
| [copilot-instructions.md](.github/copilot-instructions.md) | Workflow, MCP rules |
| [global-git-commit-instructions.md](.github/instructions/global-git-commit-instructions.md) | Conventional Commits |

### Claude-only Rules (.claude/rules)

| File | Description |
| --- | --- |
| [agent-routing.md](.claude/rules/agent-routing.md) | Subagent routing rules |
| [language-and-writing.md](.claude/rules/language-and-writing.md) | Default language and term preservation |

### Agents

`.claude/agents/` is for Claude; `.github/agents/` is for GitHub Copilot/Codex. Representative agents:

| Agent | Purpose | MCP/Tools (examples) |
| --- | --- | --- |
| [code-reviewer](.claude/agents/code-reviewer.md) | Code review | git, serena |
| [implementer](.claude/agents/implementer.md) | Multi-file implementation | serena, jetbrains, git |
| [single-file-implementer](.claude/agents/single-file-implementer.md) | Single-file edits | jetbrains, serena |
| [test-runner](.claude/agents/test-runner.md) | Test run/fix | jetbrains, bash |

### Skills

| Skill | Trigger Examples |
| --- | --- |
| [code-review](.github/skills/code-review/SKILL.md) | "review code" |
| [explain-code](.github/skills/explain-code/SKILL.md) | "explain this code" |
| [generate-tests](.github/skills/generate-tests/SKILL.md) | "write tests" |
| [implement-code](.github/skills/implement-code/SKILL.md) | "implement feature" |
| [refactor](.github/skills/refactor/SKILL.md) | "refactor this" |
| [debug](.github/skills/debug/SKILL.md) | "debug this" |
| [conventional-commit](.github/skills/conventional-commit/SKILL.md) | "write commit message" |

### Prompts

| Prompt | Purpose |
| --- | --- |
| [fix-error](.github/prompts/fix-error.prompt.md) | Error fix |
| [explain](.github/prompts/explain.prompt.md) | Explanation |
| [optimize](.github/prompts/optimize.prompt.md) | Optimization |
| [document](.github/prompts/document.prompt.md) | Documentation |
| [implement](.github/prompts/implement.prompt.md) | Implementation |
| [create-pr](.github/prompts/create-pr.prompt.md) | PR desc |
| [continue-without-confirmation](.github/prompts/continue-without-confirmation.prompt.md) | Continue work |

## Usage

### VS Code + GitHub Copilot

After installation, instructions apply automatically in Copilot Chat.

### Claude Code / Codex

```text
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

1. Edit `.md` files.
2. Re-run `python setup-agents.py` (copies `.github/**/*`, `.claude/**/*`, `.github/prompts/**/*`).
3. Claude-only rules live in `.claude/rules/`; Copilot/Codex agents live in `.github/agents/`.

### Add New Skill

```text
.github/skills/
└── my-skill/
    └── SKILL.md
```

### Add New Agent

```text
.github/agents/     # for Copilot/Codex
.claude/agents/     # for Claude
└── my-agent.md
```

### Add New Prompt

```text
.github/prompts/
└── my-prompt.prompt.md
```

### Python Script Test

Setup script has no extra dependencies. After changes, quick check:

```bash
python -m compileall setup-agents.py
```

## MCP Integration

Uses only the MCP servers defined in `copilot-instructions.md`.

| MCP Server | Purpose |
| --- | --- |
| context7 | Library/API docs |
| serena | Symbol nav, analysis |
| jetbrains | IDE integration |
| git | Version control |
| sequential-thinking | Complex problem |
| fetch | External web content |
| markitdown | Document conversion |

## Principles

- Natural language parts in Korean; preserve:
    - code blocks, backtick content
    - CamelCase / snake_case identifiers
    - paths (including `.`, `/`, `[]`)
    - ALL_CAPS acronyms
    - proper nouns, reserved words

## References

### Official Documentation

#### GitHub Copilot

- [Custom Instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions) - Configure custom
  instructions for VS Code Copilot
- [Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills) - Develop Copilot agent skills
- [github/awesome-copilot](https://github.com/github/awesome-copilot) - Awesome Copilot resources

#### Claude

- [Skills Documentation](https://code.claude.com/docs/ko/skills) - Guide to writing Claude skills
- [Memory Feature](https://code.claude.com/docs/ko/memory) - Using Claude memory
- [anthropics/skills](https://github.com/anthropics/skills) - Official Anthropic skills

#### OpenAI Codex

- [Agents.md Guide](https://developers.openai.com/codex/guides/agents-md) - Codex agent configuration
- [Skills Development](https://developers.openai.com/codex/skills/) - Creating Codex skills
- [openai/skills](https://github.com/openai/skills) - Official OpenAI skills

### Community Resources

- [agents.md](https://agents.md/) - Agent configuration standard specification
- [agentskills/agentskills](https://github.com/agentskills/agentskills) - Collection of agent skills

## License

MIT
