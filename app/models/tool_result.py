from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ToolResult:
    success: bool
    data: Any = None
    error: str | None = None