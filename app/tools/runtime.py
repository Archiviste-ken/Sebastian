from typing import Any

from app.models.tool_result import ToolResult
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
                success=True,
                data=result,
            )

        except Exception as exc:
            return ToolResult(
                success=False,
                error=str(exc),
            )