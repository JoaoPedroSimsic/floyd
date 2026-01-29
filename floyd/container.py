"""Dependency injection container - Composition root."""

from dataclasses import dataclass

from floyd.adapters.outbound.ai.claude_adapter import ClaudeAdapter
from floyd.adapters.outbound.config.toml_config_adapter import TomlConfigAdapter
from floyd.adapters.outbound.git.git_cli_adapter import GitCLIAdapter
from floyd.adapters.outbound.github.github_cli_adapter import GitHubCLIAdapter
from floyd.application.ports.outbound.ai_service_port import AIServicePort
from floyd.application.ports.outbound.config_port import ConfigPort
from floyd.application.ports.outbound.git_repository_port import GitRepositoryPort
from floyd.application.ports.outbound.pr_repository_port import PRRepositoryPort
from floyd.application.services.pr_generation_service import PRGenerationService


@dataclass
class Container:
    """Dependency injection container holding all wired dependencies."""

    ai_service: AIServicePort
    git_repository: GitRepositoryPort
    pr_repository: PRRepositoryPort
    config: ConfigPort
    pr_generation_service: PRGenerationService


def create_container() -> Container:
    """Create and wire all dependencies.

    Returns:
        Container with all dependencies wired.
    """
    ai_service = ClaudeAdapter()
    git_repository = GitCLIAdapter()
    pr_repository = GitHubCLIAdapter()
    config = TomlConfigAdapter()

    pr_generation_service = PRGenerationService(
        ai_service=ai_service,
        git_repository=git_repository,
        pr_repository=pr_repository,
        config=config,
    )

    return Container(
        ai_service=ai_service,
        git_repository=git_repository,
        pr_repository=pr_repository,
        config=config,
        pr_generation_service=pr_generation_service,
    )
