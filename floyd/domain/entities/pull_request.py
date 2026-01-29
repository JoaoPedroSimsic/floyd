"""Pull Request entity."""

from pydantic import BaseModel, Field, field_validator


class PullRequest(BaseModel):
    """Represents a pull request with title and body."""

    title: str = Field(..., min_length=1, max_length=256)
    body: str = Field(default="")

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate and clean title."""
        v = v.strip()
        if not v:
            raise ValueError("Title cannot be empty")
        return v

    @field_validator("body")
    @classmethod
    def validate_body(cls, v: str) -> str:
        """Clean body content."""
        return v.strip()
