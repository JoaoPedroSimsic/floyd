"""GitHub CLI Adapter - Implements PRRepositoryPort using gh CLI."""

import subprocess

from floyd.application.ports.outbound.pr_repository_port import PRRepositoryPort
from floyd.domain.entities.pull_request import PullRequest


class GitHubCLIAdapter(PRRepositoryPort):
    """PR repository adapter using GitHub CLI (gh)."""

    def _run_command(self, command: list[str]) -> str | None:
        """Execute a command and return output.

        Args:
            command: Command and arguments to execute.

        Returns:
            Command output or None if failed.
        """
        try:
            result = subprocess.run(
                command, capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    def pr_exists(self, head_branch: str, base_branch: str) -> bool:
        """Check if a PR already exists.

        Args:
            head_branch: Source branch of the PR.
            base_branch: Target branch of the PR.

        Returns:
            True if PR exists, False otherwise.
        """
        result = self._run_command(
            [
                "gh",
                "pr",
                "list",
                "--head",
                head_branch,
                "--base",
                base_branch,
                "--state",
                "open",
                "--json",
                "number",
                "--jq",
                ".[0].number",
            ]
        )
        return bool(result)

    def create_pr(self, pr: PullRequest, base_branch: str) -> str:
        """Create a pull request.

        Args:
            pr: PullRequest entity with title and body.
            base_branch: Target branch for the PR.

        Returns:
            URL of the created PR.
        """
        result = self._run_command(
            [
                "gh",
                "pr",
                "create",
                "--title",
                pr.title,
                "--body",
                pr.body,
                "--base",
                base_branch,
            ]
        )
        return result or ""
