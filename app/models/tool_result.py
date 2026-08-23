# 🔧 Tool result container
# This is the normalized answer returned after a tool runs.
# It keeps execution output consistent regardless of whether the tool succeeded or failed.

from dataclasses import dataclass
from enum import Enum
from typing import Any


class ToolResultStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    WAITING_APPROVAL = "waiting_approval"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class ToolResult:
    status: ToolResultStatus
    data: Any = None
    error: str | None = None

    @property
    def success(self) -> bool:
        return self.status == ToolResultStatus.SUCCESS