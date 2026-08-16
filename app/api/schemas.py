from pydantic import BaseModel, Field


class TaskCreateRequest(BaseModel):
    id: str = Field(min_length=1)
    goal: str = Field(min_length=1)