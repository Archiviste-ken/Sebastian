from pathlib import Path

from app.models.tool_call import ToolCall
from app.security.permissions import PermissionKernel, PermissionLevel
from app.security.safety import ToolSafety
from app.tools.audit import AuditRecorder
from app.tools.builtin.filesystem import read_file
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