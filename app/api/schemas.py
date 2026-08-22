# 📡 API request schemas
# These models define what a client is allowed to send when creating a task.

from pydantic import BaseModel, Field


class TaskCreateRequest(BaseModel):
    # 🆔 Task identifier submitted by the client.
    id: str = Field(min_length=1)

    # 🎯 Human-readable goal that describes the desired outcome.
    goal: str = Field(min_length=1)