from app.intent.engine import IntentEngine
from app.llm.gateway import ModelResponse


class FakeGateway:
    def generate(self, messages):
        return ModelResponse(
            content=(
                '{'
                '"goal":"Clean the project folder",'
                '"constraints":["Do not permanently delete files"],'
                '"expected_outcome":"The folder is organized",'
                '"forbidden_actions":["Permanent deletion"],'
                '"missing_information":["Which folder should be cleaned"],'
                '"required_permissions":["filesystem"],'
                '"success_criteria":["Folder is organized"]'
                '}'
            )
        )


def test_intent_engine_parses_structured_response():
    engine = IntentEngine(
        gateway=FakeGateway(),
    )

    intent = engine.parse(
        "Clean this folder and don't delete anything."
    )

    assert intent.goal == "Clean the project folder"

    assert intent.constraints == [
        "Do not permanently delete files"
    ]

    assert intent.expected_outcome == (
        "The folder is organized"
    )

    assert intent.forbidden_actions == [
        "Permanent deletion"
    ]

    assert intent.missing_information == [
        "Which folder should be cleaned"
    ]

    assert intent.required_permissions == [
        "filesystem"
    ]

    assert intent.success_criteria == [
        "Folder is organized"
    ]
    
import pytest
from pydantic import ValidationError

from app.intent.engine import IntentEngine
from app.llm.gateway import ModelResponse


class InvalidGateway:
    def generate(self, messages):
        return ModelResponse(
            content='{"goal": ""}'
        )


def test_intent_engine_rejects_invalid_model_output():
    engine = IntentEngine(
        gateway=InvalidGateway(),
    )

    with pytest.raises(ValidationError):
        engine.parse("Do something.")