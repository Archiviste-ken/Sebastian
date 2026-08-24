from typing import Any

from groq import AuthenticationError, Groq

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
        else:
            key = api_key or ""

            if not key.strip():
                raise RuntimeError(
                    "Groq API key is required."
                )

            self.client = Groq(
                api_key=key,
            )

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

        try:
            response = self.client.chat.completions.create(
                **request,
            )
        except AuthenticationError as exc:
            raise RuntimeError(
                "Groq authentication failed: verify GROQ_API_KEY in .env."
            ) from exc

        content = response.choices[0].message.content or ""

        return ModelResponse(
            content=content,
            raw=response,
        )
