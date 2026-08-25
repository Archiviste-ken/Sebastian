# 🧩 Action model
# This model represents one concrete step inside a larger plan.
# Sebastian turns a high-level objective into a series of actions,
# and each action carries a short description that explains what work is being done.

# 📦 Import BaseModel and Field from pydantic for data validation and schema generation
from pydantic import BaseModel, Field


# 🎯 Define the Action class, inheriting from BaseModel
class Action(BaseModel):
    # 🆔 Unique action identifier.
    # 📝 Represents the id of the action
    id: str

    # 🗺️ The plan this action belongs to.
    # 🏷️ Identifier for the associated plan
    plan_id: str

    # 📝 Human-readable action description.
    # It must not be empty so the system can reason about what is happening.
    # 🔧 Define a field with a minimum length constraint
    description: str = Field(min_length=1)