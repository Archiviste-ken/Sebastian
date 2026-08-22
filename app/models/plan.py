# 🗺️ Plan model
# A plan is the structured strategy Sebastian follows to accomplish a task.
# It turns a general goal into an ordered set of actions or intentions.

from pydantic import BaseModel, Field


class Plan(BaseModel):
    # 🆔 Unique plan identifier.
    id: str

    # 🧵 Task this plan belongs to.
    task_id: str

    # 📝 Short summary of the plan's purpose.
    description: str = Field(min_length=1)