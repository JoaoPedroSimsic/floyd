"""Branch value object."""

from pydantic import BaseModel, field_validator


class Branch(BaseModel):
    """Represents a git branch with validation."""

    name: str

    model_config = {"frozen": True}

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate branch name is not empty and has valid format."""
        if not v or not v.strip():
            raise ValueError("Branch name cannot be empty")
        v = v.strip()
        if v.startswith("-"):
            raise ValueError("Branch name cannot start with '-'")
        if ".." in v:
            raise ValueError("Branch name cannot contain '..'")
        if v.endswith(".lock"):
            raise ValueError("Branch name cannot end with '.lock'")
        return v

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Branch):
            return self.name == other.name
        if isinstance(other, str):
            return self.name == other
        return False

    def __hash__(self) -> int:
        return hash(self.name)
