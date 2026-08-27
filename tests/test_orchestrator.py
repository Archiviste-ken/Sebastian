import pytest
from pathlib import Path

from app.llm.gateway import ModelGateway, ModelResponse
from app.orchestrator import Sebastian, TaskReport
from app.security.permissions import PermissionLevel


class FakeGateway(ModelGateway):
    """Returns canned responses: intent JSON for structured calls, arg JSON otherwise."""

    def __init__(self, intent_json=None, arg_json=None, workspace=None):
        self._intent_json = intent_json or (
            '{"goal":"Read a file","constraints":[],"expected_outcome":"File contents shown",'
            '"forbidden_actions":[],"missing_information":[],'
            '"required_permissions":["read_file"],"success_criteria":["File content returned"]}'
        )
        self._workspace = workspace
        # Build default arg_json with absolute path if workspace given.
        if arg_json is not None:
            self._arg_json = arg_json
        elif workspace is not None:
            import json
            self._arg_json = json.dumps({
                "tool_name": "read_file",
                "arguments": {"path": str(workspace / "test.txt")},
            })
        else:
            self._arg_json = '{"tool_name":"read_file","arguments":{"path":"test.txt"}}'

    def generate(self, messages, response_format=None):
        if response_format is not None:
            return ModelResponse(content=self._intent_json, raw=None)
        return ModelResponse(content=self._arg_json, raw=None)


def test_run_returns_task_report(tmp_path):
    (tmp_path / "test.txt").write_text("hello from sebastian")
    agent = Sebastian(
        workspace=tmp_path,
        gateway=FakeGateway(workspace=tmp_path),
        permissions={
            "read_file": PermissionLevel.AUTONOMOUS,
            "list_directory": PermissionLevel.AUTONOMOUS,
            "git_status": PermissionLevel.AUTONOMOUS,
            "git_diff": PermissionLevel.AUTONOMOUS,
            "git_log": PermissionLevel.AUTONOMOUS,
        },
    )
    report = agent.run("Read test.txt")
    assert isinstance(report, TaskReport)
    assert report.goal == "Read a file"
    assert report.execution.actions_total >= 1


def test_run_read_file_success(tmp_path):
    (tmp_path / "test.txt").write_text("hello")
    agent = Sebastian(
        workspace=tmp_path,
        gateway=FakeGateway(workspace=tmp_path),
        permissions={"read_file": PermissionLevel.AUTONOMOUS},
    )
    report = agent.run("Read test.txt")
    assert report.success
    assert report.execution.actions_completed >= 1


def test_run_has_audit_events(tmp_path):
    (tmp_path / "test.txt").write_text("hello")
    agent = Sebastian(
        workspace=tmp_path,
        gateway=FakeGateway(workspace=tmp_path),
        permissions={"read_file": PermissionLevel.AUTONOMOUS},
    )
    report = agent.run("Read test.txt")
    assert len(report.audit_events) > 0


def test_cancel_does_not_error(tmp_path):
    agent = Sebastian(workspace=tmp_path, gateway=FakeGateway(workspace=tmp_path))
    agent.cancel("nonexistent-task")  # Should not raise


def test_run_blocked_tool(tmp_path):
    """When the only matched tool is BLOCKED, the action fails."""
    (tmp_path / "test.txt").write_text("hi")
    agent = Sebastian(
        workspace=tmp_path,
        gateway=FakeGateway(workspace=tmp_path),
        permissions={"read_file": PermissionLevel.BLOCKED},
    )
    report = agent.run("Read test.txt")
    assert not report.success
