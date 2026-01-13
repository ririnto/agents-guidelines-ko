import os
import shutil
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

import logging

from setup_agents.constants import Asset, Target, get_source_path


class AgentSetup(ABC):
    base: Path
    env: Optional[str]
    assets_subdirs: dict
    special_copies: Optional[list[dict]]

    def __init__(self, repo_dir: Path, logger: logging.Logger):
        self.repo_dir = repo_dir
        self.logger = logger
        self.base_dir = self._get_base_dir()
        self.backup_dir = self.base_dir / "backup"

    def _get_base_dir(self) -> Path:
        if self.env and self.env in os.environ:
            return Path(os.environ[self.env])
        return self.base

    @abstractmethod
    def setup(self, targets: set[Target]) -> None:
        pass

    def copy_assets(self, src_dir: Path, asset_type: Asset, is_directory: bool) -> None:
        from setup_agents.utils.file_utils import FileUtils

        if not src_dir.is_dir():
            return
        dest_paths = FileUtils.get_dest_paths(asset_type, self.get_tool_config())
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
                self.logger.info("Copied %s: %s", asset_type, src_path.name)

    def copy_special_files(self, copies: list[dict]) -> None:
        from setup_agents.utils.file_utils import FileUtils

        for entry in copies:
            source_key = entry.get("source")
            filename = entry.get("filename")
            if not isinstance(source_key, str) or not isinstance(filename, str):
                continue
            source_path = get_source_path(self.repo_dir, source_key)
            if not source_path.exists():
                print(f"Missing source: {source_path}", file=sys.stderr)
                continue
            dest_path = self.base_dir / filename
            FileUtils.backup_and_copy(dest_path, self.backup_dir, source_path, self.logger)

    def cleanup_symlinks(self) -> None:
        from setup_agents.utils.file_utils import FileUtils

        FileUtils.cleanup_old_symlinks(self.get_tool_config(), self.logger)

    def get_tool_config(self) -> dict:
        return {
            "base": self.base,
            "env": self.env,
            **self.assets_subdirs,
        }
