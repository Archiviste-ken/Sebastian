from pathlib import Path

from app.models.tool_call import ToolCall
from app.models.tool_result import ToolResultStatus
from app.security.permissions import PermissionKernel, PermissionLevel
from app.security.safety import ToolSafety
from app.tools.audit import AuditRecorder
from app.tools.builtin.filesystem import read_file
from app.tools.context import ExecutionContext
from app.tools.definition import ToolDefinition
from app.tools.executor import ToolExecutor
from app.tools.registry import ToolRegistry
from app.tools.runtime import ToolRuntime


def build_executor(
    workspace: Path,
    permission_level: PermissionLevel,
) -> ToolExecutor:
    registry = ToolRegistry()

    registry.register(
        ToolDefinition(
            name="read_file",
            description="Read a text file.",
            handler=read_file,
        )
    )

    context = ExecutionContext(
        workspace=workspace,
    )

    return ToolExecutor(
        registry=registry,
        permission_kernel=PermissionKernel(
            {
                "read_file": permission_level,
            }
        ),
        safety=ToolSafety(
            workspace=workspace,
        ),
        runtime=ToolRuntime(),
        audit_recorder=AuditRecorder(),
        context=context,
    )


def test_phase1_allowed_execution(tmp_path: Path):
    file_path = tmp_path / "hello.txt"

    file_path.write_text(
        "Sebastian Phase 1",
        encoding="utf-8",
    )

    executor = build_executor(
        workspace=tmp_path,
        permission_level=PermissionLevel.AUTONOMOUS,
    )

    result = executor.execute(
        ToolCall(
            tool_name="read_file",
            arguments={
                "path": str(file_path),
            },
        )
    )

    assert result.status == ToolResultStatus.SUCCESS
    assert result.success is True
    assert result.data == "Sebastian Phase 1"

    events = executor.audit_recorder.events()

    assert len(events) == 1
    assert events[0].tool_name == "read_file"
    assert events[0].success is True


def test_phase1_blocked_execution(tmp_path: Path):
    file_path = tmp_path / "secret.txt"

    file_path.write_text(
        "secret",
        encoding="utf-8",
    )

    executor = build_executor(
        workspace=tmp_path,
        permission_level=PermissionLevel.BLOCKED,
    )

    result = executor.execute(
        ToolCall(
            tool_name="read_file",
            arguments={
                "path": str(file_path),
            },
        )
    )

    assert result.status == ToolResultStatus.BLOCKED
    assert result.success is False
    assert result.error == "Tool is blocked."

    events = executor.audit_recorder.events()

    assert len(events) == 1
    assert events[0].tool_name == "read_file"
    assert events[0].success is False