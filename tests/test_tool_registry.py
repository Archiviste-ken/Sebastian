from app.tools.definition import ToolDefinition
from app.tools.registry import ToolRegistry


def hello():
    return "Hello from Sebastian"


def goodbye():
    return "Goodbye from Sebastian"


def make_hello_tool():
    return ToolDefinition(
        name="hello",
        description="Say hello",
        handler=hello,
    )


def make_goodbye_tool():
    return ToolDefinition(
        name="goodbye",
        description="Say goodbye",
        handler=goodbye,
    )


def test_register_and_get_tool():
    registry = ToolRegistry()

    tool = make_hello_tool()

    registry.register(tool)

    result = registry.get("hello")

    assert result is tool


def test_unknown_tool_raises_error():
    registry = ToolRegistry()

    try:
        registry.get("does_not_exist")
        assert False
    except KeyError:
        pass


def test_duplicate_tool_registration_raises_error():
    registry = ToolRegistry()

    registry.register(make_hello_tool())

    try:
        registry.register(make_hello_tool())
        assert False
    except ValueError:
        pass


def test_list_tools():
    registry = ToolRegistry()

    hello_tool = make_hello_tool()
    goodbye_tool = make_goodbye_tool()

    registry.register(hello_tool)
    registry.register(goodbye_tool)

    tools = registry.list_tools()

    assert tools == [hello_tool, goodbye_tool]