# 🗂️ Tool registry
# This registry keeps track of every tool Sebastian can use.
# It acts like a capability index for the execution system.

from app.tools.definition import ToolDefinition


class ToolRegistry:
    def __init__(self):
        # 📚 Dictionary of tool names to their definitions.
        self._tools: dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        # 🧾 Prevent duplicate registration to keep the capability map clean.
        if tool.name in self._tools:
            raise ValueError(f"Tool already registered: {tool.name}")

        self._tools[tool.name] = tool

    def get(self, name: str) -> ToolDefinition:
        # 🔎 Fetch a tool by name or raise a clear error when missing.
        if name not in self._tools:
            raise KeyError(f"Tool not found: {name}")

        return self._tools[name]

    def list_tools(self) -> list[ToolDefinition]:
        # 📜 Return all registered tools in insertion order.
        return list(self._tools.values())