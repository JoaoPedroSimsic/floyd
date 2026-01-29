"""Git Repository Port - Interface for git operations."""

from abc import ABC, abstractmethod


class GitRepositoryPort(ABC):
    """Interface for git repository operations."""

    @abstractmethod
    def is_git_repo(self) -> bool:
        """Check if current directory is a git repository."""
        ...

    @abstractmethod
    def branch_exists(self, branch_name: str) -> bool:
        """Check if a branch exists on remote.

        Args:
            branch_name: Name of the branch to check.

        Returns:
            True if branch exists, False otherwise.
        """
        ...

    @abstractmethod
    def get_current_branch(self) -> str:
        """Get the name of the current branch.

        Returns:
            Name of the current branch.
        """
        ...

    @abstractmethod
    def get_commits(self, base_branch: str) -> str:
        """Get recent commits since diverging from base branch.

        Args:
            base_branch: Base branch to compare against.

        Returns:
            Formatted commit history.
        """
        ...

    @abstractmethod
    def get_diff(self, base_branch: str) -> str:
        """Get diff between current branch and base branch.

        Args:
            base_branch: Base branch to compare against.

        Returns:
            Git diff output.
        """
        ...

    @abstractmethod
    def get_diff_stat(self, base_branch: str) -> str:
        """Get diff statistics (files changed, insertions, deletions).

        Args:
            base_branch: Base branch to compare against.

        Returns:
            Diff statistics output.
        """
        ...
