import subprocess
from pathlib import Path


def _run_git(
    workspace: Path,
    arguments: list[str],
) -> dict:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=workspace,
        capture_output=True,
        text=True,
        shell=False,
        check=False,
    )

    return {
        "return_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def git_status(workspace: Path) -> dict:
    return _run_git(
        workspace,
        ["status", "--short"],
    )


def git_diff(workspace: Path) -> dict:
    return _run_git(
        workspace,
        ["diff"],
    )


def git_log(workspace: Path) -> dict:
    return _run_git(
        workspace,
        ["log", "--oneline", "-10"],
    )