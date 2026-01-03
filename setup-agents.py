#!/usr/bin/env python3
import datetime
import json
import logging
import os
import sys
import tempfile

CONFIG = {
    "settings-keys": {
        "instructions-locations": "chat.instructionsFilesLocations",
        "prompt-locations": "chat.promptFilesLocations",
        "commit-instructions": "github.copilot.chat.commitMessageGeneration.instructions",
    },
    "filenames": {
        "copilot-source": "global-copilot.instructions.md",
        "copilot-target": "global-copilot-instructions.md",
        "commit": "global-git-commit-instructions.md",
    },
    "settings-rel-path": [
        "Library",
        "Application Support",
        "Code",
        "User",
        "settings.json",
    ],
    "copilot-rel-dir": [".config", "github-copilot", "intellij"],
    "skills-dest-bases": ("~/.claude/skills", "~/.codex/skills"),
    "prompts-dest-bases": (
        "~/.claude/commands",
        "~/.codex/prompts",
        "~/.config/github-copilot/intellij",
    ),
}


def setup_logger() -> logging.Logger:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    return logging.getLogger(__name__)


def get_repo_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def build_settings_paths(home_dir: str) -> tuple[str, str, str]:
    settings_path = os.path.join(home_dir, *CONFIG["settings-rel-path"])
    settings_dir = os.path.dirname(settings_path)
    target_dir = os.path.join(home_dir, *CONFIG["copilot-rel-dir"])
    return settings_path, settings_dir, target_dir


def build_repo_paths(repo_dir: str) -> tuple[str, str, str]:
    source_copilot = os.path.join(repo_dir, CONFIG["filenames"]["copilot-source"])
    source_commit = os.path.join(repo_dir, CONFIG["filenames"]["commit"])
    skills_src_dir = os.path.join(repo_dir, "skills")
    return source_copilot, source_commit, skills_src_dir


def build_target_paths(target_dir: str) -> tuple[str, str]:
    target_copilot = os.path.join(target_dir, CONFIG["filenames"]["copilot-target"])
    target_commit = os.path.join(target_dir, CONFIG["filenames"]["commit"])
    return target_copilot, target_commit


def ensure_settings_file(
    settings_path: str,
    settings_dir: str,
    logger: logging.Logger,
) -> None:
    os.makedirs(settings_dir, exist_ok=True)
    logger.info("Ensured settings directory: %s", settings_dir)
    if not os.path.exists(settings_path) or os.path.getsize(settings_path) == 0:
        with open(settings_path, "w", encoding="utf-8") as f:
            f.write("{}\n")
        logger.info("Initialized settings file: %s", settings_path)


def load_settings(settings_path: str) -> dict | None:
    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except ValueError as e:
        print(f"Invalid JSON in settings file: {e}", file=sys.stderr)
        return None
    if not isinstance(data, dict):
        print("Settings JSON must be an object at the top level.", file=sys.stderr)
        return None
    return data


def ensure_location_entries(data: dict, key: str, paths: list[str]) -> bool:
    existing = data.get(key)
    if existing is None:
        existing = {}
        data[key] = existing
    if not isinstance(existing, dict):
        print(f'Expected "{key}" to be an object.', file=sys.stderr)
        return False
    for path in paths:
        existing[path] = True
    return True


def ensure_instructions_list(data: dict, commit_file: str) -> bool:
    key = CONFIG["settings-keys"]["commit-instructions"]
    existing = data.get(key)
    entry = {"file": commit_file}
    if existing is None:
        data[key] = [entry]
        return True
    if not isinstance(existing, list):
        print(f'Expected "{key}" to be an array.', file=sys.stderr)
        return False
    for item in existing:
        if isinstance(item, dict) and item.get("file") == commit_file:
            return True
    existing.append(entry)
    return True


def update_settings_data(
    data: dict,
    target_dir: str,
    repo_dir: str,
    commit_source: str,
) -> bool:
    instructions_key = CONFIG["settings-keys"]["instructions-locations"]
    prompt_key = CONFIG["settings-keys"]["prompt-locations"]
    prompts_dir = os.path.join(repo_dir, "prompts")
    if not ensure_location_entries(data, instructions_key, [target_dir, repo_dir]):
        return False
    if not ensure_location_entries(data, prompt_key, [prompts_dir]):
        return False
    if not ensure_instructions_list(data, commit_source):
        return False
    return True


