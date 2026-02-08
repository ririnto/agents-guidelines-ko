from pathlib import Path

from setup_agents.utils.file_utils import FileUtils


def test_get_dest_base_no_env(mocker):
    tool_config = {
        "base": Path("/fake/base"),
        "env": "FAKE_ENV",
    }
    mocker.patch.dict("os.environ", {}, clear=True)
    result = FileUtils.get_dest_base(tool_config)
    assert result == Path("/fake/base")


def test_get_dest_base_with_env(mocker):
    tool_config = {
        "base": Path("/fake/base"),
        "env": "FAKE_ENV",
    }
    mocker.patch.dict("os.environ", {"FAKE_ENV": "/env/path"})
    result = FileUtils.get_dest_base(tool_config)
    assert result == Path("/env/path")


def test_get_dest_base_no_env_key():
    tool_config = {
        "base": Path("/fake/base"),
    }
    result = FileUtils.get_dest_base(tool_config)
    assert result == Path("/fake/base")


def test_backup_and_copy_new_file(tmp_path, caplog):
    import logging

    logging.basicConfig(level=logging.INFO)

    source = tmp_path / "source.txt"
    source.write_text("content")

    dest = tmp_path / "subdir" / "dest.txt"
    backup_dir = tmp_path / "backup"
    logger = logging.getLogger(__name__)

    FileUtils.backup_and_copy(dest, backup_dir, source, logger)

    assert dest.exists()
    assert dest.read_text() == "content"
    assert not backup_dir.exists()


def test_backup_and_copy_existing_file(tmp_path, caplog):
    import logging

    logging.basicConfig(level=logging.INFO)

    source = tmp_path / "source.txt"
    source.write_text("new content")

    dest = tmp_path / "dest.txt"
    dest.write_text("old content")

    backup_dir = tmp_path / "backup"
    logger = logging.getLogger(__name__)

    FileUtils.backup_and_copy(dest, backup_dir, source, logger)

    assert dest.read_text() == "new content"
    assert backup_dir.exists()
    assert len(list(backup_dir.iterdir())) == 1


def test_get_dest_paths_with_subdir():
    from setup_agents.constants import Asset

    tool_config = {
        "base": Path("/fake/base"),
        Asset.SKILLS: "skills",
    }
    paths = FileUtils.get_dest_paths(Asset.SKILLS, tool_config)
    assert paths == [Path("/fake/base/skills")]


def test_get_dest_paths_no_subdir():
    from setup_agents.constants import Asset

    tool_config = {
        "base": Path("/fake/base"),
        Asset.SKILLS: None,
    }
    paths = FileUtils.get_dest_paths(Asset.SKILLS, tool_config)
    assert paths == []


def test_get_dest_paths_dot_subdir():
    from setup_agents.constants import Asset

    tool_config = {
        "base": Path("/fake/base"),
        Asset.SKILLS: ".",
    }
    paths = FileUtils.get_dest_paths(Asset.SKILLS, tool_config)
    assert paths == [Path("/fake/base")]


def test_cleanup_old_symlinks(tmp_path):
    import logging

    logging.basicConfig(level=logging.INFO)

    symlink_dir = tmp_path / "assets"
    symlink_dir.mkdir()
    (symlink_dir / "symlink.md").symlink_to(tmp_path / "real.md")
    (tmp_path / "real.md").write_text("content")

    from setup_agents.constants import Asset

    tool_config = {
        "base": tmp_path,
        Asset.SKILLS: "assets",
    }
    logger = logging.getLogger(__name__)

    FileUtils.cleanup_old_symlinks(tool_config, logger)

    assert not (symlink_dir / "symlink.md").exists()
