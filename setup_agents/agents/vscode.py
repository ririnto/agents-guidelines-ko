from pathlib import Path

from setup_agents.constants import Asset, Target, get_source_path
from setup_agents.agents.base import AgentSetup
from setup_agents.utils.vscode_settings import VSCodeSettings


class VSCodeAgentSetup(AgentSetup):
    base = Path.home() / "Library" / "Application Support" / "Code" / "User"
    env = "VSCODE_USER_DATA"
    assets_subdirs = {
        Asset.SKILLS: None,
    }
    special_copies = None

    def _get_settings_path(self) -> tuple[Path, Path]:
        return VSCodeSettings.get_path(self.repo_dir)

    def setup(self, targets: set[Target]) -> None:
        if Target.VSCODE not in targets:
            return

        settings_path, settings_dir = self._get_settings_path()
        settings = VSCodeSettings(settings_path, settings_dir, self.repo_dir, self.logger)
        settings.ensure()
        data = settings.load()
        if data is None:
            return
        settings.update(data)
        settings.write(data)

        self._copy_common_assets(targets)
        self.cleanup_symlinks()

    def _copy_common_assets(self, targets: set[Target]) -> None:
        for asset_type, is_dir in [(Asset.SKILLS, True)]:
            self.copy_assets(get_source_path(self.repo_dir, asset_type.value), asset_type, is_dir)
