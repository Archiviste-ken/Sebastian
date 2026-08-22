from app.models.tool_call import ToolCall
from app.security.safety import ToolSafety


def test_valid_tool_call_is_safe():
    safety = ToolSafety()

    call = ToolCall(
        tool_name="hello",
        arguments={"name": "Shreyesh"},
    )

    decision = safety.check(call)

    assert decision.safe is True


def test_empty_tool_name_is_unsafe():
    safety = ToolSafety()

    call = ToolCall(
        tool_name="   ",
        arguments={},
    )

    decision = safety.check(call)

    assert decision.safe is False
    assert decision.reason == "Tool name cannot be empty."