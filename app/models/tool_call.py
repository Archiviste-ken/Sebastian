# 📦 Import Any from typing for flexible type hinting.
from typing import Any

# 📦 Import BaseModel from pydantic to define the data model.
from pydantic import BaseModel


# 🧰 Tool call model
# 🎯 This small request object travels through the execution pipeline.
class ToolCall(BaseModel):
    # 🏷️ Registered name of the tool to run, such as `read_file`.
    # 📝 Represents the string name of the tool.
    tool_name: str

    # 📦 Named values the tool handler needs, such as a file path.
    # 📝 A dictionary storing the tool's arguments, defaulting to an empty dict.
    arguments: dict[str, Any] = {}
