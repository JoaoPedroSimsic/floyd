"""Claude AI Adapter - Implements AIServicePort using Claude CLI."""

import subprocess

from floyd.application.dto.ai_config import AIConfig
from floyd.application.ports.outbound.ai_service_port import AIServicePort
from floyd.domain.entities.git_context import GitContext
from floyd.domain.entities.pull_request import PullRequest
from floyd.domain.exceptions.pr.pr_generation_exception import PRGenerationException


class ClaudeAdapter(AIServicePort):
    """AI service adapter using Claude CLI."""

    def _run_command(self, command: list[str]) -> str | None:
        """Execute a command and return output.

        Args:
            command: Command and arguments to execute.

        Returns:
            Command output or None if failed.
        """
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    def _build_prompt(
        self,
        context: GitContext,
        config: AIConfig,
        feedback: str | None = None,
    ) -> str:
        """Build the prompt for Claude.

        Args:
            context: Git context with branch info, commits, and diff.
            config: AI configuration.
            feedback: Optional feedback for refining the draft.

        Returns:
            Formatted prompt string.
        """
        diff = context.diff

        if config.diff_limit > 0 and len(diff) > config.diff_limit:
            diff = (
                diff[: config.diff_limit]
                + "\n\n[... DIFF TRUNCATED FOR TOKEN LIMITS ...]"
            )

        extra_prompt = ""
        if config.instructions:
            extra_prompt = f"\nUSER-SPECIFIC INSTRUCTIONS:\n{config.instructions}\n"

        feedback_section = ""
        if feedback:
            feedback_section = f"\nUSER FEEDBACK FOR REFINEMENT:\n{feedback}\n"

        prompt = (
            f"Context:\n"
            f"- Working on branch: {context.current_branch.name}\n"
            f"- Target branch: {context.target_branch.name}\n"
            f"- Recent commits:\n{context.commits}\n\n"
            f"- File Change Summary:\n{context.diff_stat}\n\n"
            f"Task: Review the git diff below and write a PR title and description. "
            f"TITLE CONVENTION: Use conventional commits for the title "
            f"(e.g., feat: [title], fix: [title], docs: [title]).\n\n"
            f"Use the commit history to understand the intent behind the changes.\n\n"
            f"{extra_prompt}"
            f"{feedback_section}"
            f"IMPORTANT: Do not include any signatures, footers, or mentions of "
            f"being 'Generated with Claude Code' or any other tool.\n\n"
            f"Format your response exactly like this:\n"
            f"TITLE: [Your Title]\n"
            f"BODY: [Your Description]\n\n"
            f"Diff:\n{diff}"
        )

        return prompt

    def _parse_response(self, response: str) -> PullRequest:
        """Parse Claude's response into a PullRequest.

        Args:
            response: Raw response from Claude.

        Returns:
            PullRequest entity.

        Raises:
            PRGenerationException: If parsing fails.
        """
        try:
            title = response.split("TITLE:")[1].split("BODY:")[0].strip()
            body = response.split("BODY:")[1].strip()

            if not title or not body:
                raise PRGenerationException("AI response missing title or body")

            return PullRequest(title=title, body=body)

        except (IndexError, AttributeError) as e:
            raise PRGenerationException(f"Failed to parse AI response: {e}") from e

    def generate_draft(
        self,
        context: GitContext,
        config: AIConfig,
        feedback: str | None = None,
    ) -> PullRequest:
        """Generate a PR draft using Claude.

        Args:
            context: Git context with branch info, commits, and diff.
            config: AI configuration.
            feedback: Optional feedback for refining the draft.

        Returns:
            Generated PullRequest entity.

        Raises:
            PRGenerationException: If generation fails.
        """
        prompt = self._build_prompt(context, config, feedback)

        response = self._run_command(["claude", "-p", prompt])

        if response is None:
            raise PRGenerationException("Failed to get response from Claude CLI")

        return self._parse_response(response)
