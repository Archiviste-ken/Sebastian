# 🗺️ Plan model
# 📝 A plan is the structured strategy Sebastian follows to accomplish a task.
# 🎯 It turns a general goal into an ordered set of actions or intentions.

# 📦 Import BaseModel and Field from pydantic for data validation and schema definition.
from pydantic import BaseModel, Field


# 🏷️ Define the Plan class, inheriting from BaseModel to create a Pydantic model.
class Plan(BaseModel):
    # 🆔 Unique plan identifier.
    # 📝 Represents the string ID of the plan.
    id: str

    # 🧵 Task this plan belongs to.
    # 🏷️ Links the plan to a specific task ID.
    task_id: str

    # 📝 Short summary of the plan's purpose.
    # 🔧 Uses Field to enforce a minimum length of 1 character for the description.
    description: str = Field(min_length=1)