"""PR Repository Port - Interface for PR operations."""

from abc import ABC, abstractmethod

from floyd.domain.entities.pull_request import PullRequest


class PRRepositoryPort(ABC):
    """Interface for pull request repository operations (GitHub, GitLab, etc.)."""

    @abstractmethod
    def pr_exists(self, head_branch: str, base_branch: str) -> bool:
        """Check if a PR already exists.

        Args:
            head_branch: Source branch of the PR.
            base_branch: Target branch of the PR.

        Returns:
            True if PR exists, False otherwise.
        """
        ...

    @abstractmethod
    def create_pr(self, pr: PullRequest, base_branch: str) -> str:
        """Create a pull request.

        Args:
            pr: PullRequest entity with title and body.
            base_branch: Target branch for the PR.

        Returns:
            URL of the created PR.
        """
        ...
