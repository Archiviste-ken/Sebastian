# 🧩 Tool definition
# This is the contract for any tool Sebastian may execute.
# A tool has a name, a human-readable description, and a callable handler.

# 📦 Import dataclass to define structured record types.
from dataclasses import dataclass
# 📦 Import typing primitives for handler signature definition.
from typing import Any, Callable


# 🏗️ Define a frozen dataclass representing the schema of a single tool.
@dataclass(frozen=True)
# ⚙️ This class establishes the minimum requirements to register a tool.
class ToolDefinition:
    # 🏷️ The unique, string-based identifier for the tool.
    name: str
    # 💬 A human-readable description explaining what the tool does.
    description: str
    # 🔌 The actual function to execute when the tool is called.
    handler: Callable[..., Any]
    # 🔧 Whether this tool's handler expects an ExecutionContext object.
    uses_context: bool = False
    # 🧩 Optional dictionary defining the expected argument schema.
    argument_schema: dict[str, Any] | None = None