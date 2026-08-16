from pydantic import BaseModel, Field


class Plan(BaseModel):
    id: str
    task_id: str
    description: str = Field(min_length=1)