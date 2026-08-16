from app.models.tool_call import ToolCall


def test_tool_call_creation():
    tool_call = ToolCall(
        id="call-1",
        action_id="action-1",
        tool_name="read_file",
        arguments={
            "path": "app/main.py",
        },
    )

    assert tool_call.tool_name == "read_file"
    assert tool_call.arguments["path"] == "app/main.py"