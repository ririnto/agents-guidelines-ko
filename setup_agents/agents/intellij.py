import sys
from pathlib import Path

from setup_agents.constants import Asset, Target, get_source_path
from setup_agents.agents.base import AgentSetup


class IntelliJAgentSetup(AgentSetup):
    base = Path.home() / ".config" / "github-copilot" / "intellij"
    env = None
    assets_subdirs = {
        Asset.AGENTS: ".",
        Asset.SKILLS: None,
        Asset.PROMPTS: ".",
        Asset.RULES: None,
    }
    special_copies = None

    instructions_map = {
        "commit": "global-git-commit-instructions.md",
        "copilot": "global-copilot-instructions.md",
    }

    def setup(self, targets: set[Target]) -> None:
        if Target.INTELLIJ not in targets:
            return

        self._copy_instructions()
        self._copy_common_assets(targets)
        self._copy_agents(targets)
        self.cleanup_symlinks()

    def _copy_instructions(self) -> None:
        from setup_agents.utils.file_utils import FileUtils

        if not isinstance(self.instructions_map, dict):
            self.logger.warning("Skipping IntelliJ instructions: instructions config is invalid")
            return

        for source_key, target_name in self.instructions_map.items():
            if not isinstance(target_name, str):
                self.logger.warning("Skipping IntelliJ instruction %s: target must be a string", source_key)
                continue
            source_path = get_source_path(self.repo_dir, source_key)
            if not source_path.exists():
                print(f"Missing source: {source_path}", file=sys.stderr)
                continue
            dest_path = self.base_dir / target_name
            FileUtils.backup_and_copy(dest_path, self.backup_dir, source_path, self.logger)

    def _copy_common_assets(self, targets: set[Target]) -> None:
        for asset_type, is_dir in [(Asset.SKILLS, True), (Asset.PROMPTS, False)]:
            self.copy_assets(get_source_path(self.repo_dir, asset_type.value), asset_type, is_dir)

    def _copy_agents(self, targets: set[Target]) -> None:
        if Target.CLAUDE in targets:
            return

        self.copy_assets(
            get_source_path(self.repo_dir, Asset.AGENTS.value),
            Asset.AGENTS,
            False,
        )
