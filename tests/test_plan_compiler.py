import pytest

from app.models.tool_call import ToolCall
from app.planning.compiler import PlanCompiler
from app.planning.models import Action
from app.tools.definition import ToolDefinition
from app.tools.registry import ToolRegistry


def hello(name: str):
    return f"Hello {name}"


def build_registry() -> ToolRegistry:
    registry = ToolRegistry()

    registry.register(
        ToolDefinition(
            name="hello",
            description="Say hello.",
            handler=hello,
        )
    )

    return registry


def test_compiler_converts_action_to_tool_call():
    registry = build_registry()

    compiler = PlanCompiler(
        registry=registry,
    )

    action = Action(
        action_id="say-hello",
        tool="hello",
        arguments={
            "name": "Sebastian",
        },
        expected_result="A greeting is returned.",
        verification_method="Check the returned greeting.",
    )

    tool_call = compiler.compile(action)

    assert isinstance(tool_call, ToolCall)
    assert tool_call.tool_name == "hello"
    assert tool_call.arguments == {
        "name": "Sebastian",
    }


def test_compiler_rejects_unknown_tool():
    registry = build_registry()

    compiler = PlanCompiler(
        registry=registry,
    )

    action = Action(
        action_id="unknown",
        tool="does_not_exist",
        arguments={},
        expected_result="Something happens.",
        verification_method="Check the result.",
    )

    with pytest.raises(ValueError, match="unknown tool"):
        compiler.compile(action)