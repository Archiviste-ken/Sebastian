# 🔧 Tool result container
# 🎯 This is the normalized answer returned after a tool runs.
# 🔄 It keeps execution output consistent regardless of whether the tool succeeded or failed.

# 📦 Import dataclass from dataclasses to create a lightweight data container.
from dataclasses import dataclass
# 📦 Import Enum from enum for string-based enumeration.
from enum import Enum
# 📦 Import Any from typing for generic type hints.
from typing import Any


# 🏷️ Define ToolResultStatus enum for representing tool execution outcomes.
class ToolResultStatus(str, Enum):
    # ✅ Indicates the tool ran successfully.
    SUCCESS = "success"
    # ❌ Indicates the tool encountered an error or failed.
    FAILED = "failed"
    # 🛡️ Indicates the tool is waiting for user approval.
    WAITING_APPROVAL = "waiting_approval"
    # 🛑 Indicates the tool execution was blocked.
    BLOCKED = "blocked"


# 🏷️ Define the ToolResult dataclass. frozen=True makes it immutable.
@dataclass(frozen=True)
class ToolResult:
    # 🔄 Represents the status outcome of the tool call.
    status: ToolResultStatus
    # 📝 Holds the returned data from the tool, can be of any type, defaults to None.
    data: Any = None
    # ❌ Holds error message string if the tool failed, defaults to None.
    error: str | None = None

    # 🎯 Define a property for quick success checking.
    @property
    def success(self) -> bool:
        # ✅ Returns True if the status is SUCCESS, otherwise False.
        return self.status == ToolResultStatus.SUCCESS