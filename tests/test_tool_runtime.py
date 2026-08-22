from app.models.tool_result import ToolResult
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
    assert result.success is True
    assert result.data == "Hello Shreyesh"
    assert result.error is None