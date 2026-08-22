# 🧰 Tool call model
# This describes a single tool invocation from within an action.
# It records which tool ran, which action triggered it, and what arguments it received.

from typing import Any

from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    # 🆔 Unique call identifier.
    id: str

    # ⚙️ The action that requested this tool call.
    action_id: str

    # 🏷️ Name of the tool being invoked.
    tool_name: str = Field(min_length=1)

    # 📥 Arguments passed to the tool.
    arguments: dict[str, Any] = {}