from pydantic import BaseModel, Field


class Action(BaseModel):
    id: str
    plan_id: str
    description: str = Field(min_length=1)