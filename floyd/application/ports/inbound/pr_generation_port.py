"""PR Generation Port - Inbound interface for PR generation use case."""

from abc import ABC, abstractmethod

from floyd.domain.entities.git_context import GitContext
from floyd.domain.entities.pull_request import PullRequest


class PRGenerationPort(ABC):
    """Interface for PR generation use case."""

    @abstractmethod
    def generate_draft(
        self,
        context: GitContext,
        feedback: str | None = None,
    ) -> PullRequest:
        """Generate a PR draft from git context.

        Args:
            context: Git context with branch info, commits, and diff.
            feedback: Optional feedback for refining the draft.

        Returns:
            Generated PullRequest entity.
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

    @abstractmethod
    def validate_can_create_pr(
        self, current_branch: str, target_branch: str
    ) -> None:
        """Validate that a PR can be created.

        Args:
            current_branch: Current working branch.
            target_branch: Target branch for the PR.

        Raises:
            InvalidBranchException: If branches are the same.
            BranchNotFoundException: If target branch doesn't exist.
            PRAlreadyExistsException: If PR already exists.
        """
        ...

    @abstractmethod
    def get_git_context(self, target_branch: str) -> GitContext:
        """Gather git context for PR generation.

        Args:
            target_branch: Target branch for the PR.

        Returns:
            GitContext with all relevant information.
        """
        ...
