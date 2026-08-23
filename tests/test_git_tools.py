from pathlib import Path

from app.tools.builtin.git import git_status


def test_git_status_runs_in_workspace(tmp_path: Path):
    result = git_status(tmp_path)

    assert "return_code" in result
    assert "stdout" in result
    assert "stderr" in result