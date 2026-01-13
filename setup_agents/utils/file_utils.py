import datetime
import os
import shutil
from pathlib import Path

import logging

from setup_agents.constants import Asset


class FileUtils:
    @staticmethod
    def get_dest_base(tool_config: dict) -> Path:
        env_var = tool_config.get("env")
        if env_var and os.environ.get(env_var):
            return Path(os.environ[env_var])
        return tool_config["base"]

    @staticmethod
    def backup_and_copy(
        dest_path: Path,
        backup_dir: Path,
        source_path: Path,
        logger: logging.Logger,
    ) -> None:
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

    @staticmethod
    def get_dest_paths(asset_type: Asset, tool_config: dict) -> list[Path]:
        paths = []
        subdir = tool_config.get(asset_type.value)
        if subdir is None:
            return paths
        base = FileUtils.get_dest_base(tool_config)
        paths.append(base if subdir == "." else base / subdir)
        return paths

    @staticmethod
    def cleanup_old_symlinks(
        tool_config: dict,
        logger: logging.Logger,
    ) -> None:
        base = FileUtils.get_dest_base(tool_config)
        for asset_type in Asset:
            subdir = tool_config.get(asset_type.value)
            if subdir is None:
                continue
            dest_dir = base if subdir == "." else base / subdir
            if not dest_dir.is_dir():
                continue
            for dest_path in dest_dir.iterdir():
                if dest_path.is_symlink():
                    dest_path.unlink()
                    logger.info("Removed old symlink: %s", dest_path.name)
