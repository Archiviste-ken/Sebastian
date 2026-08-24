from app.intent.models import Intent
from app.llm.gateway import ModelGateway

class IntentEngine:
    def __init__(self, gateway: ModelGateway):
        self.gateway = gateway

    def parse(self, user_request: str) -> Intent:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are Sebastian's intent extraction engine. "
                    "Understand what the user wants before deciding how "
                    "to accomplish it. Return only valid JSON matching "
                    "the requested intent structure."
                ),
            },
            {
                "role": "user",
                "content": user_request,
            },
        ]

        response = self.gateway.generate(messages)

        return Intent.model_validate_json(response.content)