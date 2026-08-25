# 🔐 Permission rules
# Each tool gets one clear outcome: run now, ask first, or do not run.

# 📦 Import dataclass to create structured, immutable data objects.
from dataclasses import dataclass
# 📦 Import Enum to define a set of named, constant values.
from enum import Enum


# 🏷️ Define an enumeration for the different levels of permission a tool can have.
class PermissionLevel(str, Enum):
    # 🟢 The tool may run without asking the user again.
    AUTONOMOUS = "autonomous"
    # 🟡 The tool must wait for a user's approval.
    APPROVAL = "approval"
    # 🔴 The tool is not allowed to run.
    BLOCKED = "blocked"


# 🏗️ Define a frozen dataclass to represent the final permission decision.
@dataclass(frozen=True)
# 🛡️ This class encapsulates the allowed state, approval need, and reasoning.
class PermissionDecision:
    # ✅ Whether execution can continue immediately.
    allowed: bool
    # 🙋 Whether a user can unblock the action by approving it.
    requires_approval: bool
    # 💬 A clear explanation for users, logs, and tests.
    reason: str


# ⚙️ Define the core kernel that checks tool permissions against a defined policy.
class PermissionKernel:
    # 🛠️ Initialize the kernel with a dictionary mapping tool names to their permission levels.
    def __init__(self, permissions: dict[str, PermissionLevel]):
        # 🗺️ Map each tool name to its allowed level.
        self._permissions = permissions

    # 🔍 Method to retrieve the permission level for a specific tool by its name.
    def get_level(self, tool_name: str) -> PermissionLevel:
        # 🚫 Unknown tools are blocked by default—a safe fallback.
        # 📥 Look up the tool in the permissions map, defaulting to BLOCKED if not found.
        return self._permissions.get(
            # 🏷️ The name of the tool to look up.
            tool_name,
            # 🔴 The default fallback value if the tool is absent.
            PermissionLevel.BLOCKED,
        )

    # 🛡️ Method to check a tool and return a comprehensive PermissionDecision object.
    def check(self, tool_name: str) -> PermissionDecision:
        # 🔎 Translate a simple level into the detailed decision the executor needs.
        # 📥 Retrieve the permission level for the given tool name.
        level = self.get_level(tool_name)

        # ⚖️ Check if the retrieved level allows autonomous execution.
        if level == PermissionLevel.AUTONOMOUS:
            # ✅ Nothing else is needed; the tool can proceed.
            # 🏗️ Return a decision indicating the tool is allowed without approval.
            return PermissionDecision(
                # 🟢 Set allowed to True since it's autonomous.
                allowed=True,
                # 🟢 Set requires_approval to False as it runs automatically.
                requires_approval=False,
                # 📝 Provide a clear reason for the autonomous approval.
                reason="Tool is permitted autonomously.",
            )

        # ⚖️ Check if the retrieved level requires user approval.
        if level == PermissionLevel.APPROVAL:
            # ⏸️ Do not run yet; surface the request for human approval.
            # 🏗️ Return a decision indicating the tool needs approval before running.
            return PermissionDecision(
                # 🔴 Set allowed to False until approved.
                allowed=False,
                # 🟡 Set requires_approval to True to prompt the user.
                requires_approval=True,
                # 📝 Provide a clear reason stating approval is needed.
                reason="User approval is required.",
            )

        # 🚫 This covers explicitly blocked and unknown tools.
        # 🏗️ Return a decision indicating the tool is completely blocked.
        return PermissionDecision(
            # 🔴 Set allowed to False as it is blocked.
            allowed=False,
            # 🔴 Set requires_approval to False as approval cannot unblock it.
            requires_approval=False,
            # 📝 Provide a clear reason stating the tool is blocked.
            reason="Tool is blocked.",
        )
