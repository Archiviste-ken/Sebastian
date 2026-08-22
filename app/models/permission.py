# 🛡️ Permission model
# This models the safety boundary around what Sebastian is allowed to do.
# It reflects the project's idea that some tools are safe to run automatically,
# while others require approval or are prohibited entirely.

from enum import Enum

from pydantic import BaseModel


class PermissionLevel(str, Enum):
    # 🟢 No approval needed; tool may run autonomously.
    AUTONOMOUS = "autonomous"

    # 🟡 Requires human approval before execution.
    APPROVAL = "approval"

    # 🔴 Explicitly blocked; may not run.
    BLOCKED = "blocked"


class Permission(BaseModel):
    # 🆔 Unique permission record identifier.
    id: str

    # 🧰 Name of the tool this permission controls.
    tool_name: str

    # 🔐 Permission level for that tool.
    level: PermissionLevel