def write_settings(
    settings_path: str,
    settings_dir: str,
    data: dict,
    logger: logging.Logger,
) -> None:
    fd, tmp_path = tempfile.mkstemp(
        prefix="settings.",
        suffix=".json",
        dir=settings_dir,
    )
    os.close(fd)
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=True)
        f.write("\n")
    os.replace(tmp_path, settings_path)
    logger.info("Updated settings file: %s", settings_path)


def validate_sources(paths: list[str]) -> bool:
    missing = [path for path in paths if not os.path.exists(path)]
    if missing:
        for path in missing:
            print(f"Missing source file: {path}", file=sys.stderr)
        return False
    return True


def backup_and_link(
    dest_path: str,
    backup_dir: str,
    source_path: str,
    logger: logging.Logger,
) -> None:
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    if os.path.exists(dest_path) or os.path.islink(dest_path):
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT-%H-%M-%S")
        backup_path = os.path.join(
            backup_dir,
            os.path.basename(dest_path).replace(".md", f".{timestamp}.md"),
        )
        os.replace(dest_path, backup_path)
        logger.info("Backed up %s to %s", dest_path, backup_path)
    if os.path.islink(dest_path) or os.path.exists(dest_path):
        os.remove(dest_path)
    os.symlink(source_path, dest_path)
    logger.info("Linked %s to %s", dest_path, source_path)


def link_skills(
    skills_src_dir: str,
    dest_bases: tuple[str, str],
    logger: logging.Logger,
) -> None:
    if not os.path.isdir(skills_src_dir):
        return
    for name in sorted(os.listdir(skills_src_dir)):
        src_path = os.path.join(skills_src_dir, name)
        if not os.path.isdir(src_path):
            continue
        for base in dest_bases:
            dest_dir = os.path.expanduser(base)
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, name)
            if os.path.islink(dest_path) or os.path.exists(dest_path):
                os.remove(dest_path)
            os.symlink(src_path, dest_path)
            logger.info("Linked skill %s to %s", src_path, dest_path)


def link_prompts(
    prompts_src_dir: str,
    dest_bases: tuple[str, ...],
    logger: logging.Logger,
) -> None:
    if not os.path.isdir(prompts_src_dir):
        return
    for name in sorted(os.listdir(prompts_src_dir)):
        src_path = os.path.join(prompts_src_dir, name)
        if not os.path.isfile(src_path) or not name.endswith(".md"):
            continue
        for base in dest_bases:
            dest_dir = os.path.expanduser(base)
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, name)
            if os.path.islink(dest_path) or os.path.exists(dest_path):
                os.remove(dest_path)
            os.symlink(src_path, dest_path)
            logger.info("Linked prompt %s to %s", src_path, dest_path)


def cleanup_broken_links(
    dest_bases: tuple[str, ...],
    logger: logging.Logger,
) -> None:
    for base in dest_bases:
        dest_dir = os.path.expanduser(base)
        if not os.path.isdir(dest_dir):
            continue
        for name in os.listdir(dest_dir):
            dest_path = os.path.join(dest_dir, name)
            if os.path.islink(dest_path) and not os.path.exists(dest_path):
                os.remove(dest_path)
                logger.info("Removed broken link %s", dest_path)


def main() -> int:
    logger = setup_logger()
    repo_dir = get_repo_dir()
    source_copilot, source_commit, skills_src_dir = build_repo_paths(repo_dir)
    home_dir = os.path.expanduser("~")
    settings_path, settings_dir, target_dir = build_settings_paths(home_dir)
    target_copilot, target_commit = build_target_paths(target_dir)

    ensure_settings_file(settings_path, settings_dir, logger)
    data = load_settings(settings_path)
    if data is None:
        return 1

    if not update_settings_data(data, target_dir, repo_dir, source_commit):
        return 1
    logger.info("Merged settings for %s", target_dir)

    write_settings(settings_path, settings_dir, data, logger)

    if not validate_sources([source_copilot, source_commit]):
        return 1

    backup_and_link(
        target_copilot,
        os.path.join(target_dir, "backup"),
        source_copilot,
        logger,
    )
    backup_and_link(
        target_commit,
        os.path.join(target_dir, "backup"),
        source_commit,
        logger,
    )

    skills_dest_bases = CONFIG["skills-dest-bases"]
    prompts_dest_bases = CONFIG["prompts-dest-bases"]
    prompts_src_dir = os.path.join(repo_dir, "prompts")

    link_skills(skills_src_dir, skills_dest_bases, logger)
    link_prompts(prompts_src_dir, prompts_dest_bases, logger)
    cleanup_broken_links(skills_dest_bases + prompts_dest_bases, logger)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
