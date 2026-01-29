"""Config Port - Interface for configuration loading."""

from abc import ABC, abstractmethod

from floyd.application.dto.ai_config import AIConfig


class ConfigPort(ABC):
    """Interface for configuration loading."""

    @abstractmethod
    def get_ai_config(self) -> AIConfig:
        """Load AI configuration.

        Returns:
            AIConfig with settings for AI service.
        """
        ...
