import pytest

from app.config import Settings
from app.intent.engine import IntentEngine
from app.llm.groq import GroqModelGateway


@pytest.fixture
def intent_engine() -> IntentEngine:
    settings = Settings()

    gateway = GroqModelGateway(
        api_key=settings.groq_api_key,
        model="openai/gpt-oss-20b",
    )

    return IntentEngine(
        gateway=gateway,
    )


@pytest.mark.real_groq
@pytest.mark.parametrize(
    "request_text",
    [
        "Read README.md and tell me what this project does.",
        "Clean this folder, but don't permanently delete anything.",
        "Run the tests for this Python project.",
        "Move the old reports into an archive folder.",
        "Don't change anything. Just tell me what is broken.",
    ],
)
def test_real_groq_intent_is_structurally_valid(
    intent_engine: IntentEngine,
    request_text: str,
):
    intent = intent_engine.parse(request_text)

    assert intent.goal.strip()
    assert intent.expected_outcome.strip()

    assert isinstance(intent.constraints, list)
    assert isinstance(intent.forbidden_actions, list)
    assert isinstance(intent.missing_information, list)
    assert isinstance(intent.required_permissions, list)
    assert isinstance(intent.success_criteria, list)
    
@pytest.mark.real_groq
def test_real_groq_identifies_missing_information(
    intent_engine: IntentEngine,
):
    intent = intent_engine.parse(
        "Clean this folder without deleting anything."
    )

    assert intent.goal.strip()

    assert (
        len(intent.missing_information) > 0
        or len(intent.constraints) > 0
    )