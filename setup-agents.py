#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import datetime
import json
import logging
import os
import sys
import tempfile
from typing import Optional

ALL_TARGETS = ("vscode", "codex", "claude", "intellij")

CONFIG = {
    "destinations": {
        "claude": {
            "base": "~/.claude",
            "agents": "agents",
            "skills": "skills",
            "prompts": "commands",
        },
        "codex": {
            "base": "~/.codex",
            "env": "CODEX_HOME",
            "agents": "agents",
            "skills": "skills",
            "prompts": "prompts",
        },
        "intellij": {
            "base": "~/.config/github-copilot/intellij",
            "agents": ".",
            "skills": None,
            "prompts": ".",
            "instructions": {
                "commit": "global-git-commit-instructions.md",
                "copilot": "global-copilot-instructions.md",
            },
        },
        "vscode": {
            "base": "~/Library/Application Support/Code/User",
            "agents": "prompts",
            "skills": None,
            "prompts": "prompts",
        },
    },
    "sources": {
        "agents": [".github", "agents"],
        "commit": [".github", "instructions", "global-git-commit-instructions.md"],
        "copilot": [".github", "copilot-instructions.md"],
        "instructions": [".github", "instructions"],
        "prompts": [".github", "prompts"],
        "skills": [".github", "skills"],
    },
    "vscode": {
        "settings-keys": {
            "commit-instructions": "github.copilot.chat.commitMessageGeneration.instructions",
            "instructions-locations": "chat.instructionsFilesLocations",
            "prompt-locations": "chat.promptFilesLocations",
        },
        "settings-path": ["Library", "Application Support", "Code", "User", "settings.json"],
    },
}


def setup_logger() -> logging.Logger:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    return logging.getLogger(__name__)


def get_repo_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def get_source_path(repo_dir: str, key: str) -> str:
    """
    Get absolute path for a source file/directory.

    :param repo_dir: Repository root directory
    :param key: Source key in CONFIG
    :returns: Absolute path
    """
    return os.path.join(repo_dir, *CONFIG["sources"][key])


def get_dest_base(tool_config: dict) -> str:
    """
    Get base directory for a tool, respecting env var.

    :param tool_config: Tool configuration dict
    :returns: Expanded base directory path
    """
    env_var = tool_config.get("env")
    if env_var and os.environ.get(env_var):
        return os.environ[env_var]
    return os.path.expanduser(tool_config["base"])


def get_vscode_settings_path(home_dir: str) -> tuple[str, str]:
    """
    Get VS Code settings.json path.

    :param home_dir: User home directory
    :returns: Tuple of (settings_path, settings_dir)
    """
    settings_path = os.path.join(home_dir, *CONFIG["vscode"]["settings-path"])
    return settings_path, os.path.dirname(settings_path)


def ensure_settings_file(settings_path: str, settings_dir: str, logger: logging.Logger) -> None:
    """
    Ensure settings file exists.

    :param settings_path: Path to settings.json
    :param settings_dir: Directory containing settings.json
    :param logger: Logger instance
    """
    os.makedirs(settings_dir, exist_ok=True)
    if not os.path.exists(settings_path) or os.path.getsize(settings_path) == 0:
        with open(settings_path, "w", encoding="utf-8") as f:
            f.write("{}\n")
        logger.info("Initialized settings file: %s", settings_path)


def load_settings(settings_path: str) -> Optional[dict]:
    """
    Load settings from JSON file.

    :param settings_path: Path to settings.json
    :returns: Parsed settings dict or None on error
    """
    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (ValueError, FileNotFoundError) as e:
        print(f"Error loading settings: {e}", file=sys.stderr)
        return None


def write_settings(settings_path: str, settings_dir: str, data: dict, logger: logging.Logger) -> None:
    """
    Write settings to JSON file atomically.

    :param settings_path: Path to settings.json
    :param settings_dir: Directory containing settings.json
    :param data: Settings data to write
    :param logger: Logger instance
    """
    fd, tmp_path = tempfile.mkstemp(prefix="settings.", suffix=".json", dir=settings_dir)
    os.close(fd)
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=True)
        f.write("\n")
    os.replace(tmp_path, settings_path)
    logger.info("Updated settings file: %s", settings_path)


def update_vscode_settings(data: dict, repo_dir: str, logger: logging.Logger) -> bool:
    """
    Update VS Code settings.json with repo paths.

    :param data: Settings data dict
    :param repo_dir: Repository root directory
    :param logger: Logger instance
    :returns: True on success
    """
    keys = CONFIG["vscode"]["settings-keys"]

    instructions_dir = get_source_path(repo_dir, "instructions")
    instructions_locations = data.setdefault(keys["instructions-locations"], {})
    instructions_locations[instructions_dir] = True

    agents_dir = get_source_path(repo_dir, "agents")
    prompts_dir = get_source_path(repo_dir, "prompts")
    prompt_locations = data.setdefault(keys["prompt-locations"], {})
    prompt_locations[agents_dir] = True
    prompt_locations[prompts_dir] = True

    commit_file = get_source_path(repo_dir, "commit")
    entry = {"file": commit_file}
    commit_instructions = data.setdefault(keys["commit-instructions"], [])
    if not any(item.get("file") == commit_file for item in commit_instructions if isinstance(item, dict)):
        commit_instructions.append(entry)

    logger.info("Updated VS Code settings for repo: %s", repo_dir)
    return True


