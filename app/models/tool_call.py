from typing import Any

from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    id: str
    action_id: str
    tool_name: str = Field(min_length=1)
    arguments: dict[str, Any] = {}