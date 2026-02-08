from enum import StrEnum
from pathlib import Path

CONFIG = {
    "sources": {
        "commit": Path(".github") / "instructions" / "global-git-commit-instructions.md",
        "copilot": Path(".github") / "copilot-instructions.md",
        "instructions": Path(".github") / "instructions",
        "skills": Path(".github") / "skills",
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
    SKILLS = "skills"


class Target(StrEnum):
    VSCODE = "vscode"
    CODEX = "codex"
    CLAUDE = "claude"
    INTELLIJ = "intellij"
