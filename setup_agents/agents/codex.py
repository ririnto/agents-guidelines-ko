from pathlib import Path

from setup_agents.constants import Asset, Target, SPECIAL_INSTRUCTION_COPIES
from setup_agents.agents.base import AgentSetup


class CodexAgentSetup(AgentSetup):
    base = Path.home() / ".codex"
    env = "CODEX_HOME"
    assets_subdirs = {
        Asset.SKILLS: "skills",
    }
    special_copies = SPECIAL_INSTRUCTION_COPIES.get("codex")

    def setup(self, targets: set[Target]) -> None:
        if Target.CODEX not in targets:
            return

        self._copy_common_assets(targets)
        if self.special_copies:
            self.copy_special_files(self.special_copies)
        self.cleanup_symlinks()

    def _copy_common_assets(self, targets: set[Target]) -> None:
        from setup_agents.constants import get_source_path

        for asset_type, is_dir in [(Asset.SKILLS, True)]:
            self.copy_assets(get_source_path(self.repo_dir, asset_type.value), asset_type, is_dir)
