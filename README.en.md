# AI Coding Agent Guidelines (English)

[한국어](README.md) | **English**

A collection of global instructions and skills
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
| Claude | skills, `copilot-instructions.md` → `CLAUDE.md` | `~/.claude/` | - |
| Codex | skills, `copilot-instructions.md` → `AGENTS.md` | `~/.codex/` | `CODEX_HOME` |
| GitHub Copilot (IntelliJ) | instructions(`global-copilot-instructions.md`, `global-git-commit-instructions.md`), skills | `~/.config/github-copilot/intellij/` | - |
| VS Code Copilot Chat | instruction paths added to `settings.json` | `~/Library/Application Support/Code/User/` | `VSCODE_USER_DATA` |

## Structure

### Global Instructions

| File | Description |
| --- | --- |
| [copilot-instructions.md](.github/copilot-instructions.md) | Workflow, MCP rules |
| [global-git-commit-instructions.md](.github/instructions/global-git-commit-instructions.md) | Conventional Commits |

### Skills

| Skill | Trigger Examples |
| --- | --- |
| [conventional-commit](.github/skills/conventional-commit/SKILL.md) | "write commit message" |

## Usage

### VS Code + GitHub Copilot

After installation, instructions apply automatically in Copilot Chat.

### Claude Code / Codex

```text
# Skills are auto-triggered during conversation
"write commit message"  # conventional-commit skill
```

## Customization

### Modify Instructions

1. Edit `.md` files.
2. Re-run `python setup-agents.py`.
3. Modify `.github/copilot-instructions.md` if needed.

### Add New Skill

```text
.github/skills/
└── my-skill/
    └── SKILL.md
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
| fetch | External web content |
| exa | AI-powered web search |
| grep-app | GitHub code search |

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
- [github/awesome-copilot](https://github.com/github.com/github/awesome-copilot) - Awesome Copilot resources

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
