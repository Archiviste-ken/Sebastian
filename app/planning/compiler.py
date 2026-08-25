from app.models.tool_call import ToolCall
from app.planning.models import Action
from app.tools.registry import ToolRegistry


class PlanCompiler:
    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def compile(self, action: Action) -> ToolCall:
        # 🧰 Only registered tools can become executable ToolCalls.
        try:
            self.registry.get(action.tool)
        except KeyError as exc:
            raise ValueError(
                f"Cannot compile unknown tool: {action.tool}"
            ) from exc

        return ToolCall(
            tool_name=action.tool,
            arguments=action.arguments,
        )