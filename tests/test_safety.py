from pathlib import Path

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


def test_read_file_inside_workspace_is_safe(tmp_path: Path):
    safety = ToolSafety(workspace=tmp_path)

    call = ToolCall(
        tool_name="read_file",
        arguments={
            "path": "project/hello.txt",
        },
    )

    decision = safety.check(call)

    assert decision.safe is True


def test_read_file_outside_workspace_is_unsafe(tmp_path: Path):
    safety = ToolSafety(workspace=tmp_path)

    call = ToolCall(
        tool_name="read_file",
        arguments={
            "path": "../secret.txt",
        },
    )

    decision = safety.check(call)

    assert decision.safe is False
    assert decision.reason == "Path is outside the allowed workspace."
    
def test_move_file_destination_outside_workspace_is_unsafe(tmp_path):
    safety = ToolSafety(workspace=tmp_path)

    call = ToolCall(
        tool_name="move_file",
        arguments={
            "source": "draft.txt",
            "destination": "../outside.txt",
        },
    )

    decision = safety.check(call)

    assert decision.safe is False
    assert decision.reason == "Path is outside the allowed workspace."
    
    
def test_run_command_allowed_executable():
    safety = ToolSafety()

    call = ToolCall(
        tool_name="run_command",
        arguments={
            "command": ["python", "-c", "print('hello')"],
        },
    )

    decision = safety.check(call)

    assert decision.safe is True
    
def test_run_command_blocks_unknown_executable():
    safety = ToolSafety()

    call = ToolCall(
        tool_name="run_command",
        arguments={
            "command": ["definitely_not_allowed", "--do-something"],
        },
    )

    decision = safety.check(call)

    assert decision.safe is False
    assert decision.reason == (
        "Command is not allowed: definitely_not_allowed"
    )
    
def test_run_command_requires_command_list():
    safety = ToolSafety()

    call = ToolCall(
        tool_name="run_command",
        arguments={},
    )

    decision = safety.check(call)

    assert decision.safe is False
    assert decision.reason == (
        "run_command requires a non-empty command list."
    )

def test_run_python_inside_workspace_is_safe(tmp_path):
    safety = ToolSafety(workspace=tmp_path)

    call = ToolCall(
        tool_name="run_python",
        arguments={
            "script": "scripts/hello.py",
        },
    )

    decision = safety.check(call)

    assert decision.safe is True
    
def test_run_python_outside_workspace_is_unsafe(tmp_path):
    safety = ToolSafety(workspace=tmp_path)

    call = ToolCall(
        tool_name="run_python",
        arguments={
            "script": "../hello.py",
        },
    )

    decision = safety.check(call)

    assert decision.safe is False
    assert decision.reason == (
        "Python script is outside the allowed workspace."
    )
    
def test_run_python_requires_python_file(tmp_path):
    safety = ToolSafety(workspace=tmp_path)

    call = ToolCall(
        tool_name="run_python",
        arguments={
            "script": "hello.txt",
        },
    )

    decision = safety.check(call)

    assert decision.safe is False
    assert decision.reason == (
        "run_python requires a .py script."
    )