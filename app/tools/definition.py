from dataclasses import dataclass
from typing import Callable, Any


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    handler: Callable[..., Any]