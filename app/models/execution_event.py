# 🧪 Execution event model
# This records what happened during a tool execution.
# It turns raw tool behavior into traceable evidence for verification and debugging.

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class ExecutionEvent(BaseModel):
    # 🆔 Unique execution event identifier.
    id: str

    # 🔗 Tool call this event is associated with.
    tool_call_id: str

    # 🏷️ Event category, such as "tool_started" or "tool_completed".
    event_type: str = Field(min_length=1)

    # ✅ Whether the event indicates success or failure.
    success: bool

    # 🕒 When the event occurred.
    timestamp: datetime

    # 📦 Additional execution metadata such as exit codes or outputs.
    data: dict[str, Any] = {}