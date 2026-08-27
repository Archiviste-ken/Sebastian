import pytest
from pathlib import Path

from app.checkpoint.store import CheckpointStore
from app.execution.action_executor import ActionExecutor
from app.execution.models import ExecutionReport
from app.models.tool_result import ToolResult, ToolResultStatus
from app.planning.models import Action, ActionRisk, Plan, RetryPolicy
from app.recovery.engine import RecoveryEngine
from app.security.permissions import PermissionKernel, PermissionLevel
from app.security.safety import ToolSafety
from app.tools.audit import AuditRecorder
from app.tools.builtin.filesystem import read_file, list_directory
from app.tools.context import ExecutionContext
from app.tools.definition import ToolDefinition
from app.tools.executor import ToolExecutor
from app.tools.registry import ToolRegistry
from app.tools.runtime import ToolRuntime
from app.verification.engine import VerificationEngine


def _build_tool_executor(tmp_path):
    registry = ToolRegistry()
    registry.register(ToolDefinition(
        name="read_file", description="Read file", handler=read_file,
        argument_schema={"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]},
    ))
    registry.register(ToolDefinition(
        name="list_directory", description="List dir", handler=list_directory,
        argument_schema={"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]},
    ))
    permissions = PermissionKernel({
        "read_file": PermissionLevel.AUTONOMOUS,
        "list_directory": PermissionLevel.AUTONOMOUS,
    })
    return ToolExecutor(
        registry=registry,
        permission_kernel=permissions,
        safety=ToolSafety(workspace=tmp_path),
        runtime=ToolRuntime(),
        audit_recorder=AuditRecorder(),
        context=ExecutionContext(workspace=tmp_path),
    )


def _plan(actions):
    return Plan(goal="Test goal", actions=actions, success_criteria=["pass"])


def _action(action_id, tool, arguments, **kwargs):
    defaults = dict(
        action_id=action_id, tool=tool, arguments=arguments,
        expected_result="ok", verification_method="test",
    )
    defaults.update(kwargs)
    return Action(**defaults)


def test_single_action_success(tmp_path):
    (tmp_path / "hello.txt").write_text("world")
    ae = ActionExecutor(
        tool_executor=_build_tool_executor(tmp_path),
        verification_engine=VerificationEngine(),
        recovery_engine=RecoveryEngine(),
        checkpoint_store=CheckpointStore(),
    )
    plan = _plan([_action("a1", "read_file", {"path": str(tmp_path / "hello.txt")})])
    report = ae.execute_plan("t-1", plan, tmp_path)
    assert report.success
    assert report.actions_completed == 1
    assert report.actions_failed == 0


def test_failed_action_stops_plan(tmp_path):
    ae = ActionExecutor(
        tool_executor=_build_tool_executor(tmp_path),
        verification_engine=VerificationEngine(),
        recovery_engine=RecoveryEngine(),
        checkpoint_store=CheckpointStore(),
    )
    plan = _plan([
        _action("a1", "read_file", {"path": str(tmp_path / "missing.txt")}),
        _action("a2", "read_file", {"path": str(tmp_path / "also_missing.txt")}),
    ])
    report = ae.execute_plan("t-2", plan, tmp_path)
    assert not report.success
    assert report.actions_failed == 1
    # Second action should not have been attempted
    assert report.actions_completed + report.actions_failed == 1


def test_multiple_actions_success(tmp_path):
    (tmp_path / "a.txt").write_text("aaa")
    (tmp_path / "b.txt").write_text("bbb")
    ae = ActionExecutor(
        tool_executor=_build_tool_executor(tmp_path),
        verification_engine=VerificationEngine(),
        recovery_engine=RecoveryEngine(),
        checkpoint_store=CheckpointStore(),
    )
    plan = _plan([
        _action("a1", "read_file", {"path": str(tmp_path / "a.txt")}),
        _action("a2", "read_file", {"path": str(tmp_path / "b.txt")}),
    ])
    report = ae.execute_plan("t-3", plan, tmp_path)
    assert report.success
    assert report.actions_completed == 2


def test_cancellation_before_execution(tmp_path):
    ae = ActionExecutor(
        tool_executor=_build_tool_executor(tmp_path),
        verification_engine=VerificationEngine(),
        recovery_engine=RecoveryEngine(),
        checkpoint_store=CheckpointStore(),
    )
    ae.cancel("t-4")
    plan = _plan([_action("a1", "read_file", {"path": "x"})])
    report = ae.execute_plan("t-4", plan, tmp_path)
    assert not report.success
    assert report.cancelled


def test_cancel_is_task_specific(tmp_path):
    (tmp_path / "f.txt").write_text("data")
    ae = ActionExecutor(
        tool_executor=_build_tool_executor(tmp_path),
        verification_engine=VerificationEngine(),
        recovery_engine=RecoveryEngine(),
        checkpoint_store=CheckpointStore(),
    )
    ae.cancel("other-task")
    plan = _plan([_action("a1", "read_file", {"path": str(tmp_path / "f.txt")})])
    report = ae.execute_plan("my-task", plan, tmp_path)
    assert not report.cancelled


def test_action_limit(tmp_path):
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / "b.txt").write_text("b")
    ae = ActionExecutor(
        tool_executor=_build_tool_executor(tmp_path),
        verification_engine=VerificationEngine(),
        recovery_engine=RecoveryEngine(),
        checkpoint_store=CheckpointStore(),
        max_actions=1,
    )
    plan = _plan([
        _action("a1", "read_file", {"path": str(tmp_path / "a.txt")}),
        _action("a2", "read_file", {"path": str(tmp_path / "b.txt")}),
    ])
    report = ae.execute_plan("t-5", plan, tmp_path)
    assert not report.success
    assert "limit" in report.reason.lower()


def test_checkpoint_saved_on_success(tmp_path):
    (tmp_path / "test.txt").write_text("content")
    store = CheckpointStore()
    ae = ActionExecutor(
        tool_executor=_build_tool_executor(tmp_path),
        verification_engine=VerificationEngine(),
        recovery_engine=RecoveryEngine(),
        checkpoint_store=store,
    )
    plan = _plan([_action("a1", "read_file", {"path": str(tmp_path / "test.txt")})])
    ae.execute_plan("t-6", plan, tmp_path)
    state = store.load("t-6")
    assert state is not None
    assert "a1" in state.completed_actions
    assert state.status == "completed"


def test_checkpoint_saved_on_failure(tmp_path):
    store = CheckpointStore()
    ae = ActionExecutor(
        tool_executor=_build_tool_executor(tmp_path),
        verification_engine=VerificationEngine(),
        recovery_engine=RecoveryEngine(),
        checkpoint_store=store,
    )
    plan = _plan([_action("a1", "read_file", {"path": str(tmp_path / "nope.txt")})])
    ae.execute_plan("t-7", plan, tmp_path)
    state = store.load("t-7")
    assert state is not None
    assert "a1" in state.failed_actions
    assert state.status == "failed"


def test_list_directory_action(tmp_path):
    (tmp_path / "x.txt").write_text("x")
    ae = ActionExecutor(
        tool_executor=_build_tool_executor(tmp_path),
        verification_engine=VerificationEngine(),
        recovery_engine=RecoveryEngine(),
        checkpoint_store=CheckpointStore(),
    )
    plan = _plan([_action("a1", "list_directory", {"path": str(tmp_path)})])
    report = ae.execute_plan("t-8", plan, tmp_path)
    assert report.success


def test_unknown_tool_fails(tmp_path):
    ae = ActionExecutor(
        tool_executor=_build_tool_executor(tmp_path),
        verification_engine=VerificationEngine(),
        recovery_engine=RecoveryEngine(),
        checkpoint_store=CheckpointStore(),
    )
    plan = _plan([_action("a1", "nonexistent_tool", {})])
    report = ae.execute_plan("t-9", plan, tmp_path)
    assert not report.success
    assert report.actions_failed == 1


def test_recovery_retry_on_safe_policy(tmp_path):
    """A SAFE-policy action that fails should be retried before giving up."""
    ae = ActionExecutor(
        tool_executor=_build_tool_executor(tmp_path),
        verification_engine=VerificationEngine(),
        recovery_engine=RecoveryEngine(),
        checkpoint_store=CheckpointStore(),
    )
    plan = _plan([
        _action("a1", "read_file", {"path": str(tmp_path / "nope.txt")},
                retry_policy=RetryPolicy.SAFE, risk=ActionRisk.LOW),
    ])
    report = ae.execute_plan("t-10", plan, tmp_path)
    assert not report.success
    # Should have attempted recovery (>0 attempts)
    assert report.outcomes[0].recovery_attempts > 0
