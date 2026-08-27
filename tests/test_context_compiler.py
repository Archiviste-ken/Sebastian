import pytest
from pathlib import Path

from app.context.compiler import ContextCompiler
from app.context.models import TaskContext
from app.intent.models import Intent
from app.security.permissions import PermissionKernel, PermissionLevel
from app.tools.definition import ToolDefinition
from app.tools.registry import ToolRegistry


def _make_intent(**kwargs):
    defaults = {
        "goal": "Test goal",
        "constraints": [],
        "expected_outcome": "Test outcome",
        "forbidden_actions": [],
        "missing_information": [],
        "required_permissions": [],
        "success_criteria": ["works"],
    }
    defaults.update(kwargs)
    return Intent(**defaults)


def _make_tool(name):
    return ToolDefinition(name=name, description=f"{name} tool", handler=lambda: None)


def test_compile_returns_task_context(tmp_path):
    registry = ToolRegistry()
    registry.register(_make_tool("read_file"))
    permissions = PermissionKernel({"read_file": PermissionLevel.AUTONOMOUS})
    compiler = ContextCompiler(registry=registry, permission_kernel=permissions, workspace=tmp_path)
    intent = _make_intent()
    ctx = compiler.compile("read a file", intent)
    assert isinstance(ctx, TaskContext)
    assert ctx.user_request == "read a file"
    assert ctx.intent_goal == "Test goal"
    assert "read_file" in ctx.available_tools
    assert ctx.tool_permissions["read_file"] == "autonomous"


def test_compile_workspace_files_bounded(tmp_path):
    for i in range(5):
        (tmp_path / f"file_{i}.txt").write_text(f"content {i}")
    registry = ToolRegistry()
    permissions = PermissionKernel({})
    compiler = ContextCompiler(registry=registry, permission_kernel=permissions, workspace=tmp_path)
    intent = _make_intent()
    ctx = compiler.compile("test", intent)
    assert len(ctx.workspace_files) == 5


def test_compile_includes_constraints(tmp_path):
    registry = ToolRegistry()
    permissions = PermissionKernel({})
    compiler = ContextCompiler(registry=registry, permission_kernel=permissions, workspace=tmp_path)
    intent = _make_intent(constraints=["no deleting"], forbidden_actions=["delete"])
    ctx = compiler.compile("test", intent)
    assert "no deleting" in ctx.intent_constraints
    assert "delete" in ctx.intent_forbidden_actions


def test_compile_with_prior_results(tmp_path):
    registry = ToolRegistry()
    permissions = PermissionKernel({})
    compiler = ContextCompiler(registry=registry, permission_kernel=permissions, workspace=tmp_path)
    intent = _make_intent()
    prior = [{"action": "read_file", "success": True}]
    ctx = compiler.compile("test", intent, prior_results=prior)
    assert len(ctx.prior_results) == 1


def test_compile_skips_hidden_files(tmp_path):
    (tmp_path / ".hidden").write_text("secret")
    (tmp_path / "visible.txt").write_text("public")
    registry = ToolRegistry()
    permissions = PermissionKernel({})
    compiler = ContextCompiler(registry=registry, permission_kernel=permissions, workspace=tmp_path)
    ctx = compiler.compile("test", _make_intent())
    assert "visible.txt" in ctx.workspace_files
    assert ".hidden" not in ctx.workspace_files


def test_compile_workspace_path(tmp_path):
    registry = ToolRegistry()
    permissions = PermissionKernel({})
    compiler = ContextCompiler(registry=registry, permission_kernel=permissions, workspace=tmp_path)
    ctx = compiler.compile("test", _make_intent())
    assert ctx.workspace_path == str(tmp_path.resolve())
