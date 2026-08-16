import pytest
from pydantic import ValidationError

from app.models.action import Action


def test_action_creation():
    action = Action(
        id="action-1",
        plan_id="plan-1",
        description="Run the project's test suite",
    )

    assert action.id == "action-1"
    assert action.plan_id == "plan-1"


def test_action_rejects_empty_description():
    with pytest.raises(ValidationError):
        Action(
            id="action-2",
            plan_id="plan-1",
            description="",
        )