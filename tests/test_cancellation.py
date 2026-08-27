import pytest
from pathlib import Path

from app.checkpoint.store import CheckpointStore
from app.execution.action_executor import ActionExecutor
from app.planning.models import Action, Plan
from app.recovery.engine import RecoveryEngine
from app.security.permissions import PermissionKernel, PermissionLevel
from app.security.safety import ToolSafety
from app.tools.audit import AuditRecorder
from app.tools.builtin.filesystem import read_file
from app.tools.context import ExecutionContext
from app.tools.definition import ToolDefinition
from app.tools.executor import ToolExecutor
from app.tools.registry import ToolRegistry
from app.tools.runtime import ToolRuntime
from app.verification.engine import VerificationEngine


def _executor(tmp_path):
    registry = ToolRegistry()
    registry.register(ToolDefinition(
        name="read_file", description="Read", handler=read_file,
        argument_schema={"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]},
    ))
    return ToolExecutor(
        registry=registry,
        permission_kernel=PermissionKernel({"read_file": PermissionLevel.AUTONOMOUS}),
        safety=ToolSafety(workspace=tmp_path),
        runtime=ToolRuntime(),
        audit_recorder=AuditRecorder(),
        context=ExecutionContext(workspace=tmp_path),
    )


def _plan(*actions):
    return Plan(goal="test", actions=list(actions), success_criteria=["ok"])


def _action(aid, path):
    return Action(
        action_id=aid, tool="read_file", arguments={"path": path},
        expected_result="r", verification_method="v",
    )


def test_cancel_prevents_execution(tmp_path):
    ae = ActionExecutor(
        tool_executor=_executor(tmp_path),
        verification_engine=VerificationEngine(),
        recovery_engine=RecoveryEngine(),
        checkpoint_store=CheckpointStore(),
    )
    ae.cancel("t-1")
    report = ae.execute_plan("t-1", _plan(_action("a", "x")), tmp_path)
    assert report.cancelled
    assert report.actions_completed == 0


def test_cancel_does_not_affect_other_tasks(tmp_path):
    (tmp_path / "f.txt").write_text("ok")
    ae = ActionExecutor(
        tool_executor=_executor(tmp_path),
        verification_engine=VerificationEngine(),
        recovery_engine=RecoveryEngine(),
        checkpoint_store=CheckpointStore(),
    )
    ae.cancel("other")
    report = ae.execute_plan("mine", _plan(_action("a", str(tmp_path / "f.txt"))), tmp_path)
    assert not report.cancelled
    assert report.success


def test_cancelled_checkpoint_status(tmp_path):
    store = CheckpointStore()
    ae = ActionExecutor(
        tool_executor=_executor(tmp_path),
        verification_engine=VerificationEngine(),
        recovery_engine=RecoveryEngine(),
        checkpoint_store=store,
    )
    ae.cancel("t-2")
    ae.execute_plan("t-2", _plan(_action("a", "x")), tmp_path)
    state = store.load("t-2")
    assert state is not None
    assert state.status == "cancelled"
