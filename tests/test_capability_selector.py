from app.intent.models import Intent
from app.planning.selector import CapabilitySelector


def test_selector_identifies_read_file():
    intent = Intent(
        goal="Read README.md",
        constraints=[],
        expected_outcome="Return the README contents.",
        forbidden_actions=[],
        missing_information=[],
        required_permissions=["filesystem"],
        success_criteria=[
            "README contents are returned.",
        ],
    )

    selector = CapabilitySelector()

    capabilities = selector.select(intent)

    assert [item.name for item in capabilities] == [
        "read_file",
    ]


def test_selector_identifies_test_execution():
    intent = Intent(
        goal="Run the Python project's tests.",
        constraints=[],
        expected_outcome="The test suite runs.",
        forbidden_actions=[],
        missing_information=[],
        required_permissions=["terminal"],
        success_criteria=[
            "Pytest completes.",
        ],
    )

    selector = CapabilitySelector()

    capabilities = selector.select(intent)

    assert [item.name for item in capabilities] == [
        "run_command",
    ]


def test_selector_identifies_folder_inspection():
    intent = Intent(
        goal="Inspect this folder.",
        constraints=[],
        expected_outcome="Understand what is inside it.",
        forbidden_actions=[],
        missing_information=[],
        required_permissions=["filesystem"],
        success_criteria=[
            "Directory contents are known.",
        ],
    )

    selector = CapabilitySelector()

    capabilities = selector.select(intent)

    assert [item.name for item in capabilities] == [
        "list_directory",
    ]