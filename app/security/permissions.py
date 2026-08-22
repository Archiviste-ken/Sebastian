from dataclasses import dataclass
from enum import Enum


class PermissionLevel(str, Enum):
    AUTONOMOUS = "autonomous"
    APPROVAL = "approval"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class PermissionDecision:
    allowed: bool
    requires_approval: bool
    reason: str


class PermissionKernel:
    def __init__(self, permissions: dict[str, PermissionLevel]):
        self._permissions = permissions

    def get_level(self, tool_name: str) -> PermissionLevel:
        return self._permissions.get(
            tool_name,
            PermissionLevel.BLOCKED,
        )

    def check(self, tool_name: str) -> PermissionDecision:
        level = self.get_level(tool_name)

        if level == PermissionLevel.AUTONOMOUS:
            return PermissionDecision(
                allowed=True,
                requires_approval=False,
                reason="Tool is permitted autonomously.",
            )

        if level == PermissionLevel.APPROVAL:
            return PermissionDecision(
                allowed=False,
                requires_approval=True,
                reason="User approval is required.",
            )

        return PermissionDecision(
            allowed=False,
            requires_approval=False,
            reason="Tool is blocked.",
        )