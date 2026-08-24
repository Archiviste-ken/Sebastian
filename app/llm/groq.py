from typing import Any

from groq import Groq

from app.llm.gateway import ModelGateway, ModelResponse


class GroqModelGateway(ModelGateway):
    def __init__(
        self,
        model: str,
        client: Any | None = None,
        api_key: str | None = None,
    ):
        self.model = model

        if client is not None:
            self.client = client
        elif api_key:
            self.client = Groq(
                api_key=api_key,
            )
        else:
            self.client = Groq()

    def generate(
        self,
        messages: list[dict[str, str]],
        response_format: dict[str, Any] | None = None,
    ) -> ModelResponse:
        request: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
        }

        if response_format is not None:
            request["response_format"] = response_format

        response = self.client.chat.completions.create(
            **request,
        )

        content = response.choices[0].message.content or ""

        return ModelResponse(
            content=content,
            raw=response,
        )