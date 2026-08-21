import pytest

from app.tools.registry import ToolRegistry


def hello():
    return "Hello from Sebastian"


def goodbye():
    return "Goodbye from Sebastian"


def test_register_and_get_tool():
    registry = ToolRegistry()

    registry.register("hello", hello)

    assert registry.get("hello") is hello


def test_unknown_tool_raises_error():
    registry = ToolRegistry()

    with pytest.raises(KeyError):
        registry.get("does_not_exist")


def test_duplicate_tool_registration_raises_error():
    registry = ToolRegistry()

    registry.register("hello", hello)

    with pytest.raises(ValueError):
        registry.register("hello", goodbye)


def test_list_tools():
    registry = ToolRegistry()

    registry.register("hello", hello)
    registry.register("goodbye", goodbye)

    assert registry.list_tools() == ["hello", "goodbye"]