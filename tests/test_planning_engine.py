from app.intent.models import Intent
from app.llm.gateway import ModelResponse
from app.planning.argument_resolver import ArgumentResolver
from app.planning.compiler import PlanCompiler
from app.planning.engine import PlanningEngine
from app.planning.planner import Planner
from app.planning.selector import CapabilitySelector
from app.tools.definition import ToolDefinition
from app.tools.registry import ToolRegistry


def fake_read_file(path: str):
    return path


class FakeGateway:
    def generate(
        self,
        messages,
        response_format=None,
    ):
        return ModelResponse(
            content=(
                "{"
                '"tool_name":"read_file",'
                '"arguments":{"path":"README.md"}'
                "}"
            )
        )


def test_planning_engine_compiles_intent_to_tool_call():
    registry = ToolRegistry()

    registry.register(
        ToolDefinition(
            name="read_file",
            description="Read a file.",
            handler=fake_read_file,
            argument_schema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                    },
                },
                "required": ["path"],
                "additionalProperties": False,
            },
        )
    )

    gateway = FakeGateway()

    planner = Planner(
        selector=CapabilitySelector(),
    )

    compiler = PlanCompiler(
        registry=registry,
    )

    argument_resolver = ArgumentResolver(
        gateway=gateway,
    )

    engine = PlanningEngine(
        planner=planner,
        compiler=compiler,
        argument_resolver=argument_resolver,
        registry=registry,
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

    tool_calls = engine.compile_intent(
        intent,
    )

    assert len(tool_calls) == 1

    call = tool_calls[0]

    assert call.tool_name == "read_file"
    assert call.arguments == {
        "path": "README.md",
    }
    
def test_planning_engine_rejects_missing_required_argument():
    class EmptyArgumentGateway:
        def generate(
            self,
            messages,
            response_format=None,
        ):
            return ModelResponse(
                content=(
                    "{"
                    '"tool_name":"read_file",'
                    '"arguments":{}'
                    "}"
                )
            )

    registry = ToolRegistry()

    registry.register(
        ToolDefinition(
            name="read_file",
            description="Read a file.",
            handler=fake_read_file,
            argument_schema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                    },
                },
                "required": ["path"],
                "additionalProperties": False,
            },
        )
    )

    engine = PlanningEngine(
        planner=Planner(
            selector=CapabilitySelector(),
        ),
        compiler=PlanCompiler(
            registry=registry,
        ),
        argument_resolver=ArgumentResolver(
            gateway=EmptyArgumentGateway(),
        ),
        registry=registry,
    )

    intent = Intent(
        goal="Read a file.",
        constraints=[],
        expected_outcome="Return its contents.",
        forbidden_actions=[],
        missing_information=[],
        required_permissions=["filesystem"],
        success_criteria=[
            "File contents are returned.",
        ],
    )

    try:
        engine.compile_intent(intent)
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Missing required arguments should not compile."
        )