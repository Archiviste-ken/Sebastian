# ⚙️ Tool runtime
# This is the execution wrapper for any registered tool.
# It ensures tool calls are converted into consistent result objects.

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
        # 🏃 Attempt to run the tool's handler.
        try:
            result = tool.handler(*args, **kwargs)

            # ✅ Return a success payload with the tool's data.
            return ToolResult(
                success=True,
                data=result,
            )

        # ❌ Catch any exception and normalize it into a failure result.
        except Exception as exc:
            return ToolResult(
                success=False,
                error=str(exc),
            )