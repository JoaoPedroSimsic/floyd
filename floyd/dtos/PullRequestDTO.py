from pydantic import BaseModel


class PullRequestDTO(BaseModel):
    title: str
    body: str
