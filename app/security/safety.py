# 🛡️ Call safety checks
# These checks reject malformed calls and prevent filesystem tools from escaping
# the workspace chosen for this Sebastian session.

from dataclasses import dataclass
from pathlib import Path

from app.models.tool_call import ToolCall


@dataclass(frozen=True)
class SafetyDecision:
    # ✅ True means the call can continue to execution.
    safe: bool
    # 💬 Short explanation that can be shown in a result or audit record.
    reason: str


class ToolSafety:
    def __init__(self, workspace: Path | None = None):
        # 📍 Resolve once so every later path comparison uses the same absolute folder.
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

        if tool_call.tool_name in {
            "read_file",
            "list_directory",
            "write_file",
}:
    # 🔒 All filesystem tools must stay inside the allowed workspace.
            return self._check_filesystem_path(tool_call)

        # ✅ Other tools currently need only the basic name check.
        return SafetyDecision(
            safe=True,
            reason="Tool call passed basic safety checks.",
        )

    def _check_filesystem_path(
        self,
        tool_call: ToolCall,
    ) -> SafetyDecision:
        # 📥 Read the common `path` argument used by filesystem tools.
        path_value = tool_call.arguments.get("path")

        if not isinstance(path_value, str) or not path_value.strip():
            # ❌ Do not accept missing, blank, or non-text paths.
            return SafetyDecision(
                safe=False,
                reason=f"{tool_call.tool_name} requires a non-empty path.",
            )

        # 🧭 Turn the text into a path object so Python can resolve it safely.
        candidate = Path(path_value)

        if not candidate.is_absolute():
            # 📁 Treat relative paths as relative to the approved workspace.
            candidate = self.workspace / candidate

        try:
            # 🔍 Resolve `..` and symlinks, then prove the path remains inside the workspace.
            resolved = candidate.resolve()
            resolved.relative_to(self.workspace)
        except ValueError:
            # 🚫 `relative_to` raises ValueError when the path escaped the workspace.
            return SafetyDecision(
                safe=False,
                reason="Path is outside the allowed workspace.",
            )

        # ✅ The final resolved path is safely contained in the workspace.
        return SafetyDecision(
            safe=True,
            reason="Path is inside the allowed workspace.",
        )
