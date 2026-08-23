# # 🧰 Tool call model
# # This describes a single tool invocation from within an action.
# # It records which tool ran, which action triggered it, and what arguments it received.

# from typing import Any

# from pydantic import BaseModel, Field


# class ToolCall(BaseModel):
#     # 🆔 Unique call identifier.
#     id: str

#     # ⚙️ The action that requested this tool call.
#     action_id: str

#     # 🏷️ Name of the tool being invoked.
#     tool_name: str = Field(min_length=1)

#     # 📥 Arguments passed to the tool.
#     arguments: dict[str, Any] = {}

from typing import Any

from pydantic import BaseModel


# 🧰 Tool call model
# This small request object travels through the execution pipeline.
class ToolCall(BaseModel):
    # 🏷️ Registered name of the tool to run, such as `read_file`.
    tool_name: str

    # 📦 Named values the tool handler needs, such as a file path.
    arguments: dict[str, Any] = {}
