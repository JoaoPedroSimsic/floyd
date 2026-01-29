from pydantic import BaseModel, Field


class AIConfigDTO(BaseModel):
    diff_limit: int = Field(default=-1)
    instructions: str = Field(default="")
