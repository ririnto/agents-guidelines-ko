from pathlib import Path


from setup_agents.constants import Asset, Target, SPECIAL_INSTRUCTION_COPIES
from setup_agents.agents.base import AgentSetup


class ClaudeAgentSetup(AgentSetup):
    base = Path.home() / ".claude"
    env = None
    assets_subdirs = {
        Asset.AGENTS: "agents",
        Asset.SKILLS: "skills",
        Asset.PROMPTS: "commands",
        Asset.RULES: "rules",
    }
    special_copies = SPECIAL_INSTRUCTION_COPIES.get("claude")

    def setup(self, targets: set[Target]) -> None:
        if Target.CLAUDE not in targets:
            return

        self._copy_common_assets(targets)
        self._copy_agents()
        self._copy_rules()
        if self.special_copies:
            self.copy_special_files(self.special_copies)
        self.cleanup_symlinks()

    def _copy_common_assets(self, targets: set[Target]) -> None:
        from setup_agents.constants import get_source_path

        for asset_type, is_dir in [(Asset.SKILLS, True), (Asset.PROMPTS, False)]:
            self.copy_assets(get_source_path(self.repo_dir, asset_type.value), asset_type, is_dir)

    def _copy_agents(self) -> None:
        from setup_agents.constants import get_source_path

        self.copy_assets(
            get_source_path(self.repo_dir, "claude_agents"),
            Asset.AGENTS,
            False,
        )

    def _copy_rules(self) -> None:
        from setup_agents.constants import get_source_path

        self.copy_assets(
            get_source_path(self.repo_dir, "claude_rules"),
            Asset.RULES,
            False,
        )
