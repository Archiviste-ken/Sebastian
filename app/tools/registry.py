# 🗂️ Tool registry
# This registry keeps track of every tool Sebastian can use.
# It acts like a capability index for the execution system.

# 📦 Import the ToolDefinition model to type the registry storage.
from app.tools.definition import ToolDefinition


# 🗂️ Define the registry class to manage available capabilities.
class ToolRegistry:
    # 🛠️ Initialize an empty registry instance.
    def __init__(self):
        # 📚 Dictionary mapping string tool names to their definitions.
        self._tools: dict[str, ToolDefinition] = {}

    # ➕ Method to add a new tool to the registry.
    def register(self, tool: ToolDefinition) -> None:
        # 🧾 Prevent duplicate registration to keep the capability map clean.
        # ⚖️ Check if the tool name is already present in the dictionary.
        if tool.name in self._tools:
            # 🚫 Raise a ValueError to strictly reject duplicate names.
            raise ValueError(f"Tool already registered: {tool.name}")

        # 💾 Store the new tool definition in the dictionary.
        self._tools[tool.name] = tool

    # 🔎 Method to retrieve a specific tool definition by name.
    def get(self, name: str) -> ToolDefinition:
        # 🔎 Fetch a tool by name or raise a clear error when missing.
        # ⚖️ Check if the requested name exists in the dictionary.
        if name not in self._tools:
            # 🚫 Raise a KeyError if the caller requested an unknown tool.
            raise KeyError(f"Tool not found: {name}")

        # 🔄 Return the matched ToolDefinition object.
        return self._tools[name]

    # 📜 Method to return all tools currently available.
    def list_tools(self) -> list[ToolDefinition]:
        # 📜 Return all registered tools in insertion order.
        # 🔄 Extract values from the dictionary and cast to a list.
        return list(self._tools.values())