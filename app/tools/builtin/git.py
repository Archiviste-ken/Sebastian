from pathlib import Path
import subprocess

from app.tools.context import ExecutionContext


def _run_git(
    workspace: Path,
    arguments: list[str],
) -> dict:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=workspace,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        shell=False,
        check=False,
    )

    return {
        "return_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def git_status(context: ExecutionContext) -> dict:
    return _run_git(
        context.workspace,
        ["status", "--short"],
    )


def git_diff(context: ExecutionContext) -> dict:
    return _run_git(
        context.workspace,
        ["diff"],
    )


def git_log(context: ExecutionContext) -> dict:
    return _run_git(
        context.workspace,
        ["log", "--oneline", "-10"],
    )