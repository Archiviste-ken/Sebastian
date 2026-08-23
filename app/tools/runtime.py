# ⚙️ Tool runtime
# This is the execution wrapper for any registered tool.
# It ensures tool calls are converted into consistent result objects.

from typing import Any

from app.models.tool_result import ToolResult, ToolResultStatus
from app.tools.definition import ToolDefinition


class ToolRuntime:
    def execute(
        self,
        tool: ToolDefinition,
        *args: Any,
        **kwargs: Any,
    ) -> ToolResult:
        try:
            result = tool.handler(*args, **kwargs)

            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                data=result,
            )

        except Exception as exc:
            return ToolResult(
                status=ToolResultStatus.FAILED,
                error=str(exc),
            )