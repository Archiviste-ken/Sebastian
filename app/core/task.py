from enum import Enum

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    PENDING = "pending"


class Task(BaseModel):
    id: str
    goal: str = Field(min_length=1)
    status: TaskStatus = TaskStatus.PENDING