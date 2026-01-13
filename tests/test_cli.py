import sys
from pathlib import Path

import pytest

from setup_agents.cli import get_repo_dir, main, parse_args


def test_get_repo_dir():
    repo_dir = get_repo_dir()
    assert isinstance(repo_dir, Path)
    assert repo_dir.exists()
    assert repo_dir.name == "agents-guidelines-ko"


def test_parse_args_no_targets(mocker):
    mocker.patch.object(sys, "argv", ["setup-agents.py"])
    args = parse_args()
    assert args.targets == ["vscode", "codex", "claude", "intellij"]


def test_parse_args_with_targets(mocker):
    mocker.patch.object(sys, "argv", ["setup-agents.py", "claude", "vscode"])
    args = parse_args()
    assert args.targets == ["claude", "vscode"]


def test_parse_args_invalid_target(mocker):
    mocker.patch.object(sys, "argv", ["setup-agents.py", "invalid"])
    with pytest.raises(SystemExit):
        parse_args()


@pytest.mark.parametrize("targets", [[], ["vscode"], ["claude", "codex"]])
def test_main_with_mocked_agents(targets, mocker):
    mocker.patch.object(sys, "argv", ["setup-agents.py"] + targets)
    MockVSCode = mocker.patch("setup_agents.cli.VSCodeAgentSetup")
    MockCodex = mocker.patch("setup_agents.cli.CodexAgentSetup")
    MockClaude = mocker.patch("setup_agents.cli.ClaudeAgentSetup")
    MockIntelliJ = mocker.patch("setup_agents.cli.IntelliJAgentSetup")

    result = main()
    assert result == 0

    for mock_class in [MockVSCode, MockCodex, MockClaude, MockIntelliJ]:
        if mock_class.return_value:
            mock_instance = mock_class.return_value
            mock_instance.setup.assert_called_once()
