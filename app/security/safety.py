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

        # 🔒 All single-path filesystem tools use the same workspace check.
        if tool_call.tool_name in {
            "read_file",
            "list_directory",
            "write_file",
            "create_directory",
        }:
            return self._check_filesystem_path(tool_call)

        # 🔀 move_file has TWO paths, so it needs its own validation.
        if tool_call.tool_name == "move_file":
            return self._check_move_file(tool_call)

        # ⌨️ run_command has a command list instead of a filesystem path.
        if tool_call.tool_name == "run_command":
            return self._check_run_command(tool_call)

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
            # ❌ Do not accept missing, blank, or non-text paths.
            return SafetyDecision(
                safe=False,
                reason=f"{tool_call.tool_name} requires a non-empty path.",
            )

        # 🧭 Turn the text into a Path object.
        candidate = Path(path_value)

        if not candidate.is_absolute():
            # 📁 Treat relative paths as relative to the approved workspace.
            candidate = self.workspace / candidate

        try:
            # 🔍 Resolve `..` and symlinks, then prove the path remains
            # inside the workspace.
            resolved = candidate.resolve()
            resolved.relative_to(self.workspace)

        except ValueError:
            # 🚫 `relative_to` raises ValueError when the path escaped
            # the workspace.
            return SafetyDecision(
                safe=False,
                reason="Path is outside the allowed workspace.",
            )

        # ✅ The final resolved path is safely contained in the workspace.
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

        # ❌ Source must be a non-empty string.
        if not isinstance(source, str) or not source.strip():
            return SafetyDecision(
                safe=False,
                reason="move_file requires a non-empty source.",
            )

        # ❌ Destination must be a non-empty string.
        if not isinstance(destination, str) or not destination.strip():
            return SafetyDecision(
                safe=False,
                reason="move_file requires a non-empty destination.",
            )

        # 🔒 Both paths must stay inside the allowed workspace.
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

        # ✅ Both source and destination are inside the workspace.
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

        # ❌ Command must be a non-empty list.
        if not isinstance(command, list) or not command:
            return SafetyDecision(
                safe=False,
                reason="run_command requires a non-empty command list.",
            )

        # ❌ Every command part must be a non-empty string.
        if not all(
            isinstance(part, str) and part.strip()
            for part in command
        ):
            return SafetyDecision(
                safe=False,
                reason="run_command arguments must be non-empty strings.",
            )

        # 🔎 Extract only the executable name.
        executable = Path(command[0]).name.lower()

        # 🚫 Unknown executables are rejected.
        if executable not in ALLOWED_COMMANDS:
            return SafetyDecision(
                safe=False,
                reason=f"Command is not allowed: {executable}",
            )

        # ✅ Executable passed the initial allowlist check.
        return SafetyDecision(
            safe=True,
            reason="Command passed safety checks.",
        )