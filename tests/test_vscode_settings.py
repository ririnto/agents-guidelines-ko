from pathlib import Path

from setup_agents.utils.vscode_settings import VSCodeSettings, SETTINGS_KEYS


def test_vscode_settings_initialization():
    import logging

    settings_path = Path("/fake/settings.json")
    settings_dir = Path("/fake")
    repo_dir = Path("/repo")
    logger = logging.getLogger("test")

    settings = VSCodeSettings(settings_path, settings_dir, repo_dir, logger)
    assert settings.settings_path == settings_path
    assert settings.settings_dir == settings_dir
    assert settings.repo_dir == repo_dir
    assert settings.logger == logger


def test_vscode_settings_get_path():
    repo_dir = Path("/repo")

    settings_path, settings_dir = VSCodeSettings.get_path(repo_dir)
    assert isinstance(settings_path, Path)
    assert isinstance(settings_dir, Path)
    assert settings_path.name == "settings.json"


def test_vscode_settings_ensure_new_file(tmp_path):
    import logging

    settings_dir = tmp_path / "settings"
    settings_dir.mkdir()
    settings_path = settings_dir / "settings.json"
    logger = logging.getLogger("test")

    settings = VSCodeSettings(settings_path, settings_dir, Path("/repo"), logger)
    settings.ensure()

    assert settings_path.exists()
    assert settings_path.read_text() == "{}\n"


def test_vscode_settings_ensure_existing_empty_file(tmp_path):
    import logging

    settings_dir = tmp_path / "settings"
    settings_dir.mkdir()
    settings_path = settings_dir / "settings.json"
    settings_path.write_text("")
    logger = logging.getLogger("test")

    settings = VSCodeSettings(settings_path, settings_dir, Path("/repo"), logger)
    settings.ensure()

    assert settings_path.read_text() == "{}\n"


def test_vscode_settings_ensure_existing_non_empty_file(tmp_path):
    import logging

    settings_dir = tmp_path / "settings"
    settings_dir.mkdir()
    settings_path = settings_dir / "settings.json"
    settings_path.write_text('{"existing": true}')
    logger = logging.getLogger("test")

    settings = VSCodeSettings(settings_path, settings_dir, Path("/repo"), logger)
    settings.ensure()

    assert settings_path.read_text() == '{"existing": true}'


def test_vscode_settings_load_valid_json(tmp_path):
    import logging

    settings_file = tmp_path / "settings.json"
    settings_file.write_text('{"key": "value"}')
    logger = logging.getLogger("test")

    settings = VSCodeSettings(settings_file, Path("/dir"), Path("/repo"), logger)
    result = settings.load()

    assert result == {"key": "value"}


def test_vscode_settings_load_invalid_json(tmp_path):
    import logging

    settings_file = tmp_path / "settings.json"
    settings_file.write_text("{invalid}")
    logger = logging.getLogger("test")

    settings = VSCodeSettings(settings_file, Path("/dir"), Path("/repo"), logger)
    result = settings.load()

    assert result is None


def test_vscode_settings_load_missing_file(tmp_path):
    import logging

    settings_file = tmp_path / "nonexistent.json"
    logger = logging.getLogger("test")

    settings = VSCodeSettings(settings_file, Path("/dir"), Path("/repo"), logger)
    result = settings.load()

    assert result is None


def test_vscode_settings_write(tmp_path):
    import json
    import logging

    settings_dir = tmp_path / "settings"
    settings_dir.mkdir()
    settings_path = settings_dir / "settings.json"
    logger = logging.getLogger("test")

    settings = VSCodeSettings(settings_path, settings_dir, Path("/repo"), logger)
    data = {"key": "value", "nested": {"a": 1}}
    settings.write(data)

    assert settings_path.exists()
    loaded = json.loads(settings_path.read_text())
    assert loaded == data


def test_vscode_settings_update(tmp_path):
    import logging

    settings_dir = tmp_path / "settings"
    settings_dir.mkdir()
    settings_path = settings_dir / "settings.json"
    logger = logging.getLogger("test")

    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    (repo_dir / ".github" / "instructions").mkdir(parents=True)
    (repo_dir / ".github" / "instructions" / "global-git-commit-instructions.md").write_text("# commit")

    settings = VSCodeSettings(settings_path, settings_dir, repo_dir, logger)
    data = {}
    result = settings.update(data)

    assert result is True
    assert SETTINGS_KEYS["instructions-files-locations"] in data
    assert SETTINGS_KEYS["commit-message-generation-instructions"] in data


def test_settings_keys():
    assert (
        SETTINGS_KEYS["commit-message-generation-instructions"]
        == "github.copilot.chat.commitMessageGeneration.instructions"
    )
    assert SETTINGS_KEYS["instructions-files-locations"] == "chat.instructionsFilesLocations"
