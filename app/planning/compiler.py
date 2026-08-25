# 📦 Import ToolCall model from app.models.tool_call
from app.models.tool_call import ToolCall
# 📦 Import Action model from app.planning.models
from app.planning.models import Action
# 📦 Import ToolRegistry from app.tools.registry
from app.tools.registry import ToolRegistry
# 🈳 Blank line
# 🈳 Blank line

# ⚙️ Define PlanCompiler class to turn plans into tool calls
class PlanCompiler:
    # ⚙️ Initialize PlanCompiler with a ToolRegistry
    def __init__(self, registry: ToolRegistry):
        # 🔗 Store the registry instance variable
        self.registry = registry
# 🈳 Blank line

    # ⚙️ Define compile method to convert Action to ToolCall
    def compile(self, action: Action) -> ToolCall:
        # 🧰 Only registered tools can become executable ToolCalls.
        try:
            # 🔍 Attempt to get the tool from the registry
            self.registry.get(action.tool)
        # 🛑 Catch KeyError if the tool is not registered
        except KeyError as exc:
            # 🛑 Raise ValueError indicating the tool is unknown
            raise ValueError(
                # 🛑 Format the error message with the unknown tool name
                f"Cannot compile unknown tool: {action.tool}"
            # 🛑 Chain the original exception
            ) from exc
# 🈳 Blank line

        # ⚙️ Return a new ToolCall object
        return ToolCall(
            # ⚙️ Set the tool_name from the action's tool
            tool_name=action.tool,
            # ⚙️ Set the arguments from the action's arguments
            arguments=action.arguments,
        # ⚙️ Close ToolCall instantiation
        )