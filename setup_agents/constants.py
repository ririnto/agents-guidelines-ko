from enum import StrEnum
from pathlib import Path

CONFIG = {
    "sources": {
        "agents": Path(".github") / "agents",
        "commit": Path(".github") / "instructions" / "global-git-commit-instructions.md",
        "copilot": Path(".github") / "copilot-instructions.md",
        "instructions": Path(".github") / "instructions",
        "prompts": Path(".github") / "prompts",
        "skills": Path(".github") / "skills",
        "claude_agents": Path(".claude") / "agents",
        "claude_rules": Path(".claude") / "rules",
    },
}

SPECIAL_INSTRUCTION_COPIES = {
    "codex": [
        {"source": "copilot", "filename": "AGENTS.md"},
    ],
    "claude": [
        {"source": "copilot", "filename": "CLAUDE.md"},
    ],
}


def get_source_path(repo_dir: Path, key: str) -> Path:
    source = CONFIG["sources"][key]
    if not isinstance(source, Path):
        raise TypeError(f"Source path for '{key}' must be a Path, got {type(source).__name__}")
    return repo_dir / source


class Asset(StrEnum):
    AGENTS = "agents"
    SKILLS = "skills"
    PROMPTS = "prompts"
    RULES = "rules"


class Target(StrEnum):
    VSCODE = "vscode"
    CODEX = "codex"
    CLAUDE = "claude"
    INTELLIJ = "intellij"
