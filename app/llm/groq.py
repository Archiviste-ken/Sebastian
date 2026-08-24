from typing import Any

from app.llm.gateway import ModelGateway, ModelResponse


class GroqModelGateway(ModelGateway):
    def __init__(
        self,
        client: Any,
        model: str,
    ):
        self.client = client
        self.model = model

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