def backup_and_link(dest_path: str, backup_dir: str, source_path: str, logger: logging.Logger) -> None:
    """
    Backup existing file and create symlink.

    :param dest_path: Destination path for symlink
    :param backup_dir: Directory for backups
    :param source_path: Source file to link to
    :param logger: Logger instance
    """
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    if os.path.exists(dest_path) or os.path.islink(dest_path):
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT-%H-%M-%S")
        backup_name = os.path.basename(dest_path).replace(".md", f".{timestamp}.md")
        os.replace(dest_path, os.path.join(backup_dir, backup_name))
        logger.info("Backed up %s", dest_path)
    if os.path.islink(dest_path) or os.path.exists(dest_path):
        os.remove(dest_path)
    os.symlink(source_path, dest_path)
    logger.info("Linked %s -> %s", dest_path, source_path)


def link_intellij_instructions(repo_dir: str, logger: logging.Logger) -> None:
    """
    Link instructions files to IntelliJ Copilot directory.

    :param repo_dir: Repository root directory
    :param logger: Logger instance
    """
    intellij_config = CONFIG["destinations"].get("intellij")
    if not intellij_config or "instructions" not in intellij_config:
        return

    base_dir = get_dest_base(intellij_config)
    backup_dir = os.path.join(base_dir, "backup")
    instructions_map = intellij_config["instructions"]

    for source_key, target_name in instructions_map.items():
        source_path = get_source_path(repo_dir, source_key)
        if not os.path.exists(source_path):
            print(f"Missing source: {source_path}", file=sys.stderr)
            continue
        dest_path = os.path.join(base_dir, target_name)
        backup_and_link(dest_path, backup_dir, source_path, logger)


def get_dest_paths(asset_type: str, targets: set[str]) -> list[str]:
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
        paths.append(base if subdir == "." else os.path.join(base, subdir))
    return paths


def link_assets(
    src_dir: str, asset_type: str, is_directory: bool, logger: logging.Logger, targets: set[str]
) -> None:
    """
    Link assets to destination directories.

    :param src_dir: Source directory containing assets
    :param asset_type: One of 'agents', 'skills', 'prompts'
    :param is_directory: True if assets are directories (skills)
    :param logger: Logger instance
    :param targets: Set of target tool names to include
    """
    if not os.path.isdir(src_dir):
        return
    dest_paths = get_dest_paths(asset_type, targets)
    for name in sorted(os.listdir(src_dir)):
        src_path = os.path.join(src_dir, name)
        if is_directory and not os.path.isdir(src_path):
            continue
        if not is_directory and (not os.path.isfile(src_path) or not name.endswith(".md")):
            continue
        for dest_dir in dest_paths:
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, name)
            if os.path.islink(dest_path) or os.path.exists(dest_path):
                os.remove(dest_path)
            os.symlink(src_path, dest_path)
            logger.info("Linked %s: %s", asset_type[:-1], name)


def cleanup_broken_links(logger: logging.Logger, targets: set[str]) -> None:
    """
    Remove broken symlinks from all destination directories.

    :param logger: Logger instance
    :param targets: Set of target tool names to include
    """
    seen = set()
    for tool_name, tool_config in CONFIG["destinations"].items():
        if tool_name not in targets:
            continue
        base = get_dest_base(tool_config)
        for asset_type in ("agents", "skills", "prompts"):
            subdir = tool_config.get(asset_type)
            if subdir is None:
                continue
            dest_dir = base if subdir == "." else os.path.join(base, subdir)
            if dest_dir in seen or not os.path.isdir(dest_dir):
                continue
            seen.add(dest_dir)
            for name in os.listdir(dest_dir):
                dest_path = os.path.join(dest_dir, name)
                if os.path.islink(dest_path) and not os.path.exists(dest_path):
                    os.remove(dest_path)
                    logger.info("Removed broken link: %s", name)


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
        help=f"Target environments to configure: {', '.join(ALL_TARGETS)} (default: all)",
    )
    args = parser.parse_args()
    if not args.targets:
        args.targets = list(ALL_TARGETS)
    else:
        invalid = set(args.targets) - set(ALL_TARGETS)
        if invalid:
            parser.error(f"invalid target(s): {', '.join(invalid)} (choose from {', '.join(ALL_TARGETS)})")
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
    home_dir = os.path.expanduser("~")

    if "vscode" in targets:
        settings_path, settings_dir = get_vscode_settings_path(home_dir)
        ensure_settings_file(settings_path, settings_dir, logger)
        data = load_settings(settings_path)
        if data is None:
            return 1
        update_vscode_settings(data, repo_dir, logger)
        write_settings(settings_path, settings_dir, data, logger)

    if "intellij" in targets:
        link_intellij_instructions(repo_dir, logger)

    link_assets(get_source_path(repo_dir, "skills"), "skills", is_directory=True, logger=logger, targets=targets)
    link_assets(get_source_path(repo_dir, "prompts"), "prompts", is_directory=False, logger=logger, targets=targets)
    link_assets(get_source_path(repo_dir, "agents"), "agents", is_directory=False, logger=logger, targets=targets)

    cleanup_broken_links(logger, targets)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
