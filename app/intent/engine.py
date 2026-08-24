from typing import Any

from app.intent.models import Intent
from app.llm.gateway import ModelGateway


class IntentEngine:
    def __init__(self, gateway: ModelGateway):
        self.gateway = gateway

    def _strict_schema(self) -> dict[str, Any]:
        schema = Intent.model_json_schema()

        # Groq strict structured outputs require every property
        # to appear in `required`.
        properties = schema.get("properties", {})

        schema["required"] = list(properties.keys())
        schema["additionalProperties"] = False

        return schema

    def parse(self, user_request: str) -> Intent:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are Sebastian's intent extraction engine. "
                    "Understand what the user wants before deciding how "
                    "to accomplish it. Extract the user's goal, constraints, "
                    "expected outcome, forbidden actions, missing information, "
                    "required permissions, and success criteria."
                ),
            },
            {
                "role": "user",
                "content": user_request,
            },
        ]

        response_format: dict[str, Any] = {
            "type": "json_schema",
            "json_schema": {
                "name": "sebastian_intent",
                "strict": True,
                "schema": self._strict_schema(),
            },
        }

        response = self.gateway.generate(
            messages=messages,
            response_format=response_format,
        )

        return Intent.model_validate_json(response.content)