"""Git Context entity."""

from pydantic import BaseModel, Field

from floyd.domain.value_objects.branch import Branch


class GitContext(BaseModel):
    """Represents the git context for PR generation."""

    current_branch: Branch
    target_branch: Branch
    commits: str = Field(default="")
    diff: str = Field(default="")
    diff_stat: str = Field(default="")

    def has_changes(self) -> bool:
        """Check if there are any changes to create a PR for."""
        return bool(self.diff.strip())
