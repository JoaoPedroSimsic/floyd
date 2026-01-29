"""AI Service Port - Interface for AI providers."""

from abc import ABC, abstractmethod

from floyd.application.dto.ai_config import AIConfig
from floyd.domain.entities.git_context import GitContext
from floyd.domain.entities.pull_request import PullRequest


class AIServicePort(ABC):
    """Interface for AI service providers (Claude, OpenAI, etc.)."""

    @abstractmethod
    def generate_draft(
        self,
        context: GitContext,
        config: AIConfig,
        feedback: str | None = None,
    ) -> PullRequest:
        """Generate a PR draft using AI.

        Args:
            context: Git context with branch info, commits, and diff.
            config: AI configuration.
            feedback: Optional feedback for refining the draft.

        Returns:
            Generated PullRequest entity.

        Raises:
            PRGenerationException: If generation fails.
        """
        ...
