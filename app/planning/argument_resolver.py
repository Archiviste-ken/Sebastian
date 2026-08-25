from typing import Any

from app.intent.models import Intent
from app.llm.gateway import ModelGateway
from app.planning.models import ResolvedArguments
from app.tools.definition import ToolDefinition


class ArgumentResolver:
    def __init__(self, gateway: ModelGateway):
        self.gateway = gateway

    def resolve(
        self,
        intent: Intent,
        tool: ToolDefinition,
    ) -> dict[str, Any]:
        if tool.argument_schema is None:
            raise ValueError(
                f"Tool '{tool.name}' has no argument schema."
            )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are Sebastian's tool argument resolver. "
                    "Given a validated intent and a selected tool, "
                    "produce only the arguments required by that tool. "
                    "Never execute the tool. "
                    "Never invent missing information. "
                    "If the required information is unavailable, "
                    "return an empty arguments object."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Intent:\n{intent.model_dump_json()}\n\n"
                    f"Selected tool:\n"
                    f"{tool.name}\n\n"
                    f"Tool argument schema:\n"
                    f"{tool.argument_schema}"
                ),
            },
        ]

        response = self.gateway.generate(
            messages=messages,
        )

        resolved = ResolvedArguments.model_validate_json(
            response.content
        )

        if resolved.tool_name != tool.name:
            raise ValueError(
                "Resolved tool does not match the selected tool."
            )

        return resolved.arguments