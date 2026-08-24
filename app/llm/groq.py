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
    ) -> ModelResponse:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        content = response.choices[0].message.content or ""

        return ModelResponse(
            content=content,
            raw=response,
        )