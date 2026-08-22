# 🧩 Action model
# This model represents one concrete step inside a larger plan.
# Sebastian turns a high-level objective into a series of actions,
# and each action carries a short description that explains what work is being done.

from pydantic import BaseModel, Field


class Action(BaseModel):
    # 🆔 Unique action identifier.
    id: str

    # 🗺️ The plan this action belongs to.
    plan_id: str

    # 📝 Human-readable action description.
    # It must not be empty so the system can reason about what is happening.
    description: str = Field(min_length=1)