"""Git CLI Adapter - Implements GitRepositoryPort using git CLI."""

import subprocess

from floyd.application.ports.outbound.git_repository_port import GitRepositoryPort
from floyd.adapters.outbound.utils.terminal import Terminal


class GitCLIAdapter(GitRepositoryPort):
    """Git repository adapter using git CLI."""

    def __init__(self, terminal: Terminal):
        self.terminal = terminal

    def is_git_repo(self) -> bool:
        """Check if current directory is a git repository."""
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0

    def branch_exists(self, branch_name: str) -> bool:
        """Check if a branch exists on remote.

        Args:
            branch_name: Name of the branch to check.

        Returns:
            True if branch exists, False otherwise.
        """
        result = subprocess.run(
            ["git", "ls-remote", "--exit-code", "--heads", "origin", branch_name],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0

    def get_current_branch(self) -> str:
        """Get the name of the current branch.

        Returns:
            Name of the current branch.
        """
        result = self.terminal.run(["git", "branch", "--show-current"])
        return result or ""

    def get_commits(self, base_branch: str) -> str:
        """Get recent commits since diverging from base branch.

        Args:
            base_branch: Base branch to compare against.

        Returns:
            Formatted commit history.
        """
        result = self.terminal.run(
            ["git", "log", f"{base_branch}..HEAD", "--oneline"]
        )
        return result or ""

    def get_diff(self, base_branch: str) -> str:
        """Get diff between current branch and base branch.

        Args:
            base_branch: Base branch to compare against.

        Returns:
            Git diff output.
        """
        result = self.terminal.run(
            [
                "git",
                "diff",
                "--merge-base",
                base_branch,
                ":!*.lock",
                ":!*-lock.json",
            ]
        )
        return result or ""

    def get_diff_stat(self, base_branch: str) -> str:
        """Get diff statistics (files changed, insertions, deletions).

        Args:
            base_branch: Base branch to compare against.

        Returns:
            Diff statistics output.
        """
        result = self.terminal.run(
            [
                "git",
                "diff",
                "--stat",
                "--merge-base",
                base_branch,
                ":!*.lock",
                ":!*-lock.json",
            ]
        )
        return result or ""
