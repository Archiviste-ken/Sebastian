from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class ExecutionEvent(BaseModel):
    id: str
    tool_call_id: str
    event_type: str = Field(min_length=1)
    success: bool
    timestamp: datetime
    data: dict[str, Any] = {}