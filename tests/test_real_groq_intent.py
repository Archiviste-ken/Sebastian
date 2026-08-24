from app.config import Settings
from app.intent.engine import IntentEngine
from app.llm.groq import GroqModelGateway


def test_real_groq_generates_intent():
    settings = Settings()

    gateway = GroqModelGateway(
        api_key=settings.groq_api_key,
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