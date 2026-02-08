from pathlib import Path

import pytest

from setup_agents.constants import Asset, Target, get_source_path


def test_get_source_path():
    repo_dir = Path("/fake/repo")
    source_path = get_source_path(repo_dir, "skills")
    assert source_path == repo_dir / ".github" / "skills"


def test_get_source_path_invalid_key():
    repo_dir = Path("/fake/repo")
    with pytest.raises(KeyError):
        get_source_path(repo_dir, "invalid_key")


def test_get_source_path_invalid_type():
    from setup_agents.constants import CONFIG

    original_sources = CONFIG["sources"].copy()
    CONFIG["sources"]["test"] = "invalid_type"  # type: ignore[assignment]

    try:
        repo_dir = Path("/fake/repo")
        with pytest.raises(TypeError):
            get_source_path(repo_dir, "test")
    finally:
        CONFIG["sources"] = original_sources


def test_asset_enum():
    assert Asset.SKILLS == "skills"


def test_target_enum():
    assert Target.VSCODE == "vscode"
    assert Target.CODEX == "codex"
    assert Target.CLAUDE == "claude"
    assert Target.INTELLIJ == "intellij"
