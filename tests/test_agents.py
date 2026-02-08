from pathlib import Path

import pytest

from setup_agents.constants import Target
from setup_agents.agents.claude import ClaudeAgentSetup
from setup_agents.agents.codex import CodexAgentSetup
from setup_agents.agents.intellij import IntelliJAgentSetup
from setup_agents.agents.vscode import VSCodeAgentSetup


@pytest.fixture
def mock_logger():
    import logging

    return logging.getLogger("test_logger")


def test_vscode_setup_initialization(mock_repo_dir, mock_logger):
    setup = VSCodeAgentSetup(mock_repo_dir, mock_logger)
    assert setup.base == Path.home() / "Library" / "Application Support" / "Code" / "User"
    assert setup.env == "VSCODE_USER_DATA"


def test_vscode_setup_no_targets(mock_repo_dir, mock_logger, mocker):
    mocker.patch.object(VSCodeAgentSetup, "_get_settings_path")
    setup = VSCodeAgentSetup(mock_repo_dir, mock_logger)
    setup.setup(set())


def test_vscode_setup_with_vscode_target(mock_repo_dir, mock_logger, mocker, tmp_path):
    targets = {Target.VSCODE}

    settings_path = tmp_path / "settings.json"
    settings_dir = tmp_path

    mock_get_path = mocker.patch.object(
        VSCodeAgentSetup, "_get_settings_path", return_value=(settings_path, settings_dir)
    )

    mocker.patch.object(VSCodeAgentSetup, "_copy_common_assets")
    mocker.patch.object(VSCodeAgentSetup, "cleanup_symlinks")

    setup = VSCodeAgentSetup(mock_repo_dir, mock_logger)
    setup.setup(targets)

    mock_get_path.assert_called_once()
    assert settings_path.exists()


def test_codex_setup_initialization(mock_repo_dir, mock_logger):
    setup = CodexAgentSetup(mock_repo_dir, mock_logger)
    assert setup.base == Path.home() / ".codex"
    assert setup.env == "CODEX_HOME"


def test_codex_setup_no_targets(mock_repo_dir, mock_logger, mocker):
    mock_method = mocker.patch.object(CodexAgentSetup, "_copy_common_assets")
    setup = CodexAgentSetup(mock_repo_dir, mock_logger)
    setup.setup(set())
    mock_method.assert_not_called()


def test_codex_setup_with_codex_target(mock_repo_dir, mock_logger, mocker):
    targets = {Target.CODEX}

    mock_common = mocker.patch.object(CodexAgentSetup, "_copy_common_assets")
    mock_special = mocker.patch.object(CodexAgentSetup, "copy_special_files")
    mock_cleanup = mocker.patch.object(CodexAgentSetup, "cleanup_symlinks")

    setup = CodexAgentSetup(mock_repo_dir, mock_logger)
    setup.setup(targets)

    mock_common.assert_called_once()
    mock_special.assert_called_once()
    mock_cleanup.assert_called_once()


def test_claude_setup_initialization(mock_repo_dir, mock_logger):
    setup = ClaudeAgentSetup(mock_repo_dir, mock_logger)
    assert setup.base == Path.home() / ".claude"
    assert setup.env is None


def test_claude_setup_no_targets(mock_repo_dir, mock_logger, mocker):
    mock_method = mocker.patch.object(ClaudeAgentSetup, "_copy_common_assets")
    setup = ClaudeAgentSetup(mock_repo_dir, mock_logger)
    setup.setup(set())
    mock_method.assert_not_called()


def test_claude_setup_with_claude_target(mock_repo_dir, mock_logger, mocker):
    targets = {Target.CLAUDE}

    mock_common = mocker.patch.object(ClaudeAgentSetup, "_copy_common_assets")
    mock_special = mocker.patch.object(ClaudeAgentSetup, "copy_special_files")
    mock_cleanup = mocker.patch.object(ClaudeAgentSetup, "cleanup_symlinks")

    setup = ClaudeAgentSetup(mock_repo_dir, mock_logger)
    setup.setup(targets)

    mock_common.assert_called_once()
    mock_special.assert_called_once()
    mock_cleanup.assert_called_once()


def test_intellij_setup_initialization(mock_repo_dir, mock_logger):
    setup = IntelliJAgentSetup(mock_repo_dir, mock_logger)
    assert setup.base == Path.home() / ".config" / "github-copilot" / "intellij"
    assert setup.env is None


def test_intellij_setup_no_targets(mock_repo_dir, mock_logger, mocker):
    mock_method = mocker.patch.object(IntelliJAgentSetup, "_copy_instructions")
    setup = IntelliJAgentSetup(mock_repo_dir, mock_logger)
    setup.setup(set())
    mock_method.assert_not_called()


def test_intellij_setup_with_intellij_target(mock_repo_dir, mock_logger, mocker):
    targets = {Target.INTELLIJ}

    mock_instructions = mocker.patch.object(IntelliJAgentSetup, "_copy_instructions")
    mock_common = mocker.patch.object(IntelliJAgentSetup, "_copy_common_assets")
    mock_cleanup = mocker.patch.object(IntelliJAgentSetup, "cleanup_symlinks")

    setup = IntelliJAgentSetup(mock_repo_dir, mock_logger)
    setup.setup(targets)

    mock_instructions.assert_called_once()
    mock_common.assert_called_once()
    mock_cleanup.assert_called_once()


def test_base_dir_with_env_var(tmp_path, mock_logger, mocker):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()

    mocker.patch.dict("os.environ", {"CODEX_HOME": "/custom/path"})
    setup = CodexAgentSetup(repo_dir, mock_logger)
    assert setup.base_dir == Path("/custom/path")


def test_base_dir_without_env_var(tmp_path, mock_logger, mocker):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()

    mocker.patch.dict("os.environ", {}, clear=True)
    setup = CodexAgentSetup(repo_dir, mock_logger)
    assert setup.base_dir == Path.home() / ".codex"
