# 📦 Import Enum base class from enum module
from enum import Enum
# 🈳 Blank line

# 📦 Import BaseModel and Field from pydantic module
from pydantic import BaseModel, Field
# 🈳 Blank line
# 🈳 Blank line

# 🧩 Define ActionRisk enumeration for action risk levels
class ActionRisk(str, Enum):
    # 🧩 Define LOW risk level string constant
    LOW = "low"
    # 🧩 Define MEDIUM risk level string constant
    MEDIUM = "medium"
    # 🧩 Define HIGH risk level string constant
    HIGH = "high"
# 🈳 Blank line
# 🈳 Blank line

# 🧩 Define RetryPolicy enumeration for action retry policies
class RetryPolicy(str, Enum):
    # 🧩 Define NEVER retry policy string constant
    NEVER = "never"
    # 🧩 Define SAFE retry policy string constant
    SAFE = "safe"
    # 🧩 Define ALWAYS retry policy string constant
    ALWAYS = "always"
# 🈳 Blank line
# 🈳 Blank line

# 🗺️ Define Action Pydantic model for individual plan steps
class Action(BaseModel):
    # 🗺️ Define action_id string field with min_length=1
    action_id: str = Field(min_length=1)
# 🈳 Blank line

    # 🧰 Define tool string field with min_length=1
    tool: str = Field(min_length=1)
# 🈳 Blank line

    # ⚙️ Define arguments dict field with default empty dictionary
    arguments: dict = Field(
        # ⚙️ Set default_factory to dict
        default_factory=dict,
    # ⚙️ Close arguments field definition
    )
# 🈳 Blank line

    # 🗺️ Define preconditions list of strings with default empty list
    preconditions: list[str] = Field(
        # 🗺️ Set default_factory to list
        default_factory=list,
    # 🗺️ Close preconditions field definition
    )
# 🈳 Blank line

    # 🎯 Define expected_result string field with min_length=1
    expected_result: str = Field(
        # 🎯 Ensure minimum length of 1
        min_length=1,
    # 🎯 Close expected_result field definition
    )
# 🈳 Blank line

    # 🧩 Define risk field using ActionRisk enum, defaulting to LOW
    risk: ActionRisk = ActionRisk.LOW
# 🈳 Blank line

    # ⚙️ Define timeout_seconds float field
    timeout_seconds: float = Field(
        # ⚙️ Set default timeout to 30.0 seconds
        default=30.0,
        # ⚙️ Ensure timeout is greater than 0
        gt=0,
    # ⚙️ Close timeout_seconds field definition
    )
# 🈳 Blank line

    # 🧩 Define retry_policy using RetryPolicy enum, defaulting to NEVER
    retry_policy: RetryPolicy = RetryPolicy.NEVER
# 🈳 Blank line

    # 🔍 Define verification_method string field with min_length=1
    verification_method: str = Field(
        # 🔍 Ensure minimum length of 1
        min_length=1,
    # 🔍 Close verification_method field definition
    )
# 🈳 Blank line

    # 🗺️ Define optional rollback_strategy string field defaulting to None
    rollback_strategy: str | None = None
# 🈳 Blank line
# 🈳 Blank line

# 🗺️ Define Plan Pydantic model representing a sequence of actions
class Plan(BaseModel):
    # 🎯 Define goal string field with min_length=1
    goal: str = Field(
        # 🎯 Ensure minimum length of 1
        min_length=1,
    # 🎯 Close goal field definition
    )
# 🈳 Blank line

    # 🗺️ Define actions list of Action models with min_length=1
    actions: list[Action] = Field(
        # 🗺️ Ensure at least one action in the plan
        min_length=1,
    # 🗺️ Close actions field definition
    )
# 🈳 Blank line

    # 🎯 Define success_criteria list of strings with min_length=1
    success_criteria: list[str] = Field(
        # 🎯 Ensure at least one success criterion
        min_length=1,
    # 🎯 Close success_criteria field definition
    )
    # 🈳 Blank space
    
# ⚙️ Define ResolvedArguments Pydantic model for LLM outputs
class ResolvedArguments(BaseModel):
    # 🧰 Define tool_name string field with min_length=1
    tool_name: str = Field(
        # 🧰 Ensure minimum length of 1
        min_length=1,
    # 🧰 Close tool_name field definition
    )
# 🈳 Blank line

    # ⚙️ Define arguments dict field with default empty dictionary
    arguments: dict = Field(
        # ⚙️ Set default_factory to dict
        default_factory=dict,
    # ⚙️ Close arguments field definition
    )