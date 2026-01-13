import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Optional

import logging

SETTINGS_KEYS = {
    "commit-message-generation-instructions": "github.copilot.chat.commitMessageGeneration.instructions",
    "instructions-files-locations": "chat.instructionsFilesLocations",
}


class VSCodeSettings:
    def __init__(
        self,
        settings_path: Path,
        settings_dir: Path,
        repo_dir: Path,
        logger: logging.Logger,
    ):
        self.settings_path = settings_path
        self.settings_dir = settings_dir
        self.repo_dir = repo_dir
        self.logger = logger

    @staticmethod
    def get_path(repo_dir: Path) -> tuple[Path, Path]:
        from ..agents.vscode import VSCodeAgentSetup
        from .file_utils import FileUtils

        base_dir = FileUtils.get_dest_base(
            {
                "base": VSCodeAgentSetup.base,
                "env": VSCodeAgentSetup.env,
            }
        )
        settings_path = base_dir / "settings.json"
        return settings_path, base_dir

    def ensure(self) -> None:
        self.settings_dir.mkdir(parents=True, exist_ok=True)
        if not self.settings_path.exists() or self.settings_path.stat().st_size == 0:
            self.settings_path.write_text("{}\n", encoding="utf-8")
            self.logger.info("Initialized settings file: %s", self.settings_path)

    def load(self) -> Optional[dict]:
        try:
            return json.loads(self.settings_path.read_text(encoding="utf-8"))
        except (ValueError, FileNotFoundError) as e:
            print(f"Error loading settings: {e}", file=sys.stderr)
            return None

    def write(self, data: dict) -> None:
        fd, tmp_path = tempfile.mkstemp(prefix="settings.", suffix=".json", dir=self.settings_dir)
        os.close(fd)
        tmp_file = Path(tmp_path)
        tmp_file.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
        tmp_file.replace(self.settings_path)
        self.logger.info("Updated settings file: %s", self.settings_path)

    def update(self, data: dict) -> bool:
        from setup_agents.constants import get_source_path

        instructions_dir = str(get_source_path(self.repo_dir, "instructions"))
        instructions_locations = data.setdefault(SETTINGS_KEYS["instructions-files-locations"], {})
        instructions_locations[instructions_dir] = True

        commit_file = str(get_source_path(self.repo_dir, "commit"))
        entry = {"file": commit_file}
        commit_instructions = data.setdefault(SETTINGS_KEYS["commit-message-generation-instructions"], [])
        if not any(item.get("file") == commit_file for item in commit_instructions if isinstance(item, dict)):
            commit_instructions.append(entry)

        self.logger.info("Updated VS Code settings for repo: %s", self.repo_dir)
        return True
