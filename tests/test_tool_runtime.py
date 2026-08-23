# 🧪 Tool runtime tests
# Verifies the runtime normalizes both successful tool calls and failures into a consistent result object.

from app.models.tool_result import ToolResult, ToolResultStatus
from app.tools.definition import ToolDefinition
from app.tools.runtime import ToolRuntime


def hello(name: str):
    return f"Hello {name}"


def test_runtime_executes_tool():
    tool = ToolDefinition(
        name="hello",
        description="Say hello",
        handler=hello,
    )

    runtime = ToolRuntime()

    result = runtime.execute(tool, "Shreyesh")

    assert isinstance(result, ToolResult)
    assert result.status == ToolResultStatus.SUCCESS
    assert result.success is True
    assert result.data == "Hello Shreyesh"
    assert result.error is None


def broken_tool():
    raise RuntimeError("Something went wrong")


def test_runtime_converts_exception_to_failure():
    tool = ToolDefinition(
        name="broken",
        description="Always fails",
        handler=broken_tool,
    )

    runtime = ToolRuntime()

    result = runtime.execute(tool)

    assert result.status == ToolResultStatus.FAILED
    assert result.success is False
    assert result.data is None
    assert result.error == "Something went wrong"