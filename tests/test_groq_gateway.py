from types import SimpleNamespace

import httpx
import pytest
from groq import AuthenticationError

from app.config import Settings
from app.llm.gateway import ModelResponse
from app.llm.groq import GroqModelGateway


class FakeCompletions:
    def create(self, *, model, messages, response_format=None):
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content="Hello from Groq!",
                    )
                )
            ]
        )


class FakeChat:
    completions = FakeCompletions()


class FakeClient:
    chat = FakeChat()


class CapturingGroq:
    received_api_key: str | None = None

    def __init__(self, *, api_key: str):
        type(self).received_api_key = api_key


class AuthenticationFailingCompletions:
    def create(self, **_kwargs):
        raise AuthenticationError(
            "Invalid API Key",
            response=httpx.Response(
                401,
                request=httpx.Request("POST", "https://api.groq.com"),
            ),
            body=None,
        )


class AuthenticationFailingClient:
    chat = SimpleNamespace(completions=AuthenticationFailingCompletions())


def test_groq_gateway_generates_response():
    gateway = GroqModelGateway(
        client=FakeClient(),
        model="fake-model",
    )

    result = gateway.generate(
        messages=[
            {
                "role": "user",
                "content": "Hello",
            }
        ]
    )

    assert isinstance(result, ModelResponse)
    assert result.content == "Hello from Groq!"
    assert result.raw is not None


def test_groq_gateway_passes_settings_key_to_groq_unchanged(monkeypatch):
    monkeypatch.setattr("app.llm.groq.Groq", CapturingGroq)
    settings = Settings()

    GroqModelGateway(
        api_key=settings.groq_api_key,
        model="fake-model",
    )

    assert settings.groq_api_key
    assert CapturingGroq.received_api_key == settings.groq_api_key


def test_groq_gateway_reports_authentication_failure_without_credentials():
    gateway = GroqModelGateway(
        client=AuthenticationFailingClient(),
        model="fake-model",
    )

    with pytest.raises(
        RuntimeError,
        match="Groq authentication failed: verify GROQ_API_KEY in .env.",
    ):
        gateway.generate(messages=[{"role": "user", "content": "Hello"}])
