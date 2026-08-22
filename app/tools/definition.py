# 🧩 Tool definition
# This is the contract for any tool Sebastian may execute.
# A tool has a name, a human-readable description, and a callable handler.

from dataclasses import dataclass
from typing import Callable, Any


@dataclass(frozen=True)
class ToolDefinition:
    # 🏷️ Tool identifier used for lookup and dispatch.
    name: str

    # 📝 Description of what the tool does.
    description: str

    # ⚙️ The actual Python function that runs the tool logic.
    handler: Callable[..., Any]