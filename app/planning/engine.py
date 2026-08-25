# 📦 Import Intent model from app.intent.models
from app.intent.models import Intent
# 📦 Import ToolCall model from app.models.tool_call
from app.models.tool_call import ToolCall
# 📦 Import PlanCompiler from app.planning.compiler
from app.planning.compiler import PlanCompiler
# 📦 Import Planner from app.planning.planner
from app.planning.planner import Planner
# 🈳 Blank line
# 🈳 Blank line

# ⚙️ Define PlanningEngine class to orchestrate planning and compilation
class PlanningEngine:
    # ⚙️ Initialize PlanningEngine with Planner and PlanCompiler
    def __init__(
        # ⚙️ Pass self reference
        self,
        # 🗺️ Pass the Planner instance
        planner: Planner,
        # ⚙️ Pass the PlanCompiler instance
        compiler: PlanCompiler,
    # ⚙️ End of parameters
    ):
        # 🔗 Store the planner instance variable
        self.planner = planner
        # 🔗 Store the compiler instance variable
        self.compiler = compiler
# 🈳 Blank line

    # ⚙️ Define compile_intent method to convert Intent into list of ToolCalls
    def compile_intent(
        # ⚙️ Pass self reference
        self,
        # 🎯 Pass the Intent object to compile
        intent: Intent,
    # ⚙️ Return a list of ToolCall objects
    ) -> list[ToolCall]:
        # 🗺️ Use the planner to build a plan from the intent
        plan = self.planner.build(intent)
# 🈳 Blank line

        # ⚙️ Return a list comprehension compiling each action
        return [
            # ⚙️ Compile individual action into a ToolCall
            self.compiler.compile(action)
            # ⚙️ Iterate over actions in the generated plan
            for action in plan.actions
        # ⚙️ Close list comprehension
        ]