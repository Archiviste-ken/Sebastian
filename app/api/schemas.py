# 📡 API request schemas
# 📡 These models define what a client is allowed to send when creating a task.

from pydantic import BaseModel, Field  # 📦 Import BaseModel and Field for schema definition and validation


class TaskCreateRequest(BaseModel):  # 📝 Define the TaskCreateRequest schema inheriting from BaseModel
    # 🆔 Task identifier submitted by the client.
    id: str = Field(min_length=1)  # 📝 Define the 'id' field as a string with a minimum length of 1

    # 🎯 Human-readable goal that describes the desired outcome.
    goal: str = Field(min_length=1)  # 📝 Define the 'goal' field as a string with a minimum length of 1