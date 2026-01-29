from pydantic import BaseModel


class GitContextDTO(BaseModel):
    branch_name: str
    target_branch: str
    commits: str
    diff: str
    diff_stat: str
