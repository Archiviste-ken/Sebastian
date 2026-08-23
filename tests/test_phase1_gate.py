from pathlib import Path

from app.models.tool_call import ToolCall
from app.models.tool_result import ToolResultStatus
from app.security.permissions import PermissionKernel, PermissionLevel
from app.security.safety import ToolSafety
from app.tools.audit import AuditRecorder
from app.tools.builtin.command import run_command
from app.tools.builtin.filesystem import (
    create_directory,
    list_directory,
    move_file,
    read_file,
    write_file,
)
from app.tools.builtin.python import run_python
from app.tools.definition import ToolDefinition
from app.tools.executor import ToolExecutor
from app.tools.registry import ToolRegistry
from app.tools.runtime import ToolRuntime

def test_read_file_full_execution_pipeline(tmp_path: Path):
    file_path = tmp_path / "hello.txt"

    file_path.write_text(
        "Hello from Sebastian!",
        encoding="utf-8",
    )

    registry = ToolRegistry()

    registry.register(
        ToolDefinition(
            name="read_file",
            description="Read the contents of a text file.",
            handler=read_file,
        )
    )

    permission_kernel = PermissionKernel(
        {
            "read_file": PermissionLevel.AUTONOMOUS,
        }
    )

    audit_recorder = AuditRecorder()

    executor = ToolExecutor(
        registry=registry,
        permission_kernel=permission_kernel,
        safety=ToolSafety(workspace=tmp_path),
        runtime=ToolRuntime(),
        audit_recorder=audit_recorder,
    )

    result = executor.execute(
        ToolCall(
            tool_name="read_file",
            arguments={
                "path": str(file_path),
            },
        )
    )

    assert result.success is True
    assert result.data == "Hello from Sebastian!"

    events = audit_recorder.events()

    assert len(events) == 1
    assert events[0].tool_name == "read_file"
    assert events[0].success is True


def test_blocked_read_file_never_executes(tmp_path: Path):
    file_path = tmp_path / "secret.txt"

    file_path.write_text(
        "secret",
        encoding="utf-8",
    )

    registry = ToolRegistry()

    registry.register(
        ToolDefinition(
            name="read_file",
            description="Read the contents of a text file.",
            handler=read_file,
        )
    )

    permission_kernel = PermissionKernel(
        {
            "read_file": PermissionLevel.BLOCKED,
        }
    )

    audit_recorder = AuditRecorder()

    executor = ToolExecutor(
        registry=registry,
        permission_kernel=permission_kernel,
        safety=ToolSafety(workspace=tmp_path),
        runtime=ToolRuntime(),
        audit_recorder=audit_recorder,
    )

    result = executor.execute(
        ToolCall(
            tool_name="read_file",
            arguments={
                "path": str(file_path),
            },
        )
    )

    assert result.success is False
    assert result.error == "Tool is blocked."

    events = audit_recorder.events()

    assert len(events) == 1
    assert events[0].tool_name == "read_file"
    assert events[0].success is False


def test_read_file_outside_workspace_is_rejected(tmp_path: Path):
    workspace_file = tmp_path / "workspace.txt"
    outside_file = tmp_path.parent / "outside.txt"

    workspace_file.write_text(
        "inside workspace",
        encoding="utf-8",
    )

    outside_file.write_text(
        "outside workspace",
        encoding="utf-8",
    )

    registry = ToolRegistry()

    registry.register(
        ToolDefinition(
            name="read_file",
            description="Read the contents of a text file.",
            handler=read_file,
        )
    )

    permission_kernel = PermissionKernel(
        {
            "read_file": PermissionLevel.AUTONOMOUS,
        }
    )

    audit_recorder = AuditRecorder()

    executor = ToolExecutor(
        registry=registry,
        permission_kernel=permission_kernel,
        safety=ToolSafety(workspace=tmp_path),
        runtime=ToolRuntime(),
        audit_recorder=audit_recorder,
    )

    result = executor.execute(
        ToolCall(
            tool_name="read_file",
            arguments={
                "path": str(outside_file),
            },
        )
    )

    assert result.success is False
    assert result.error == "Path is outside the allowed workspace."

    events = audit_recorder.events()

    assert len(events) == 1
    assert events[0].tool_name == "read_file"
    assert events[0].success is False
    
