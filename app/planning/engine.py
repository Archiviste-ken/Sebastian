from app.intent.models import Intent
from app.models.tool_call import ToolCall
from app.planning.compiler import PlanCompiler
from app.planning.planner import Planner


class PlanningEngine:
    def __init__(
        self,
        planner: Planner,
        compiler: PlanCompiler,
    ):
        self.planner = planner
        self.compiler = compiler

    def compile_intent(
        self,
        intent: Intent,
    ) -> list[ToolCall]:
        plan = self.planner.build(intent)

        return [
            self.compiler.compile(action)
            for action in plan.actions
        ]