import argparse
from pathlib import Path

from setup_agents.constants import Target
from setup_agents.agents.claude import ClaudeAgentSetup
from setup_agents.agents.codex import CodexAgentSetup
from setup_agents.agents.intellij import IntelliJAgentSetup
from setup_agents.utils.logger import setup_logger
from setup_agents.agents.vscode import VSCodeAgentSetup


def get_repo_dir() -> Path:
    return Path(__file__).parent.parent.resolve()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Setup agent configurations for various tools.")
    parser.add_argument(
        "targets",
        nargs="*",
        metavar="TARGET",
        help=f"Target environments to configure: {', '.join(target.value for target in Target)} (default: all)",
    )
    args = parser.parse_args()

    # Validate choices manually to allow empty list
    valid_targets = [target.value for target in Target]
    for t in args.targets:
        if t not in valid_targets:
            parser.error(f"argument TARGET: invalid choice: '{t}' (choose from {', '.join(valid_targets)})")

    if not args.targets:
        args.targets = valid_targets
    return args


def main() -> int:
    args = parse_args()
    targets: set[Target] = {Target(target) for target in args.targets}

    logger = setup_logger()
    repo_dir = get_repo_dir()

    agents = [
        VSCodeAgentSetup(repo_dir, logger),
        CodexAgentSetup(repo_dir, logger),
        ClaudeAgentSetup(repo_dir, logger),
        IntelliJAgentSetup(repo_dir, logger),
    ]

    for agent in agents:
        agent.setup(targets)

    return 0
