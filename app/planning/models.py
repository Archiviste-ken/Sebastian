from enum import Enum

from pydantic import BaseModel, Field


class ActionRisk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RetryPolicy(str, Enum):
    NEVER = "never"
    SAFE = "safe"
    ALWAYS = "always"


class Action(BaseModel):
    action_id: str = Field(min_length=1)

    tool: str = Field(min_length=1)

    arguments: dict = Field(
        default_factory=dict,
    )

    preconditions: list[str] = Field(
        default_factory=list,
    )

    expected_result: str = Field(
        min_length=1,
    )

    risk: ActionRisk = ActionRisk.LOW

    timeout_seconds: float = Field(
        default=30.0,
        gt=0,
    )

    retry_policy: RetryPolicy = RetryPolicy.NEVER

    verification_method: str = Field(
        min_length=1,
    )

    rollback_strategy: str | None = None


class Plan(BaseModel):
    goal: str = Field(
        min_length=1,
    )

    actions: list[Action] = Field(
        min_length=1,
    )

    success_criteria: list[str] = Field(
        min_length=1,
    )
    
class ResolvedArguments(BaseModel):
    tool_name: str = Field(
        min_length=1,
    )

    arguments: dict = Field(
        default_factory=dict,
    )