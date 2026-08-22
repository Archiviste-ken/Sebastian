from dataclasses import dataclass
from pathlib import Path

from app.models.tool_call import ToolCall


@dataclass(frozen=True)
class SafetyDecision:
    safe: bool
    reason: str


class ToolSafety:
    def __init__(self, workspace: Path | None = None):
        self.workspace = (
            workspace if workspace is not None else Path.cwd()
        ).resolve()

    def check(self, tool_call: ToolCall) -> SafetyDecision:
        if not tool_call.tool_name.strip():
            return SafetyDecision(
                safe=False,
                reason="Tool name cannot be empty.",
            )

        if tool_call.tool_name == "read_file":
            return self._check_filesystem_path(tool_call)

        if tool_call.tool_name == "list_directory":
            return self._check_filesystem_path(tool_call)

        return SafetyDecision(
            safe=True,
            reason="Tool call passed basic safety checks.",
        )

    def _check_filesystem_path(
        self,
        tool_call: ToolCall,
    ) -> SafetyDecision:
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