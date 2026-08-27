import pytest
from pathlib import Path

from app.models.tool_result import ToolResult, ToolResultStatus
from app.planning.models import Action
from app.verification.engine import VerificationEngine
from app.verification.models import VerificationStatus


def _make_action(tool, arguments=None):
    return Action(
        action_id="test-1",
        tool=tool,
        arguments=arguments or {},
        expected_result="test succeeds",
        verification_method="test",
    )


def _ok(data=None):
    return ToolResult(status=ToolResultStatus.SUCCESS, data=data)


def _fail(error="broke"):
    return ToolResult(status=ToolResultStatus.FAILED, error=error)


@pytest.fixture
def engine():
    return VerificationEngine()


def test_failed_tool_gives_fail(engine, tmp_path):
    v = engine.verify(_make_action("read_file"), _fail(), tmp_path)
    assert v.status == VerificationStatus.FAIL


def test_command_exit_zero_passes(engine, tmp_path):
    v = engine.verify(
        _make_action("run_command"),
        _ok({"return_code": 0, "stdout": "ok", "stderr": ""}),
        tmp_path,
    )
    assert v.status == VerificationStatus.PASS


def test_command_exit_nonzero_fails(engine, tmp_path):
    v = engine.verify(
        _make_action("run_command"),
        _ok({"return_code": 1, "stdout": "", "stderr": "err"}),
        tmp_path,
    )
    assert v.status == VerificationStatus.FAIL


def test_write_file_verified_by_existence(engine, tmp_path):
    target = tmp_path / "out.txt"
    target.write_text("hello")
    v = engine.verify(
        _make_action("write_file", {"path": str(target)}),
        _ok(),
        tmp_path,
    )
    assert v.status == VerificationStatus.PASS


def test_write_file_missing_fails(engine, tmp_path):
    v = engine.verify(
        _make_action("write_file", {"path": str(tmp_path / "missing.txt")}),
        _ok(),
        tmp_path,
    )
    assert v.status == VerificationStatus.FAIL


def test_read_file_with_content_passes(engine, tmp_path):
    v = engine.verify(_make_action("read_file"), _ok("file content"), tmp_path)
    assert v.status == VerificationStatus.PASS


def test_list_directory_with_list_passes(engine, tmp_path):
    v = engine.verify(_make_action("list_directory"), _ok(["a", "b"]), tmp_path)
    assert v.status == VerificationStatus.PASS


def test_unknown_tool_gives_uncertain(engine, tmp_path):
    v = engine.verify(_make_action("future_tool"), _ok(), tmp_path)
    assert v.status == VerificationStatus.UNCERTAIN


def test_create_directory_verified(engine, tmp_path):
    target = tmp_path / "newdir"
    target.mkdir()
    v = engine.verify(
        _make_action("create_directory", {"path": str(target)}),
        _ok(),
        tmp_path,
    )
    assert v.status == VerificationStatus.PASS


def test_move_file_destination_exists(engine, tmp_path):
    dest = tmp_path / "moved.txt"
    dest.write_text("moved")
    v = engine.verify(
        _make_action("move_file", {"destination": str(dest)}),
        _ok(),
        tmp_path,
    )
    assert v.status == VerificationStatus.PASS


def test_move_file_destination_missing(engine, tmp_path):
    v = engine.verify(
        _make_action("move_file", {"destination": str(tmp_path / "gone.txt")}),
        _ok(),
        tmp_path,
    )
    assert v.status == VerificationStatus.FAIL


def test_python_exit_zero(engine, tmp_path):
    v = engine.verify(
        _make_action("run_python"),
        _ok({"return_code": 0, "stdout": "done", "stderr": ""}),
        tmp_path,
    )
    assert v.status == VerificationStatus.PASS


def test_git_status_pass(engine, tmp_path):
    v = engine.verify(
        _make_action("git_status"),
        _ok({"return_code": 0, "stdout": "", "stderr": ""}),
        tmp_path,
    )
    assert v.status == VerificationStatus.PASS
