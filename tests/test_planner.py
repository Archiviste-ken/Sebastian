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


def test_planner_requests_missing_information():
    intent = Intent(
        goal="Clean the folder.",
        constraints=[
            "Do not permanently delete anything.",
        ],
        expected_outcome="The folder is organized.",
        forbidden_actions=[
            "Permanent deletion.",
        ],
        missing_information=[
            "Which folder should be cleaned?",
        ],
        required_permissions=["filesystem"],
        success_criteria=[
            "The folder is organized.",
        ],
    )

    planner = Planner()

    plan = planner.build(intent)

    assert len(plan.actions) == 1

    action = plan.actions[0]

    assert action.action_id == "request-missing-information"
    assert action.tool == "ask_user"

    assert action.arguments == {
        "questions": [
            "Which folder should be cleaned?",
        ]
    }

    assert plan.success_criteria == [
        "All required information is available.",
    ]