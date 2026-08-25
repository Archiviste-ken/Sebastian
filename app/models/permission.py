# 🛡️ Permission model
# 📖 This models the safety boundary around what Sebastian is allowed to do.
# 🔄 It reflects the project's idea that some tools are safe to run automatically,
# ❌ while others require approval or are prohibited entirely.
# 💨 Empty line for spacing
from enum import Enum # 📦 Import Enum for permission levels
# 💨 Empty line for spacing
from pydantic import BaseModel # 📦 Import BaseModel from pydantic for validation
# 💨 Empty line for spacing
# 💨 Empty line for spacing
class PermissionLevel(str, Enum): # 🏷️ Define PermissionLevel enum inheriting from str
    # 🟢 No approval needed; tool may run autonomously.
    AUTONOMOUS = "autonomous" # 📝 Autonomous level string
# 💨 Empty line for spacing
    # 🟡 Requires human approval before execution.
    APPROVAL = "approval" # 📝 Approval level string
# 💨 Empty line for spacing
    # 🔴 Explicitly blocked; may not run.
    BLOCKED = "blocked" # 📝 Blocked level string
# 💨 Empty line for spacing
# 💨 Empty line for spacing
class Permission(BaseModel): # 🏷️ Define Permission class inheriting from BaseModel
    # 🆔 Unique permission record identifier.
    id: str # 📝 ID string for permission
# 💨 Empty line for spacing
    # 🧰 Name of the tool this permission controls.
    tool_name: str # 📝 Tool name string
# 💨 Empty line for spacing
    # 🔐 Permission level for that tool.
    level: PermissionLevel # 📝 Level using PermissionLevel enum