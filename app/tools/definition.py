# 🧩 Tool definition
# This is the contract for any tool Sebastian may execute.
# A tool has a name, a human-readable description, and a callable handler.

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    handler: Callable[..., Any]
    uses_context: bool = False
    argument_schema: dict[str, Any] | None = None