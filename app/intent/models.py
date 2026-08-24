from pydantic import BaseModel, Field


class Intent(BaseModel):
    goal: str = Field(
        min_length=1,
        description="What the user ultimately wants accomplished.",
    )

    constraints: list[str] = Field(
        default_factory=list,
        description="Rules or limitations that must be respected.",
    )

    expected_outcome: str = Field(
        min_length=1,
        description="What the successful final result should look like.",
    )

    forbidden_actions: list[str] = Field(
        default_factory=list,
        description="Actions Sebastian must not take.",
    )

    missing_information: list[str] = Field(
        default_factory=list,
        description="Information needed before execution can safely proceed.",
    )

    required_permissions: list[str] = Field(
        default_factory=list,
        description="Permissions that may be required to accomplish the task.",
    )

    success_criteria: list[str] = Field(
        default_factory=list,
        description="Checks that determine whether the task succeeded.",
    )