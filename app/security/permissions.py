# 🔐 Permission rules
# Each tool gets one clear outcome: run now, ask first, or do not run.

from dataclasses import dataclass
from enum import Enum


class PermissionLevel(str, Enum):
    # 🟢 The tool may run without asking the user again.
    AUTONOMOUS = "autonomous"
    # 🟡 The tool must wait for a user's approval.
    APPROVAL = "approval"
    # 🔴 The tool is not allowed to run.
    BLOCKED = "blocked"


@dataclass(frozen=True)
class PermissionDecision:
    # ✅ Whether execution can continue immediately.
    allowed: bool
    # 🙋 Whether a user can unblock the action by approving it.
    requires_approval: bool
    # 💬 A clear explanation for users, logs, and tests.
    reason: str


class PermissionKernel:
    def __init__(self, permissions: dict[str, PermissionLevel]):
        # 🗺️ Map each tool name to its allowed level.
        self._permissions = permissions

    def get_level(self, tool_name: str) -> PermissionLevel:
        # 🚫 Unknown tools are blocked by default—a safe fallback.
        return self._permissions.get(
            tool_name,
            PermissionLevel.BLOCKED,
        )

    def check(self, tool_name: str) -> PermissionDecision:
        # 🔎 Translate a simple level into the detailed decision the executor needs.
        level = self.get_level(tool_name)

        if level == PermissionLevel.AUTONOMOUS:
            # ✅ Nothing else is needed; the tool can proceed.
            return PermissionDecision(
                allowed=True,
                requires_approval=False,
                reason="Tool is permitted autonomously.",
            )

        if level == PermissionLevel.APPROVAL:
            # ⏸️ Do not run yet; surface the request for human approval.
            return PermissionDecision(
                allowed=False,
                requires_approval=True,
                reason="User approval is required.",
            )

        # 🚫 This covers explicitly blocked and unknown tools.
        return PermissionDecision(
            allowed=False,
            requires_approval=False,
            reason="Tool is blocked.",
        )
