import pytest

from setup_agents.agents.intellij import IntelliJAgentSetup


@pytest.fixture
def mock_logger():
    import logging

    return logging.getLogger("test_logger")


def test_intellij_instructions_map():
    assert IntelliJAgentSetup.instructions_map == {
        "commit": "global-git-commit-instructions.md",
        "copilot": "global-copilot-instructions.md",
    }


def test_intellij_copy_instructions_with_valid_sources(tmp_path, mock_logger, mocker):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    (repo_dir / ".github" / "instructions").mkdir(parents=True)

    commit_file = repo_dir / ".github" / "instructions" / "global-git-commit-instructions.md"
    commit_file.write_text("# Commit")

    mocker.patch.dict("os.environ", {}, clear=True)
    setup = IntelliJAgentSetup(repo_dir, mock_logger)
    setup._copy_instructions()

    assert (setup.base_dir / "global-git-commit-instructions.md").exists()


def test_intellij_copy_instructions_missing_source(tmp_path, mock_logger, mocker, capsys):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    (repo_dir / ".github" / "instructions").mkdir(parents=True)

    mocker.patch.dict("os.environ", {}, clear=True)
    setup = IntelliJAgentSetup(repo_dir, mock_logger)
    setup._copy_instructions()

    captured = capsys.readouterr()
    assert "Missing source" in captured.err


def test_intellij_copy_instructions_invalid_instructions_map(tmp_path, mock_logger, mocker):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()

    mocker.patch.object(IntelliJAgentSetup, "instructions_map", "invalid")
    mocker.patch.dict("os.environ", {}, clear=True)
    setup = IntelliJAgentSetup(repo_dir, mock_logger)
    setup._copy_instructions()
