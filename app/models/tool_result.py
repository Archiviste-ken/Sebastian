# 🔧 Tool result container
# This is the normalized answer returned after a tool runs.
# It keeps execution output consistent regardless of whether the tool succeeded or failed.

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ToolResult:
    # ✅ Whether the tool completed successfully.
    success: bool

    # 📦 Result payload returned by the tool, if any.
    data: Any = None

    # ❌ Error message if the tool failed.
    error: str | None = None