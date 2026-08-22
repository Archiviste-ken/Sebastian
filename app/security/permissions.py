from enum import Enum


class PermissionLevel(str, Enum):
    AUTONOMOUS = "autonomous"
    APPROVAL = "approval"
    BLOCKED = "blocked"


class PermissionKernel:
    def __init__(self, permissions: dict[str, PermissionLevel]):
        self._permissions = permissions

    def get_level(self, tool_name: str) -> PermissionLevel:
        return self._permissions.get(
            tool_name,
            PermissionLevel.BLOCKED,
        )