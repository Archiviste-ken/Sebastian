from pathlib import Path

from app.tools.builtin.git import git_status
from app.tools.context import ExecutionContext


def test_git_status_runs_in_workspace(tmp_path: Path):
    context = ExecutionContext(
        workspace=tmp_path,
    )

    result = git_status(context)

    assert "return_code" in result
    assert "stdout" in result
    assert "stderr" in result