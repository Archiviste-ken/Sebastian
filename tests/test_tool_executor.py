from app.models.tool_call import ToolCall
from app.models.tool_result import ToolResult
from app.security.permissions import PermissionKernel, PermissionLevel
from app.security.safety import SafetyDecision, ToolSafety
from app.tools.definition import ToolDefinition
from app.tools.executor import ToolExecutor
from app.tools.registry import ToolRegistry
from app.tools.runtime import ToolRuntime


def hello(name: str):
    return f"Hello {name}"


def make_executor(permission_level: PermissionLevel):
    registry = ToolRegistry()

    registry.register(
        ToolDefinition(
            name="hello",
            description="Say hello",
            handler=hello,
        )
    )

    permission_kernel = PermissionKernel(
        {
            "hello": permission_level,
        }
    )

    safety = ToolSafety()
    runtime = ToolRuntime()

    return ToolExecutor(
        registry=registry,
        permission_kernel=permission_kernel,
        safety=safety,
        runtime=runtime,
    )


def test_autonomous_tool_executes():
    executor = make_executor(PermissionLevel.AUTONOMOUS)

    call = ToolCall(
        tool_name="hello",
        arguments={"name": "Shreyesh"},
    )

    result = executor.execute(call)

    assert isinstance(result, ToolResult)
    assert result.success is True
    assert result.data == "Hello Shreyesh"


def test_approval_tool_does_not_execute():
    executor = make_executor(PermissionLevel.APPROVAL)

    call = ToolCall(
        tool_name="hello",
        arguments={"name": "Shreyesh"},
    )

    result = executor.execute(call)

    assert result.success is False
    assert result.error == "User approval is required."


def test_blocked_tool_does_not_execute():
    executor = make_executor(PermissionLevel.BLOCKED)

    call = ToolCall(
        tool_name="hello",
        arguments={"name": "Shreyesh"},
    )

    result = executor.execute(call)

    assert result.success is False
    assert result.error == "Tool is blocked."


def test_unknown_tool_does_not_execute():
    registry = ToolRegistry()

    permission_kernel = PermissionKernel({})
    safety = ToolSafety()
    runtime = ToolRuntime()

    executor = ToolExecutor(
        registry=registry,
        permission_kernel=permission_kernel,
        safety=safety,
        runtime=runtime,
    )

    call = ToolCall(
        tool_name="does_not_exist",
        arguments={},
    )

    result = executor.execute(call)

    assert result.success is False
    assert "Tool not found" in result.error


class ExplodingTool:
    def __call__(self):
        raise AssertionError("Tool should never have executed")


def test_unsafe_tool_call_does_not_execute():
    registry = ToolRegistry()

    registry.register(
        ToolDefinition(
            name="hello",
            description="Say hello",
            handler=ExplodingTool(),
        )
    )

    permission_kernel = PermissionKernel(
        {
            "hello": PermissionLevel.AUTONOMOUS,
        }
    )

    class UnsafeSafety:
        def check(self, tool_call):
            return SafetyDecision(
                safe=False,
                reason="Unsafe tool call.",
            )

    runtime = ToolRuntime()

    executor = ToolExecutor(
        registry=registry,
        permission_kernel=permission_kernel,
        safety=UnsafeSafety(),
        runtime=runtime,
    )

    call = ToolCall(
        tool_name="hello",
        arguments={},
    )

    result = executor.execute(call)

    assert result.success is False
    assert result.error == "Unsafe tool call."