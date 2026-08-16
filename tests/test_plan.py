import pytest
from pydantic import ValidationError

from app.models.plan import Plan


def test_plan_creation():
    plan = Plan(
        id="plan-1",
        task_id="task-1",
        description="Inspect the project and run its tests",
    )

    assert plan.id == "plan-1"
    assert plan.task_id == "task-1"


def test_plan_rejects_empty_description():
    with pytest.raises(ValidationError):
        Plan(
            id="plan-2",
            task_id="task-1",
            description="",
        )