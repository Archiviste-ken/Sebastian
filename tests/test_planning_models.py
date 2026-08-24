import pytest
from pydantic import ValidationError

from app.planning.models import (
    Action,
    ActionRisk,
    Plan,
    RetryPolicy,
)


def test_action_accepts_valid_data():
    action = Action(
        action_id="run-tests",
        tool="run_command",
        arguments={
            "command": ["pytest"],
        },
        preconditions=[
            "Project contains a test suite.",
        ],
        expected_result="Tests execute and produce a result.",
        risk=ActionRisk.LOW,
        timeout_seconds=60,
        retry_policy=RetryPolicy.SAFE,
        verification_method="Inspect pytest exit code.",
        rollback_strategy=None,
    )

    assert action.action_id == "run-tests"
    assert action.tool == "run_command"
    assert action.arguments["command"] == ["pytest"]


def test_plan_accepts_valid_actions():
    plan = Plan(
        goal="Run the project tests.",
        actions=[
            Action(
                action_id="run-tests",
                tool="run_command",
                arguments={
                    "command": ["pytest"],
                },
                expected_result="Tests complete.",
                verification_method="Inspect exit code.",
            )
        ],
        success_criteria=[
            "The test suite completes.",
            "Results are captured.",
        ],
    )

    assert plan.goal == "Run the project tests."
    assert len(plan.actions) == 1


def test_action_rejects_empty_tool():
    with pytest.raises(ValidationError):
        Action(
            action_id="bad-action",
            tool="",
            expected_result="Something happens.",
            verification_method="Check result.",
        )


def test_plan_requires_at_least_one_action():
    with pytest.raises(ValidationError):
        Plan(
            goal="Do something.",
            actions=[],
            success_criteria=[
                "Something happened.",
            ],
        )