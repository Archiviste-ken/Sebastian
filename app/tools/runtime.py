# ⚙️ Tool runtime
# This is the execution wrapper for any registered tool.
# It ensures tool calls are converted into consistent result objects.

# 📦 Import Any to type opaque tool arguments and return values.
from typing import Any

# 📦 Import result models to wrap the execution output.
from app.models.tool_result import ToolResult, ToolResultStatus
# ⚙️ Import ExecutionContext to optionally inject environment state.
from app.tools.context import ExecutionContext
# 🧩 Import ToolDefinition to access the handler callable.
from app.tools.definition import ToolDefinition


# 🔌 Define the class responsible for directly invoking python functions.
class ToolRuntime:
    # 🚀 Method to safely wrap and execute a tool definition's handler.
    def execute(
        # 🧍 Reference to the current instance.
        self,
        # 🧩 The validated tool definition to run.
        tool: ToolDefinition,
        # 📦 The keyword arguments to pass to the tool.
        arguments: dict[str, Any],
        # ⚙️ The execution context holding environment details.
        context: ExecutionContext,
    ) -> ToolResult:
        # 🛡️ Wrap execution in a global try/except to catch panics gracefully.
        try:
            # ⚖️ Check if the tool requires the ExecutionContext explicitly.
            if tool.uses_context:
                # 🚀 Call the handler function, injecting the context parameter.
                result = tool.handler(
                    # ⚙️ Inject the context.
                    context=context,
                    # 📦 Unpack the remaining arguments from the caller.
                    **arguments,
                )
            # 🔄 Otherwise, call the tool normally without injecting context.
            else:
                # 🚀 Call the handler function with just the caller's arguments.
                result = tool.handler(
                    # 📦 Unpack all arguments.
                    **arguments,
                )

            # 🏗️ Construct a successful result containing the handler's output.
            return ToolResult(
                # 🟢 Mark the status as a complete success.
                status=ToolResultStatus.SUCCESS,
                # 📦 Attach the returned data.
                data=result,
            )

        # ⚠️ Catch absolutely any exception raised inside the tool handler.
        except Exception as exc:
            # 🚫 Construct a failure result containing the error string.
            return ToolResult(
                # 🔴 Mark the status as a failure.
                status=ToolResultStatus.FAILED,
                # 💬 Attach the string representation of the exception.
                error=str(exc),
            )