import os

import pytest
from groq import Groq

from app.intent.engine import IntentEngine
from app.llm.groq import GroqModelGateway


@pytest.mark.real_groq
@pytest.mark.skipif(
    not os.getenv("GROQ_API_KEY"),
    reason="GROQ_API_KEY is not configured.",
)
def test_real_groq_generates_intent():
    client = Groq(
        api_key=os.environ["GROQ_API_KEY"],
    )

    gateway = GroqModelGateway(
        client=client,
        model="openai/gpt-oss-20b",
    )

    engine = IntentEngine(
        gateway=gateway,
    )

    intent = engine.parse(
        "Clean this folder but do not permanently delete anything."
    )

    assert intent.goal
    assert intent.expected_outcome

    assert isinstance(intent.constraints, list)
    assert isinstance(intent.forbidden_actions, list)
    assert isinstance(intent.missing_information, list)
    assert isinstance(intent.required_permissions, list)
    assert isinstance(intent.success_criteria, list)