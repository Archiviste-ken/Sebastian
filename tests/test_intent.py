import pytest
from pydantic import ValidationError

from app.intent.models import Intent


def test_intent_accepts_valid_data():
    intent = Intent(
        goal="Clean the project folder.",
        constraints=[
            "Do not permanently delete files.",
        ],
        expected_outcome="The project folder is organized.",
        forbidden_actions=[
            "Permanent deletion.",
        ],
        missing_information=[],
        required_permissions=[
            "filesystem",
        ],
        success_criteria=[
            "Folder is organized.",
            "No files were permanently deleted.",
        ],
    )

    assert intent.goal == "Clean the project folder."
    assert intent.constraints == [
        "Do not permanently delete files.",
    ]


def test_intent_defaults_optional_lists():
    intent = Intent(
        goal="Read a file.",
        expected_outcome="Return the file contents.",
    )

    assert intent.constraints == []
    assert intent.forbidden_actions == []
    assert intent.missing_information == []
    assert intent.required_permissions == []
    assert intent.success_criteria == []


def test_intent_rejects_empty_goal():
    with pytest.raises(ValidationError):
        Intent(
            goal="",
            expected_outcome="Something happens.",
        )


def test_intent_rejects_empty_expected_outcome():
    with pytest.raises(ValidationError):
        Intent(
            goal="Read a file.",
            expected_outcome="",
        )