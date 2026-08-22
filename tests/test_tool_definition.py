# 🧪 Tool definition tests
# Validates the metadata and callable handler behind each registered tool.

from app.tools.definition import ToolDefinition


def hello(name: str):
    return f"Hello {name}"


def test_tool_definition():
    tool = ToolDefinition(
        name="hello",
        description="Say hello to a person",
        handler=hello,
    )

    assert tool.name == "hello"
    assert tool.description == "Say hello to a person"
    assert tool.handler is hello


def test_tool_handler_is_callable():
    tool = ToolDefinition(
        name="hello",
        description="Say hello to a person",
        handler=hello,
    )

    result = tool.handler("Shreyesh")

    assert result == "Hello Shreyesh"