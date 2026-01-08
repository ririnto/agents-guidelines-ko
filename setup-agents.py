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
from typing import Optional

ALL_TARGETS = ("vscode", "codex", "claude", "intellij")

CONFIG = {
    "destinations": {
        "claude": {
            "base": Path.home() / ".claude",
            "agents": "agents",
            "skills": "skills",
            "prompts": "commands",
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
        "commit": Path(".github")
        / "instructions"
        / "global-git-commit-instructions.md",
        "copilot": Path(".github") / "copilot-instructions.md",
        "instructions": Path(".github") / "instructions",
        "prompts": Path(".github") / "prompts",
        "skills": Path(".github") / "skills",
    },
    "vscode": {
        "settings-keys": {
            "commit-message-generation-instructions": "github.copilot.chat.commitMessageGeneration.instructions",
            "instructions-files-locations": "chat.instructionsFilesLocations",
        },
    },
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
    return repo_dir / CONFIG["sources"][key]


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


def ensure_settings_file(
    settings_path: Path, settings_dir: Path, logger: logging.Logger
) -> None:
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


def write_settings(
    settings_path: Path, settings_dir: Path, data: dict, logger: logging.Logger
) -> None:
    """
    Write settings to JSON file atomically.

    :param settings_path: Path to settings.json
    :param settings_dir: Directory containing settings.json
    :param data: Settings data to write
    :param logger: Logger instance
    """
    fd, tmp_path = tempfile.mkstemp(
        prefix="settings.", suffix=".json", dir=settings_dir
    )
    os.close(fd)
    tmp_file = Path(tmp_path)
    tmp_file.write_text(
        json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
    )
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
    commit_instructions = data.setdefault(
        keys["commit-message-generation-instructions"], []
    )
    if not any(
        item.get("file") == commit_file
        for item in commit_instructions
        if isinstance(item, dict)
    ):
        commit_instructions.append(entry)

    logger.info("Updated VS Code settings for repo: %s", repo_dir)
    return True


def backup_and_copy(
    dest_path: Path, backup_dir: Path, source_path: Path, logger: logging.Logger
) -> None:
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
        backup_name = dest_path.name.replace(".md", f".{timestamp}.md")
        dest_path.replace(backup_dir / backup_name)
        logger.info("Backed up %s", dest_path)
    if dest_path.is_symlink() or dest_path.exists():
        dest_path.unlink()
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

    for source_key, target_name in instructions_map.items():
        source_path = get_source_path(repo_dir, source_key)
        if not source_path.exists():
            print(f"Missing source: {source_path}", file=sys.stderr)
            continue
        dest_path = base_dir / target_name
        backup_and_copy(dest_path, backup_dir, source_path, logger)


def get_dest_paths(asset_type: str, targets: set[str]) -> list[Path]:
    """
    Get destination paths for an asset type.

    :param asset_type: One of 'agents', 'skills', 'prompts'
    :param targets: Set of target tool names to include
    :returns: List of destination directory paths
    """
    paths = []
    for tool_name, tool_config in CONFIG["destinations"].items():
        if tool_name not in targets:
            continue
        subdir = tool_config.get(asset_type)
        if subdir is None:
            continue
        base = get_dest_base(tool_config)
        paths.append(base if subdir == "." else base / subdir)
    return paths


def copy_assets(
    src_dir: Path,
    asset_type: str,
    is_directory: bool,
    logger: logging.Logger,
    targets: set[str],
) -> None:
    """
    Copy assets to destination directories.

    :param src_dir: Source directory containing assets
    :param asset_type: One of 'agents', 'skills', 'prompts'
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
            if dest_path.is_symlink() or dest_path.exists():
                if dest_path.is_dir() and not dest_path.is_symlink():
                    shutil.rmtree(dest_path)
                else:
                    dest_path.unlink()
            if is_directory:
                shutil.copytree(src_path, dest_path)
            else:
                shutil.copy2(src_path, dest_path)
            logger.info("Copied %s: %s", asset_type[:-1], src_path.name)


def cleanup_old_files(logger: logging.Logger, targets: set[str]) -> None:
    """
    Remove old symlinks from all destination directories.

    :param logger: Logger instance
    :param targets: Set of target tool names to include
    """
    seen: set[Path] = set()
    for tool_name, tool_config in CONFIG["destinations"].items():
        if tool_name not in targets:
            continue
        base = get_dest_base(tool_config)
        for asset_type in ("agents", "skills", "prompts"):
            subdir = tool_config.get(asset_type)
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
    parser = argparse.ArgumentParser(
        description="Setup agent configurations for various tools."
    )
    parser.add_argument(
        "targets",
        nargs="*",
        metavar="TARGET",
        help=f"Target environments to configure: {', '.join(ALL_TARGETS)} (default: all)",
    )
    args = parser.parse_args()
    if not args.targets:
        args.targets = list(ALL_TARGETS)
    else:
        invalid = set(args.targets) - set(ALL_TARGETS)
        if invalid:
            parser.error(
                f"invalid target(s): {', '.join(invalid)} (choose from {', '.join(ALL_TARGETS)})"
            )
    return args


def main() -> int:
    """
    Main entry point.

    :returns: Exit code (0 for success, 1 for failure)
    """
    args = parse_args()
    targets: set[str] = set(args.targets) if args.targets else set(ALL_TARGETS)

    logger = setup_logger()
    repo_dir = get_repo_dir()

    if "vscode" in targets:
        settings_path, settings_dir = get_vscode_settings_path()
        ensure_settings_file(settings_path, settings_dir, logger)
        data = load_settings(settings_path)
        if data is None:
            return 1
        update_vscode_settings(data, repo_dir, logger)
        write_settings(settings_path, settings_dir, data, logger)

    if "intellij" in targets:
        copy_intellij_instructions(repo_dir, logger)

    for asset_type, is_dir in [("skills", True), ("prompts", False), ("agents", False)]:
        copy_assets(
            get_source_path(repo_dir, asset_type), asset_type, is_dir, logger, targets
        )

    cleanup_old_files(logger, targets)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
