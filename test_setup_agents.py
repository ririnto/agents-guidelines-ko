#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for setup-agents.py"""

import json
import tempfile
from pathlib import Path
from types import ModuleType
from typing import Iterator
from unittest.mock import MagicMock, patch
import pytest
import importlib.util
import sys

spec = importlib.util.spec_from_file_location(
    "setup_agents", Path(__file__).parent / "setup-agents.py"
)
if spec is None or spec.loader is None:
    raise ImportError("Failed to load setup_agents module")
setup_agents: ModuleType = importlib.util.module_from_spec(spec)
sys.modules["setup_agents"] = setup_agents
spec.loader.exec_module(setup_agents)


@pytest.fixture
def temp_dir() -> Iterator[Path]:
    """Fixture to create and cleanup temporary directory"""
    import shutil

    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


def test_get_dest_base_with_env_var():
    """Test get_dest_base with environment variable"""
    tool_config = {"base": Path("/default/path"), "env": "TEST_ENV_VAR"}

    with patch.dict("os.environ", {"TEST_ENV_VAR": "/custom/path"}):
        result = setup_agents.get_dest_base(tool_config)
        assert result == Path("/custom/path")


def test_get_dest_base_without_env_var():
    """Test get_dest_base without environment variable"""
    tool_config = {"base": Path("/default/path")}

    result = setup_agents.get_dest_base(tool_config)
    assert result == Path("/default/path")


def test_backup_and_copy(temp_dir):
    """Test backup_and_copy function"""
    src_dir = temp_dir / "source"
    dest_dir = temp_dir / "destination"
    backup_dir = temp_dir / "backup"

    src_dir.mkdir()
    dest_dir.mkdir()

    source_file = src_dir / "test.md"
    source_file.write_text("Test content")

    dest_file = dest_dir / "test.md"
    dest_file.write_text("Old content")

    logger = MagicMock()

    setup_agents.backup_and_copy(dest_file, backup_dir, source_file, logger)

    assert dest_file.exists()
    assert dest_file.read_text() == "Test content"

    assert backup_dir.exists()
    backup_files = list(backup_dir.iterdir())
    assert len(backup_files) == 1
    assert "test." in backup_files[0].name
    assert backup_files[0].read_text() == "Old content"


def test_backup_naming_with_extension(temp_dir):
    """Test backup naming preserves file extension"""
    src_dir = temp_dir / "source"
    dest_dir = temp_dir / "destination"
    backup_dir = temp_dir / "backup"

    src_dir.mkdir()
    dest_dir.mkdir()

    source_file = src_dir / "test.md"
    source_file.write_text("Content")

    dest_file = dest_dir / "test.md"
    dest_file.write_text("Old")

    logger = MagicMock()
    setup_agents.backup_and_copy(dest_file, backup_dir, source_file, logger)

    backup_files = list(backup_dir.iterdir())
    assert backup_files[0].name.endswith(".md")


def test_backup_naming_without_extension(temp_dir):
    """Test backup naming for files without extension"""
    src_dir = temp_dir / "source"
    dest_dir = temp_dir / "destination"
    backup_dir = temp_dir / "backup"

    src_dir.mkdir()
    dest_dir.mkdir()

    source_file = src_dir / "config"
    source_file.write_text("Content")

    dest_file = dest_dir / "config"
    dest_file.write_text("Old")

    logger = MagicMock()
    setup_agents.backup_and_copy(dest_file, backup_dir, source_file, logger)

    backup_files = list(backup_dir.iterdir())
    assert backup_files[0].name.startswith("config.")


def test_copy_assets_files(temp_dir):
    """Test copy_assets with files"""
    src_dir = temp_dir / "source"
    dest_dir = temp_dir / "destination"

    src_dir.mkdir()
    dest_dir.mkdir()

    (src_dir / "test1.md").write_text("Content 1")
    (src_dir / "test2.md").write_text("Content 2")
    (src_dir / "ignore.txt").write_text("Ignored")  # Non-.md file

    logger = MagicMock()

    with patch.object(setup_agents, "get_dest_paths", return_value=[dest_dir]):
        setup_agents.copy_assets(
            src_dir,
            setup_agents.Asset.PROMPTS,
            False,
            logger,
            {setup_agents.Target.CODEX},
        )

    assert (dest_dir / "test1.md").exists()
    assert (dest_dir / "test2.md").exists()
    assert not (dest_dir / "ignore.txt").exists()


