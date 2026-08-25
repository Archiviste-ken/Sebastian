# 🐙 Git operation tools
# ⚙️ Provides safe wrappers around git commands bounded to the workspace.

# 📁 Import Path to represent the workspace directory.
from pathlib import Path
# 📦 Import subprocess to shell out to the git executable.
import subprocess

# ⚙️ Import ExecutionContext to extract the allowed workspace path.
from app.tools.context import ExecutionContext


# 🔌 Internal helper to execute git commands safely within the workspace.
def _run_git(
    # 📁 The guaranteed-safe workspace directory.
    workspace: Path,
    # ⌨️ The list of git arguments to append to the command.
    arguments: list[str],
) -> dict:
    # 🚀 Run the git executable as a child process.
    completed = subprocess.run(
        # ⌨️ Construct the full command starting with 'git'.
        ["git", *arguments],
        # 📍 Force the command to execute inside the workspace.
        cwd=workspace,
        # 📥 Capture stdout and stderr streams.
        capture_output=True,
        # 📝 Decode streams as text.
        text=True,
        # 🔡 Force UTF-8 decoding to match most modern git setups.
        encoding="utf-8",
        # 🛡️ Replace decoding errors rather than crashing the tool.
        errors="replace",
        # 🔒 Disable shell execution for security.
        shell=False,
        # ⚠️ Do not raise an exception on non-zero exit codes.
        check=False,
    )

    # 🏗️ Return a dictionary containing the execution results.
    return {
        # 🔢 The numeric exit status of the git command.
        "return_code": completed.returncode,
        # 💬 The text printed to standard output.
        "stdout": completed.stdout,
        # 💬 The text printed to standard error.
        "stderr": completed.stderr,
    }


# 🐙 Handler for retrieving the short git status.
def git_status(context: ExecutionContext) -> dict:
    # 🚀 Delegate to the internal runner with the status arguments.
    return _run_git(
        # 📁 Pass the workspace path from the context.
        context.workspace,
        # ⌨️ Use short format for easier parsing and smaller payloads.
        ["status", "--short"],
    )


# 🐙 Handler for retrieving the unstaged git differences.
def git_diff(context: ExecutionContext) -> dict:
    # 🚀 Delegate to the internal runner with the diff argument.
    return _run_git(
        # 📁 Pass the workspace path from the context.
        context.workspace,
        # ⌨️ Request the standard patch diff format.
        ["diff"],
    )


# 🐙 Handler for retrieving the recent commit history.
def git_log(context: ExecutionContext) -> dict:
    # 🚀 Delegate to the internal runner with the log arguments.
    return _run_git(
        # 📁 Pass the workspace path from the context.
        context.workspace,
        # ⌨️ Request a condensed oneline format, limited to 10 commits.
        ["log", "--oneline", "-10"],
    )