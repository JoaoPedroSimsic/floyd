"""Claude AI Adapter - Implements AIServicePort using Claude CLI."""

from floyd.adapters.outbound.ai.ai_adapter import AIAdapter
from floyd.application.dto.ai_config import AIConfig
from floyd.domain.entities.git_context import GitContext
from floyd.domain.entities.pull_request import PullRequest


class ClaudeAdapter(AIAdapter):
    """AI service adapter using Claude CLI."""

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

        command = ["claude"]

        if config.model:
            command.extend(["-m", config.model])

        command.extend(["-p", prompt])

        response = self.terminal.run(command, error_msg="Claude Code error")

        return self._parse_response(response)