def test_copy_assets_directories(temp_dir):
    """Test copy_assets with directories (skills)"""
    src_dir = temp_dir / "source"
    dest_dir = temp_dir / "destination"

    src_dir.mkdir()
    dest_dir.mkdir()

    skill_dir = src_dir / "test-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("Skill content")
    (skill_dir / "helper.py").write_text("Helper code")

    logger = MagicMock()

    with patch.object(setup_agents, "get_dest_paths", return_value=[dest_dir]):
        setup_agents.copy_assets(
            src_dir,
            setup_agents.Asset.SKILLS,
            True,
            logger,
            {setup_agents.Target.CODEX},
        )

    assert (dest_dir / "test-skill").is_dir()
    assert (dest_dir / "test-skill" / "SKILL.md").exists()
    assert (dest_dir / "test-skill" / "helper.py").exists()


def test_cleanup_old_symlinks(temp_dir):
    """Test cleanup_old_symlinks removes symlinks"""
    dest_dir = temp_dir / "destination"
    dest_dir.mkdir()

    regular_file = dest_dir / "regular.md"
    regular_file.write_text("Content")

    symlink_file = dest_dir / "symlink.md"
    target = temp_dir / "target.md"
    target.write_text("Target")
    symlink_file.symlink_to(target)

    logger = MagicMock()

    with patch.dict(
        setup_agents.CONFIG["destinations"],
        {
            setup_agents.Target.CODEX.value: {
                "base": dest_dir.parent,
                "agents": dest_dir.name,
                "skills": None,
                "prompts": None,
                "rules": None,
            }
        },
    ):
        setup_agents.cleanup_old_symlinks(logger, {setup_agents.Target.CODEX})

    assert regular_file.exists()
    assert not symlink_file.exists()


def test_load_settings_valid_json(temp_dir):
    """Test load_settings with valid JSON"""
    settings_file = temp_dir / "settings.json"
    settings_data = {"key": "value", "number": 42}
    settings_file.write_text(json.dumps(settings_data))

    result = setup_agents.load_settings(settings_file)
    assert result == settings_data


def test_load_settings_invalid_json(temp_dir):
    """Test load_settings with invalid JSON"""
    settings_file = temp_dir / "settings.json"
    settings_file.write_text("{ invalid json }")

    result = setup_agents.load_settings(settings_file)
    assert result is None


def test_load_settings_missing_file(temp_dir):
    """Test load_settings with missing file"""
    settings_file = temp_dir / "nonexistent.json"

    result = setup_agents.load_settings(settings_file)
    assert result is None


def test_write_settings(temp_dir):
    """Test write_settings creates valid JSON file"""
    settings_dir = temp_dir / "settings"
    settings_dir.mkdir()
    settings_file = settings_dir / "settings.json"

    data = {"key": "value", "nested": {"a": 1, "b": 2}}
    logger = MagicMock()

    setup_agents.write_settings(settings_file, settings_dir, data, logger)

    assert settings_file.exists()
    loaded_data = json.loads(settings_file.read_text())
    assert loaded_data == data


def test_copy_special_instructions(temp_dir):
    """Test copy_special_instructions copies copilot instructions to each tool."""
    repo_dir = temp_dir / "repo"
    copilot_dir = repo_dir / ".github"
    copilot_dir.mkdir(parents=True)
    copilot_file = copilot_dir / "copilot-instructions.md"
    copilot_file.write_text("# Copilot instructions")

    codex_base = temp_dir / "codex"
    claude_base = temp_dir / "claude"

    logger = MagicMock()
    targets = {setup_agents.Target.CODEX, setup_agents.Target.CLAUDE}

    with patch.dict(
        setup_agents.CONFIG["destinations"],
        {
            setup_agents.Target.CODEX.value: {
                "base": codex_base,
                "agents": "agents",
                "skills": None,
                "prompts": None,
                "rules": None,
            },
            setup_agents.Target.CLAUDE.value: {
                "base": claude_base,
                "agents": "agents",
                "skills": "skills",
                "prompts": "commands",
                "rules": "rules",
            },
        },
        clear=False,
    ):
        setup_agents.copy_special_instructions(repo_dir, logger, targets)

    assert (codex_base / "AGENTS.md").exists()
    assert (codex_base / "AGENTS.md").read_text() == "# Copilot instructions"
    assert (claude_base / "CLAUDE.md").exists()
    assert (claude_base / "CLAUDE.md").read_text() == "# Copilot instructions"