def test_create_directory_requires_approval(tmp_path: Path):
    directory_path = tmp_path / "data" / "reports"

    registry = ToolRegistry()

    registry.register(
        ToolDefinition(
            name="create_directory",
            description="Create a directory.",
            handler=create_directory,
        )
    )

    permission_kernel = PermissionKernel(
        {
            "create_directory": PermissionLevel.APPROVAL,
        }
    )

    audit_recorder = AuditRecorder()

    executor = ToolExecutor(
        registry=registry,
        permission_kernel=permission_kernel,
        safety=ToolSafety(workspace=tmp_path),
        runtime=ToolRuntime(),
        audit_recorder=audit_recorder,
    )

    result = executor.execute(
        ToolCall(
            tool_name="create_directory",
            arguments={
                "path": str(directory_path),
            },
        )
    )

    assert result.success is False
    assert result.error == "User approval is required."

    # 🚨 Most important:
    # Permission must prevent the side effect.
    assert directory_path.exists() is False

    events = audit_recorder.events()

    assert len(events) == 1
    assert events[0].tool_name == "create_directory"
    assert events[0].success is False
    
def test_move_file_requires_approval(tmp_path: Path):
    source = tmp_path / "draft.txt"
    destination = tmp_path / "final.txt"

    source.write_text(
        "Important draft",
        encoding="utf-8",
    )

    registry = ToolRegistry()

    registry.register(
        ToolDefinition(
            name="move_file",
            description="Move a file to another path.",
            handler=move_file,
        )
    )

    permission_kernel = PermissionKernel(
        {
            "move_file": PermissionLevel.APPROVAL,
        }
    )

    audit_recorder = AuditRecorder()

    executor = ToolExecutor(
        registry=registry,
        permission_kernel=permission_kernel,
        safety=ToolSafety(workspace=tmp_path),
        runtime=ToolRuntime(),
        audit_recorder=audit_recorder,
    )

    result = executor.execute(
        ToolCall(
            tool_name="move_file",
            arguments={
                "source": str(source),
                "destination": str(destination),
            },
        )
    )

    assert result.success is False
    assert result.error == "User approval is required."

    # 🛑 The move must NOT have happened.
    assert source.exists() is True
    assert destination.exists() is False

    events = audit_recorder.events()

    assert len(events) == 1
    assert events[0].tool_name == "move_file"
    assert events[0].success is False
    
    
def test_move_file_autonomous_execution(tmp_path: Path):
    source = tmp_path / "draft.txt"
    destination = tmp_path / "final.txt"

    source.write_text(
        "Important content",
        encoding="utf-8",
    )

    registry = ToolRegistry()

    registry.register(
        ToolDefinition(
            name="move_file",
            description="Move a file to another path.",
            handler=move_file,
        )
    )

    permission_kernel = PermissionKernel(
        {
            "move_file": PermissionLevel.AUTONOMOUS,
        }
    )

    audit_recorder = AuditRecorder()

    executor = ToolExecutor(
        registry=registry,
        permission_kernel=permission_kernel,
        safety=ToolSafety(workspace=tmp_path),
        runtime=ToolRuntime(),
        audit_recorder=audit_recorder,
    )

    result = executor.execute(
        ToolCall(
            tool_name="move_file",
            arguments={
                "source": str(source),
                "destination": str(destination),
            },
        )
    )

    assert result.success is True

    assert source.exists() is False
    assert destination.exists() is True

    assert destination.read_text(encoding="utf-8") == (
        "Important content"
    )

    events = audit_recorder.events()

    assert len(events) == 1
    assert events[0].tool_name == "move_file"
    assert events[0].success is True
    
    
def test_run_command_requires_approval():
    from app.tools.builtin.command import run_command

    registry = ToolRegistry()

    registry.register(
        ToolDefinition(
            name="run_command",
            description="Run an approved command.",
            handler=run_command,
        )
    )

    permission_kernel = PermissionKernel(
        {
            "run_command": PermissionLevel.APPROVAL,
        }
    )

    audit_recorder = AuditRecorder()

    executor = ToolExecutor(
        registry=registry,
        permission_kernel=permission_kernel,
        safety=ToolSafety(),
        runtime=ToolRuntime(),
        audit_recorder=audit_recorder,
    )

    result = executor.execute(
        ToolCall(
            tool_name="run_command",
            arguments={
                "command": [
                    "python",
                    "-c",
                    "raise SystemExit('SHOULD NOT RUN')",
                ],
            },
        )
    )

    assert result.success is False
    assert result.error == "User approval is required."

    events = audit_recorder.events()

    assert len(events) == 1
    assert events[0].tool_name == "run_command"
    assert events[0].success is False

