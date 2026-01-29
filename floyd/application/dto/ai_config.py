"""AI Configuration DTO."""

from pydantic import BaseModel, Field


class AIConfig(BaseModel):
    """Configuration for AI service."""

    provider: str = Field(
        default="claude",
        description="The AI provider to use (e.g., 'claude', 'gemini', 'copilot')."
    )

    diff_limit: int = Field(
        default=-1,
        description="Maximum characters for diff. -1 means no limit.",
    )

    instructions: str = Field(
        default="",
        description="Custom instructions for PR generation.",
    )
