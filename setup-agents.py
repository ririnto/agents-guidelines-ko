#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import datetime
import json
import logging
import os
import shutil
import sys
import tempfile
from pathlib import Path
from enum import StrEnum
from typing import Optional


class Target(StrEnum):
    VSCODE = "vscode"
    CODEX = "codex"
    CLAUDE = "claude"
    INTELLIJ = "intellij"


class Asset(StrEnum):
    AGENTS = "agents"
    SKILLS = "skills"
    PROMPTS = "prompts"
    RULES = "rules"


CONFIG = {
    "destinations": {
        "claude": {
            "base": Path.home() / ".claude",
            "agents": "agents",
            "skills": "skills",
            "prompts": "commands",
            "rules": "rules",
        },
        "codex": {
            "base": Path.home() / ".codex",
            "env": "CODEX_HOME",
            "agents": "agents",
            "skills": "skills",
            "prompts": "prompts",
        },
        "intellij": {
            "base": Path.home() / ".config" / "github-copilot" / "intellij",
            "agents": ".",
            "skills": None,
            "prompts": ".",
            "instructions": {
                "commit": "global-git-commit-instructions.md",
                "copilot": "global-copilot-instructions.md",
            },
        },
        "vscode": {
            "base": Path.home() / "Library" / "Application Support" / "Code" / "User",
            "env": "VSCODE_USER_DATA",
            "agents": "prompts",
            "skills": None,
            "prompts": "prompts",
        },
    },
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
    "vscode": {
        "settings-keys": {
            "commit-message-generation-instructions": "github.copilot.chat.commitMessageGeneration.instructions",
            "instructions-files-locations": "chat.instructionsFilesLocations",
        },
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


def setup_logger() -> logging.Logger:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    return logging.getLogger(__name__)


def get_repo_dir() -> Path:
    return Path(__file__).parent.resolve()


def get_source_path(repo_dir: Path, key: str) -> Path:
    """
    Get absolute path for a source file/directory.

    :param repo_dir: Repository root directory
    :param key: Source key in CONFIG
    :returns: Absolute path
    """
    source = CONFIG["sources"][key]
    if not isinstance(source, Path):
        raise TypeError(f"Source path for '{key}' must be a Path, got {type(source).__name__}")
    return repo_dir / source


def get_dest_base(tool_config: dict) -> Path:
    """
    Get base directory for a tool, respecting env var.

    :param tool_config: Tool configuration dict
    :returns: Expanded base directory path
    """
    env_var = tool_config.get("env")
    if env_var and os.environ.get(env_var):
        return Path(os.environ[env_var])
    return tool_config["base"]


def get_vscode_settings_path() -> tuple[Path, Path]:
    """
    Get VS Code settings.json path.

    :returns: Tuple of (settings_path, settings_dir)
    """
    base_dir = get_dest_base(CONFIG["destinations"]["vscode"])
    settings_path = base_dir / "settings.json"
    return settings_path, base_dir


def ensure_settings_file(settings_path: Path, settings_dir: Path, logger: logging.Logger) -> None:
    """
    Ensure settings file exists.

    :param settings_path: Path to settings.json
    :param settings_dir: Directory containing settings.json
    :param logger: Logger instance
    """
    settings_dir.mkdir(parents=True, exist_ok=True)
    if not settings_path.exists() or settings_path.stat().st_size == 0:
        settings_path.write_text("{}\n", encoding="utf-8")
        logger.info("Initialized settings file: %s", settings_path)


def load_settings(settings_path: Path) -> Optional[dict]:
    """
    Load settings from JSON file.

    :param settings_path: Path to settings.json
    :returns: Parsed settings dict or None on error
    """
    try:
        return json.loads(settings_path.read_text(encoding="utf-8"))
    except (ValueError, FileNotFoundError) as e:
        print(f"Error loading settings: {e}", file=sys.stderr)
        return None


def write_settings(settings_path: Path, settings_dir: Path, data: dict, logger: logging.Logger) -> None:
    """
    Write settings to JSON file atomically.

    :param settings_path: Path to settings.json
    :param settings_dir: Directory containing settings.json
    :param data: Settings data to write
    :param logger: Logger instance
    """
    fd, tmp_path = tempfile.mkstemp(prefix="settings.", suffix=".json", dir=settings_dir)
    os.close(fd)
    tmp_file = Path(tmp_path)
    tmp_file.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    tmp_file.replace(settings_path)
    logger.info("Updated settings file: %s", settings_path)


def update_vscode_settings(data: dict, repo_dir: Path, logger: logging.Logger) -> bool:
    """
    Update VS Code settings.json with repo paths.

    :param data: Settings data dict
    :param repo_dir: Repository root directory
    :param logger: Logger instance
    :returns: True on success
    """
    keys = CONFIG["vscode"]["settings-keys"]

    instructions_dir = str(get_source_path(repo_dir, "instructions"))
    instructions_locations = data.setdefault(keys["instructions-files-locations"], {})
    instructions_locations[instructions_dir] = True

    commit_file = str(get_source_path(repo_dir, "commit"))
    entry = {"file": commit_file}
    commit_instructions = data.setdefault(keys["commit-message-generation-instructions"], [])
    if not any(item.get("file") == commit_file for item in commit_instructions if isinstance(item, dict)):
        commit_instructions.append(entry)

    logger.info("Updated VS Code settings for repo: %s", repo_dir)
    return True


def backup_and_copy(dest_path: Path, backup_dir: Path, source_path: Path, logger: logging.Logger) -> None:
    """
    Backup existing file and copy source file.

    :param dest_path: Destination path for file copy
    :param backup_dir: Directory for backups
    :param source_path: Source file to copy
    :param logger: Logger instance
    """
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    if dest_path.exists() or dest_path.is_symlink():
        backup_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT-%H-%M-%S")
        if dest_path.suffix:
            backup_name = dest_path.stem + f".{timestamp}" + dest_path.suffix
        else:
            backup_name = dest_path.name + f".{timestamp}"
        dest_path.replace(backup_dir / backup_name)
        logger.info("Backed up %s", dest_path)
    shutil.copy2(source_path, dest_path)
    logger.info("Copied %s -> %s", source_path, dest_path)


def copy_intellij_instructions(repo_dir: Path, logger: logging.Logger) -> None:
    """
    Copy instructions files to IntelliJ Copilot directory.

    :param repo_dir: Repository root directory
    :param logger: Logger instance
    """
    intellij_config = CONFIG["destinations"].get("intellij")
    if not intellij_config or "instructions" not in intellij_config:
        return

    base_dir = get_dest_base(intellij_config)
    backup_dir = base_dir / "backup"
    instructions_map = intellij_config["instructions"]
    if not isinstance(instructions_map, dict):
        logger.warning("Skipping IntelliJ instructions: instructions config is invalid")
        return

    for source_key, target_name in instructions_map.items():
        if not isinstance(target_name, str):
            logger.warning("Skipping IntelliJ instruction %s: target must be a string", source_key)
            continue
        source_path = get_source_path(repo_dir, source_key)
        if not source_path.exists():
            print(f"Missing source: {source_path}", file=sys.stderr)
            continue
        dest_path = base_dir / target_name
        backup_and_copy(dest_path, backup_dir, source_path, logger)


def get_dest_paths(asset_type: Asset, targets: set[Target]) -> list[Path]:
    """
    Get destination paths for an asset type.

    :param asset_type: Asset type to copy
    :param targets: Set of target tool names to include
    :returns: List of destination directory paths
    """
    paths = []
    for tool_name, tool_config in CONFIG["destinations"].items():
        try:
            target = Target(tool_name)
        except ValueError:
            continue
        if target not in targets:
            continue
        subdir = tool_config.get(asset_type.value)
        if subdir is None:
            continue
        base = get_dest_base(tool_config)
        paths.append(base if subdir == "." else base / subdir)
    return paths


def copy_special_instructions(repo_dir: Path, logger: logging.Logger, targets: set[Target]) -> None:
    """
    Copy specific instruction files to tool roots.

    :param repo_dir: Repository root directory
    :param logger: Logger instance
    :param targets: Set of target tool names to include
    """
    for tool_name, copies in SPECIAL_INSTRUCTION_COPIES.items():
        try:
            target = Target(tool_name)
        except ValueError:
            continue
        if target not in targets:
            continue
        tool_config = CONFIG["destinations"].get(tool_name)
        if not tool_config:
            continue
        base_dir = get_dest_base(tool_config)
        backup_dir = base_dir / "backup"
        for entry in copies:
            source_key = entry.get("source")
            filename = entry.get("filename")
            if not isinstance(source_key, str) or not isinstance(filename, str):
                continue
            source_path = get_source_path(repo_dir, source_key)
            if not source_path.exists():
                print(f"Missing source: {source_path}", file=sys.stderr)
                continue
            dest_path = base_dir / filename
            backup_and_copy(dest_path, backup_dir, source_path, logger)


def copy_assets(
    src_dir: Path,
    asset_type: Asset,
    is_directory: bool,
    logger: logging.Logger,
    targets: set[Target],
) -> None:
    """
    Copy assets to destination directories.

    :param src_dir: Source directory containing assets
    :param asset_type: Asset type to copy
    :param is_directory: True if assets are directories (skills)
    :param logger: Logger instance
    :param targets: Set of target tool names to include
    """
    if not src_dir.is_dir():
        return
    dest_paths = get_dest_paths(asset_type, targets)
    for src_path in sorted(src_dir.iterdir()):
        if is_directory and not src_path.is_dir():
            continue
        if not is_directory and (not src_path.is_file() or src_path.suffix != ".md"):
            continue
        for dest_dir in dest_paths:
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_path = dest_dir / src_path.name
            if dest_path.is_symlink():
                dest_path.unlink()
            elif dest_path.is_dir():
                shutil.rmtree(dest_path)
            elif dest_path.exists():
                dest_path.unlink()
            if is_directory:
                shutil.copytree(src_path, dest_path)
            else:
                shutil.copy2(src_path, dest_path)
            logger.info("Copied %s: %s", asset_type.value, src_path.name)


def cleanup_old_symlinks(logger: logging.Logger, targets: set[Target]) -> None:
    """
    Remove old symlinks from all destination directories.

    :param logger: Logger instance
    :param targets: Set of target tool names to include
    """
    seen: set[Path] = set()
    for tool_name, tool_config in CONFIG["destinations"].items():
        try:
            target = Target(tool_name)
        except ValueError:
            continue
        if target not in targets:
            continue
        base = get_dest_base(tool_config)
        for asset_type in Asset:
            subdir = tool_config.get(asset_type.value)
            if subdir is None:
                continue
            dest_dir = base if subdir == "." else base / subdir
            if dest_dir in seen or not dest_dir.is_dir():
                continue
            seen.add(dest_dir)
            for dest_path in dest_dir.iterdir():
                if dest_path.is_symlink():
                    dest_path.unlink()
                    logger.info("Removed old symlink: %s", dest_path.name)


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.

    :returns: Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Setup agent configurations for various tools.")
    parser.add_argument(
        "targets",
        nargs="*",
        metavar="TARGET",
        choices=[target.value for target in Target],
        help=(f"Target environments to configure: {', '.join(target.value for target in Target)} (default: all)"),
    )
    args = parser.parse_args()
    if not args.targets:
        args.targets = [target.value for target in Target]
    return args


def main() -> int:
    """
    Main entry point.

    :returns: Exit code (0 for success, 1 for failure)
    """
    args = parse_args()
    targets: set[Target] = {Target(target) for target in args.targets}

    logger = setup_logger()
    repo_dir = get_repo_dir()

    if Target.VSCODE in targets:
        settings_path, settings_dir = get_vscode_settings_path()
        ensure_settings_file(settings_path, settings_dir, logger)
        data = load_settings(settings_path)
        if data is None:
            return 1
        update_vscode_settings(data, repo_dir, logger)
        write_settings(settings_path, settings_dir, data, logger)

    if Target.INTELLIJ in targets:
        copy_intellij_instructions(repo_dir, logger)

    claude_targets = targets & {Target.CLAUDE}
    non_claude_targets = targets - {Target.CLAUDE}

    for asset_type, is_dir in [(Asset.SKILLS, True), (Asset.PROMPTS, False)]:
        copy_assets(get_source_path(repo_dir, asset_type), asset_type, is_dir, logger, targets)

    if non_claude_targets:
        copy_assets(
            get_source_path(repo_dir, Asset.AGENTS.value),
            Asset.AGENTS,
            False,
            logger,
            non_claude_targets,
        )

    if claude_targets:
        copy_assets(
            get_source_path(repo_dir, "claude_agents"),
            Asset.AGENTS,
            False,
            logger,
            claude_targets,
        )
        copy_assets(
            get_source_path(repo_dir, "claude_rules"),
            Asset.RULES,
            False,
            logger,
            claude_targets,
        )

    copy_special_instructions(repo_dir, logger, targets)

    cleanup_old_symlinks(logger, targets)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
