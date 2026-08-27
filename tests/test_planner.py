from app.intent.models import Intent
from app.planning.models import ActionRisk
from app.planning.planner import Planner


def test_planner_builds_plan_from_intent():
    intent = Intent(
        goal="Run the project tests.",
        constraints=[],
        expected_outcome="The test suite finishes successfully.",
        forbidden_actions=[],
        missing_information=[],
        required_permissions=["terminal"],
        success_criteria=[
            "The test suite completes.",
        ],
    )

    planner = Planner()

    plan = planner.build(intent)

    assert plan.goal == intent.goal
    assert len(plan.actions) == 1

    action = plan.actions[0]

    assert action.action_id == "candidate-1"
    assert action.tool == "run_command"
    assert action.risk == ActionRisk.HIGH

    assert plan.success_criteria == [
        "The test suite completes.",
    ]


def test_planner_raises_value_error_on_no_capabilities():
    intent = Intent(
        goal="Do something completely unsupported.",
        constraints=[],
        expected_outcome="Magic happens.",
        forbidden_actions=[],
        missing_information=[],
        required_permissions=[],
        success_criteria=["Magic."],
    )

    planner = Planner()

    import pytest
    with pytest.raises(ValueError, match="No available Sebastian capability matches this request."):
        planner.build(intent)