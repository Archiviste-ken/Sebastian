from types import SimpleNamespace

from app.llm.gateway import ModelResponse
from app.llm.groq import GroqModelGateway


class FakeCompletions:
    def create(self, *, model, messages):
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content="Hello from Groq!"
                    )
                )
            ]
        )


class FakeChat:
    completions = FakeCompletions()


class FakeClient:
    chat = FakeChat()


def test_groq_gateway_generates_response():
    gateway = GroqModelGateway(
        client=FakeClient(),
        model="fake-model",
    )

    result = gateway.generate(
        [
            {
                "role": "user",
                "content": "Hello",
            }
        ]
    )

    assert isinstance(result, ModelResponse)
    assert result.content == "Hello from Groq!"
    assert result.raw is not None