def test_run_command_unknown_executable_is_rejected():
    from app.tools.builtin.command import run_command

    registry = ToolRegistry()

    registry.register(
        ToolDefinition(
            name="run_command",
            description="Run an approved command.",
            handler=run_command,
        )
    )

    permission_kernel = PermissionKernel(
        {
            "run_command": PermissionLevel.AUTONOMOUS,
        }
    )

    audit_recorder = AuditRecorder()

    executor = ToolExecutor(
        registry=registry,
        permission_kernel=permission_kernel,
        safety=ToolSafety(),
        runtime=ToolRuntime(),
        audit_recorder=audit_recorder,
    )

    result = executor.execute(
        ToolCall(
            tool_name="run_command",
            arguments={
                "command": [
                    "definitely_not_allowed",
                    "whatever",
                ],
            },
        )
    )

    assert result.success is False
    assert result.error == (
        "Command is not allowed: definitely_not_allowed"
    )

    events = audit_recorder.events()

    assert len(events) == 1
    assert events[0].tool_name == "run_command"
    assert events[0].success is False
    
    
def test_run_command_autonomous_execution():
    from app.tools.builtin.command import run_command

    registry = ToolRegistry()

    registry.register(
        ToolDefinition(
            name="run_command",
            description="Run an approved command.",
            handler=run_command,
        )
    )

    permission_kernel = PermissionKernel(
        {
            "run_command": PermissionLevel.AUTONOMOUS,
        }
    )

    audit_recorder = AuditRecorder()

    executor = ToolExecutor(
        registry=registry,
        permission_kernel=permission_kernel,
        safety=ToolSafety(),
        runtime=ToolRuntime(),
        audit_recorder=audit_recorder,
    )

    result = executor.execute(
        ToolCall(
            tool_name="run_command",
            arguments={
                "command": [
                    "python",
                    "-c",
                    "print('Sebastian command works')",
                ],
            },
        )
    )

    assert result.success is True

    assert result.data["return_code"] == 0
    assert result.data["stdout"].strip() == (
        "Sebastian command works"
    )
    assert result.data["stderr"] == ""

    events = audit_recorder.events()

    assert len(events) == 1
    assert events[0].tool_name == "run_command"
    assert events[0].success is True


def test_run_python_requires_approval(tmp_path: Path):
    script = tmp_path / "should_not_run.py"

    script.write_text(
        "raise SystemExit('PYTHON SHOULD NOT RUN')",
        encoding="utf-8",
    )

    registry = ToolRegistry()

    registry.register(
        ToolDefinition(
            name="run_python",
            description="Run a Python script.",
            handler=run_python,
        )
    )

    permission_kernel = PermissionKernel(
        {
            "run_python": PermissionLevel.APPROVAL,
        }
    )

    audit_recorder = AuditRecorder()

    executor = ToolExecutor(
        registry=registry,
        permission_kernel=permission_kernel,
        safety=ToolSafety(workspace=tmp_path),
        runtime=ToolRuntime(),
        audit_recorder=audit_recorder,
    )

    result = executor.execute(
        ToolCall(
            tool_name="run_python",
            arguments={
                "script": str(script),
            },
        )
    )

    assert result.status == ToolResultStatus.WAITING_APPROVAL
    assert result.success is False
    assert result.error == "User approval is required."

    events = audit_recorder.events()

    assert len(events) == 1
    assert events[0].tool_name == "run_python"
    assert events[0].success is False

def test_run_python_autonomous_execution(tmp_path: Path):
    script = tmp_path / "hello.py"

    script.write_text(
        "print('Hello from Sebastian Python!')",
        encoding="utf-8",
    )

    registry = ToolRegistry()

    registry.register(
        ToolDefinition(
            name="run_python",
            description="Run a Python script.",
            handler=run_python,
        )
    )

    permission_kernel = PermissionKernel(
        {
            "run_python": PermissionLevel.AUTONOMOUS,
        }
    )

    audit_recorder = AuditRecorder()

    executor = ToolExecutor(
        registry=registry,
        permission_kernel=permission_kernel,
        safety=ToolSafety(workspace=tmp_path),
        runtime=ToolRuntime(),
        audit_recorder=audit_recorder,
    )

    result = executor.execute(
        ToolCall(
            tool_name="run_python",
            arguments={
                "script": str(script),
            },
        )
    )

    assert result.status == ToolResultStatus.SUCCESS
    assert result.success is True
    assert result.data["return_code"] == 0
    assert result.data["stdout"].strip() == (
        "Hello from Sebastian Python!"
    )

    events = audit_recorder.events()

    assert len(events) == 1
    assert events[0].tool_name == "run_python"
    assert events[0].success is True