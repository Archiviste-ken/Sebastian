class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, name, tool):
        if name in self._tools:
            raise ValueError(f"Tool already registered: {name}")

        self._tools[name] = tool

    def get(self, name):
        if name not in self._tools:
            raise KeyError(f"Tool not found: {name}")

        return self._tools[name]

    def list_tools(self):
        return list(self._tools.keys())