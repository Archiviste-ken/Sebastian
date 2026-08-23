# 🛡️ Call safety checks
# These checks reject malformed calls and prevent filesystem tools from escaping
# the workspace chosen for this Sebastian session.

from dataclasses import dataclass
from pathlib import Path

from app.models.tool_call import ToolCall


# 🔒 Only these executables are currently allowed by the command safety policy.
ALLOWED_COMMANDS = {
    "python",
    "python.exe",
    "pytest",
    "pytest.exe",
    "git",
    "git.exe",
}


@dataclass(frozen=True)
class SafetyDecision:
    # ✅ True means the call can continue to execution.
    safe: bool

    # 💬 Short explanation that can be shown in a result or audit record.
    reason: str


class ToolSafety:
    def __init__(self, workspace: Path | None = None):
        # 📍 Resolve once so every later path comparison uses the same
        # absolute folder.
        self.workspace = (
            workspace if workspace is not None else Path.cwd()
        ).resolve()

    def check(self, tool_call: ToolCall) -> SafetyDecision:
        # 🏷️ A blank tool name cannot be looked up or run safely.
        if not tool_call.tool_name.strip():
            return SafetyDecision(
                safe=False,
                reason="Tool name cannot be empty.",
            )

        # 🔒 Single-path filesystem tools.
        if tool_call.tool_name in {
            "read_file",
            "list_directory",
            "write_file",
            "create_directory",
        }:
            return self._check_filesystem_path(tool_call)

        # 🔀 move_file has TWO paths.
        if tool_call.tool_name == "move_file":
            return self._check_move_file(tool_call)

        # ⌨️ run_command has a command list.
        if tool_call.tool_name == "run_command":
            return self._check_run_command(tool_call)

        # 🐍 run_python has a script path.
        if tool_call.tool_name == "run_python":
            return self._check_python_script(tool_call)

        # 🐙 Git inspection tools operate only on the approved workspace.
        if tool_call.tool_name in {
            "git_status",
            "git_diff",
            "git_log",
        }:
            return self._check_git_workspace(tool_call)

        # ✅ Other tools currently need only the basic name check.
        return SafetyDecision(
            safe=True,
            reason="Tool call passed basic safety checks.",
        )

    def _check_filesystem_path(
        self,
        tool_call: ToolCall,
    ) -> SafetyDecision:
        # 📥 Read the common `path` argument used by single-path tools.
        path_value = tool_call.arguments.get("path")

        if not isinstance(path_value, str) or not path_value.strip():
            return SafetyDecision(
                safe=False,
                reason=f"{tool_call.tool_name} requires a non-empty path.",
            )

        candidate = Path(path_value)

        if not candidate.is_absolute():
            candidate = self.workspace / candidate

        try:
            # 🔍 Resolve `..` and symlinks, then prove the path remains
            # inside the workspace.
            resolved = candidate.resolve()
            resolved.relative_to(self.workspace)

        except ValueError:
            return SafetyDecision(
                safe=False,
                reason="Path is outside the allowed workspace.",
            )

        return SafetyDecision(
            safe=True,
            reason="Path is inside the allowed workspace.",
        )

    def _check_move_file(
        self,
        tool_call: ToolCall,
    ) -> SafetyDecision:
        # 📥 move_file has two paths instead of one.
        source = tool_call.arguments.get("source")
        destination = tool_call.arguments.get("destination")

        if not isinstance(source, str) or not source.strip():
            return SafetyDecision(
                safe=False,
                reason="move_file requires a non-empty source.",
            )

        if not isinstance(destination, str) or not destination.strip():
            return SafetyDecision(
                safe=False,
                reason="move_file requires a non-empty destination.",
            )

        # 🔒 Both paths must remain inside the workspace.
        for path_value in (source, destination):
            candidate = Path(path_value)

            if not candidate.is_absolute():
                candidate = self.workspace / candidate

            try:
                resolved = candidate.resolve()
                resolved.relative_to(self.workspace)

            except ValueError:
                return SafetyDecision(
                    safe=False,
                    reason="Path is outside the allowed workspace.",
                )

        return SafetyDecision(
            safe=True,
            reason="Source and destination are inside the allowed workspace.",
        )

    def _check_run_command(
        self,
        tool_call: ToolCall,
    ) -> SafetyDecision:
        # 📥 Get the command argument.
        command = tool_call.arguments.get("command")

        if not isinstance(command, list) or not command:
            return SafetyDecision(
                safe=False,
                reason="run_command requires a non-empty command list.",
            )

        if not all(
            isinstance(part, str) and part.strip()
            for part in command
        ):
            return SafetyDecision(
                safe=False,
                reason="run_command arguments must be non-empty strings.",
            )

        # 🔎 Extract the executable name.
        executable = Path(command[0]).name.lower()

        if executable not in ALLOWED_COMMANDS:
            return SafetyDecision(
                safe=False,
                reason=f"Command is not allowed: {executable}",
            )

        return SafetyDecision(
            safe=True,
            reason="Command passed safety checks.",
        )

    def _check_python_script(
        self,
        tool_call: ToolCall,
    ) -> SafetyDecision:
        # 📥 Get the script path.
        script = tool_call.arguments.get("script")

        if not isinstance(script, str) or not script.strip():
            return SafetyDecision(
                safe=False,
                reason="run_python requires a non-empty script path.",
            )

        candidate = Path(script)

        if not candidate.is_absolute():
            candidate = self.workspace / candidate

        try:
            # 🔍 Resolve the path and ensure it stays inside the workspace.
            resolved = candidate.resolve()
            resolved.relative_to(self.workspace)

        except ValueError:
            return SafetyDecision(
                safe=False,
                reason="Python script is outside the allowed workspace.",
            )

        # 🐍 Only Python scripts are accepted.
        if resolved.suffix.lower() != ".py":
            return SafetyDecision(
                safe=False,
                reason="run_python requires a .py script.",
            )

        return SafetyDecision(
            safe=True,
            reason="Python script passed safety checks.",
        )

    def _check_git_workspace(
        self,
        tool_call: ToolCall,
    ) -> SafetyDecision:
        # 🐙 Git tools do not accept an arbitrary repository path.
        # They operate only against the trusted Sebastian workspace.
        return SafetyDecision(
            safe=True,
            reason="Git operation is restricted to the Sebastian workspace.",
        )