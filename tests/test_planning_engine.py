from app.intent.models import Intent
from app.planning.compiler import PlanCompiler
from app.planning.engine import PlanningEngine
from app.planning.planner import Planner
from app.planning.selector import CapabilitySelector
from app.tools.definition import ToolDefinition
from app.tools.registry import ToolRegistry


def fake_hello(name: str):
    return f"Hello {name}"


def test_planning_engine_compiles_intent_to_tool_call():
    registry = ToolRegistry()

    registry.register(
        ToolDefinition(
            name="read_file",
            description="Read a file.",
            handler=fake_hello,
        )
    )

    planner = Planner(
        selector=CapabilitySelector(),
    )

    compiler = PlanCompiler(
        registry=registry,
    )

    engine = PlanningEngine(
        planner=planner,
        compiler=compiler,
    )

    intent = Intent(
        goal="Read README.md",
        constraints=[],
        expected_outcome="Return the README contents.",
        forbidden_actions=[],
        missing_information=[],
        required_permissions=["filesystem"],
        success_criteria=[
            "README contents are returned.",
        ],
    )

    tool_calls = engine.compile_intent(intent)

    assert len(tool_calls) == 1
    assert tool_calls[0].tool_name == "read_file"