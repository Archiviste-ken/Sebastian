"""V1 integration tests: full pipeline without LLM.

These tests exercise Intent -> Context -> Plan -> ActionExecutor -> ToolExecutor
-> Verification -> Recovery -> Checkpoint -> Report without any LLM calls.
The plan is constructed manually to test the deterministic pipeline.
"""
import pytest
from pathlib import Path

from app.checkpoint.store import CheckpointStore
from app.context.compiler import ContextCompiler
from app.context.models import TaskContext
from app.execution.action_executor import ActionExecutor
from app.execution.models import ExecutionReport
from app.intent.models import Intent
from app.models.task import TaskStatus
from app.planning.models import Action, ActionRisk, Plan, RetryPolicy
from app.recovery.engine import RecoveryEngine
from app.security.permissions import PermissionKernel, PermissionLevel
from app.security.safety import ToolSafety
from app.tools.audit import AuditRecorder
from app.tools.builtin.command import run_command
from app.tools.builtin.filesystem import (
    create_directory, list_directory, move_file, read_file, write_file,
)
from app.tools.builtin.python import run_python
from app.tools.context import ExecutionContext
from app.tools.definition import ToolDefinition
from app.tools.executor import ToolExecutor
from app.tools.registry import ToolRegistry
from app.tools.runtime import ToolRuntime
from app.verification.engine import VerificationEngine
from app.verification.models import VerificationStatus


# ── shared fixtures ───────────────────────────────────────────────────

