from app.intent.models import Intent
from app.models.tool_call import ToolCall
from app.planning.argument_resolver import ArgumentResolver
from app.planning.compiler import PlanCompiler
from app.planning.planner import Planner
from app.tools.registry import ToolRegistry


class PlanningEngine:
    def __init__(
        self,
        planner: Planner,
        compiler: PlanCompiler,
        argument_resolver: ArgumentResolver,
        registry: ToolRegistry,
    ):
        self.planner = planner
        self.compiler = compiler
        self.argument_resolver = argument_resolver
        self.registry = registry

    def compile_intent(
        self,
        intent: Intent,
    ) -> list[ToolCall]:
        plan = self.planner.build(intent)

        tool_calls: list[ToolCall] = []

        for action in plan.actions:
            tool = self.registry.get(action.tool)

            resolved_arguments = self.argument_resolver.resolve(
                intent=intent,
                tool=tool,
            )

            action_with_arguments = action.model_copy(
                update={
                    "arguments": resolved_arguments,
                }
            )

            tool_call = self.compiler.compile(
                action_with_arguments,
            )

            tool_calls.append(tool_call)

        return tool_calls