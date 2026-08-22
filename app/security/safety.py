from dataclasses import dataclass
from typing import Any

from app.models.tool_call import ToolCall


@dataclass(frozen=True)
class SafetyDecision:
    safe: bool
    reason: str


class ToolSafety:
    def check(self, tool_call: ToolCall) -> SafetyDecision:
        if not tool_call.tool_name.strip():
            return SafetyDecision(
                safe=False,
                reason="Tool name cannot be empty.",
            )

        if tool_call.arguments is None:
            return SafetyDecision(
                safe=False,
                reason="Tool arguments cannot be null.",
            )

        return SafetyDecision(
            safe=True,
            reason="Tool call passed basic safety checks.",
        )