def _full_registry():
    reg = ToolRegistry()
    reg.register(ToolDefinition(
        name="read_file", description="Read file", handler=read_file,
        argument_schema={"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]},
    ))
    reg.register(ToolDefinition(
        name="list_directory", description="List dir", handler=list_directory,
        argument_schema={"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]},
    ))
    reg.register(ToolDefinition(
        name="write_file", description="Write file", handler=write_file,
        argument_schema={
            "type": "object",
            "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
            "required": ["path", "content"],
        },
    ))
    reg.register(ToolDefinition(
        name="create_directory", description="Create dir", handler=create_directory,
        argument_schema={"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]},
    ))
    reg.register(ToolDefinition(
        name="move_file", description="Move file", handler=move_file,
        argument_schema={
            "type": "object",
            "properties": {"source": {"type": "string"}, "destination": {"type": "string"}},
            "required": ["source", "destination"],
        },
    ))
    reg.register(ToolDefinition(
        name="run_command", description="Run command", handler=run_command,
        argument_schema={
            "type": "object",
            "properties": {"command": {"type": "array", "items": {"type": "string"}}},
            "required": ["command"],
        },
    ))
    reg.register(ToolDefinition(
        name="run_python", description="Run python", handler=run_python,
        argument_schema={"type": "object", "properties": {"script": {"type": "string"}}, "required": ["script"]},
    ))
    return reg


def _build_pipeline(tmp_path, permissions=None):
    reg = _full_registry()
    default_perms = {
        "read_file": PermissionLevel.AUTONOMOUS,
        "list_directory": PermissionLevel.AUTONOMOUS,
        "write_file": PermissionLevel.AUTONOMOUS,
        "create_directory": PermissionLevel.AUTONOMOUS,
        "move_file": PermissionLevel.AUTONOMOUS,
        "run_command": PermissionLevel.AUTONOMOUS,
        "run_python": PermissionLevel.AUTONOMOUS,
    }
    pk = PermissionKernel(permissions or default_perms)
    te = ToolExecutor(
        registry=reg,
        permission_kernel=pk,
        safety=ToolSafety(workspace=tmp_path),
        runtime=ToolRuntime(),
        audit_recorder=AuditRecorder(),
        context=ExecutionContext(workspace=tmp_path),
    )
    return ActionExecutor(
        tool_executor=te,
        verification_engine=VerificationEngine(),
        recovery_engine=RecoveryEngine(),
        checkpoint_store=CheckpointStore(),
    )


def _action(aid, tool, args, **kw):
    defaults = dict(
        action_id=aid, tool=tool, arguments=args,
        expected_result="ok", verification_method="test",
    )
    defaults.update(kw)
    return Action(**defaults)


def _plan(actions):
    return Plan(goal="integration test", actions=actions, success_criteria=["pass"])


# ── 1. Read a file ────────────────────────────────────────────────────
def test_read_file_end_to_end(tmp_path):
    (tmp_path / "readme.txt").write_text("Sebastian V1")
    ae = _build_pipeline(tmp_path)
    plan = _plan([_action("a1", "read_file", {"path": str(tmp_path / "readme.txt")})])
    report = ae.execute_plan("t-read", plan, tmp_path)
    assert report.success
    assert report.outcomes[0].verification.status == VerificationStatus.PASS


# ── 2. Inspect a directory ────────────────────────────────────────────
def test_list_directory_end_to_end(tmp_path):
    (tmp_path / "a.py").write_text("pass")
    (tmp_path / "b.py").write_text("pass")
    ae = _build_pipeline(tmp_path)
    plan = _plan([_action("a1", "list_directory", {"path": str(tmp_path)})])
    report = ae.execute_plan("t-list", plan, tmp_path)
    assert report.success


# ── 3. Write and verify a file ────────────────────────────────────────
def test_write_file_verified(tmp_path):
    target = str(tmp_path / "output.txt")
    ae = _build_pipeline(tmp_path)
    plan = _plan([_action("a1", "write_file", {"path": target, "content": "hello"})])
    report = ae.execute_plan("t-write", plan, tmp_path)
    assert report.success
    assert (tmp_path / "output.txt").read_text() == "hello"
    assert report.outcomes[0].verification.status == VerificationStatus.PASS


# ── 4. Block unsafe path ──────────────────────────────────────────────
def test_block_path_traversal(tmp_path):
    ae = _build_pipeline(tmp_path)
    plan = _plan([_action("a1", "read_file", {"path": "/etc/passwd"})])
    report = ae.execute_plan("t-unsafe", plan, tmp_path)
    assert not report.success


# ── 5. Block forbidden tool ───────────────────────────────────────────
def test_block_unregistered_tool(tmp_path):
    ae = _build_pipeline(tmp_path)
    plan = _plan([_action("a1", "delete_everything", {})])
    report = ae.execute_plan("t-forbidden", plan, tmp_path)
    assert not report.success


# ── 6. Require approval ──────────────────────────────────────────────
def test_approval_required_blocks(tmp_path):
    ae = _build_pipeline(tmp_path, permissions={
        "read_file": PermissionLevel.APPROVAL,
    })
    (tmp_path / "f.txt").write_text("x")
    plan = _plan([_action("a1", "read_file", {"path": str(tmp_path / "f.txt")})])
    report = ae.execute_plan("t-approval", plan, tmp_path)
    assert not report.success


# ── 7. Recover from a failed tool (bounded retries) ──────────────────
def test_recovery_retries_then_fails(tmp_path):
    ae = _build_pipeline(tmp_path)
    plan = _plan([
        _action("a1", "read_file", {"path": str(tmp_path / "ghost.txt")},
                retry_policy=RetryPolicy.SAFE, risk=ActionRisk.LOW),
    ])
    report = ae.execute_plan("t-recover", plan, tmp_path)
    assert not report.success
    assert report.outcomes[0].recovery_attempts > 0


# ── 8. Cancel a task ──────────────────────────────────────────────────
def test_cancel_task(tmp_path):
    ae = _build_pipeline(tmp_path)
    ae.cancel("t-cancel")
    plan = _plan([_action("a1", "read_file", {"path": "x"})])
    report = ae.execute_plan("t-cancel", plan, tmp_path)
    assert report.cancelled
    assert not report.success


# ── 9. Checkpoint persists state ──────────────────────────────────────
def test_checkpoint_persists(tmp_path):
    store = CheckpointStore()
    reg = _full_registry()
    pk = PermissionKernel({"read_file": PermissionLevel.AUTONOMOUS})
    te = ToolExecutor(
        registry=reg, permission_kernel=pk,
        safety=ToolSafety(workspace=tmp_path),
        runtime=ToolRuntime(), audit_recorder=AuditRecorder(),
        context=ExecutionContext(workspace=tmp_path),
    )
    ae = ActionExecutor(
        tool_executor=te,
        verification_engine=VerificationEngine(),
        recovery_engine=RecoveryEngine(),
        checkpoint_store=store,
    )
    (tmp_path / "c.txt").write_text("checkpoint")
    plan = _plan([_action("a1", "read_file", {"path": str(tmp_path / "c.txt")})])
    ae.execute_plan("t-ckpt", plan, tmp_path)
    state = store.load("t-ckpt")
    assert state is not None
    assert state.status == "completed"
    assert "a1" in state.completed_actions


# ── 10. Context compiler integration ─────────────────────────────────
def test_context_compiler_integrates(tmp_path):
    (tmp_path / "src.py").write_text("print(1)")
    reg = _full_registry()
    pk = PermissionKernel({"read_file": PermissionLevel.AUTONOMOUS})
    compiler = ContextCompiler(registry=reg, permission_kernel=pk, workspace=tmp_path)
    intent = Intent(
        goal="Read source", constraints=[], expected_outcome="content",
        forbidden_actions=[], missing_information=[],
        required_permissions=["read_file"], success_criteria=["ok"],
    )
    ctx = compiler.compile("read src.py", intent)
    assert isinstance(ctx, TaskContext)
    assert "read_file" in ctx.available_tools
    assert len(ctx.workspace_files) >= 1


# ── 11. Create directory verified ─────────────────────────────────────
def test_create_directory_end_to_end(tmp_path):
    target = str(tmp_path / "newdir")
    ae = _build_pipeline(tmp_path)
    plan = _plan([_action("a1", "create_directory", {"path": target})])
    report = ae.execute_plan("t-mkdir", plan, tmp_path)
    assert report.success
    assert (tmp_path / "newdir").is_dir()


# ── 12. Move file verified ───────────────────────────────────────────
def test_move_file_end_to_end(tmp_path):
    src = tmp_path / "orig.txt"
    dst = tmp_path / "moved.txt"
    src.write_text("data")
    ae = _build_pipeline(tmp_path)
    plan = _plan([_action("a1", "move_file", {"source": str(src), "destination": str(dst)})])
    report = ae.execute_plan("t-move", plan, tmp_path)
    assert report.success
    assert dst.exists()
    assert not src.exists()


# ── 13. Multi-action plan ─────────────────────────────────────────────
def test_multi_action_plan(tmp_path):
    (tmp_path / "step1.txt").write_text("step1")
    ae = _build_pipeline(tmp_path)
    plan = _plan([
        _action("a1", "read_file", {"path": str(tmp_path / "step1.txt")}),
        _action("a2", "list_directory", {"path": str(tmp_path)}),
    ])
    report = ae.execute_plan("t-multi", plan, tmp_path)
    assert report.success
    assert report.actions_completed == 2
    assert len(report.outcomes) == 2
