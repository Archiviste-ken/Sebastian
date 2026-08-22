from app.models.tool_call import ToolCall
from app.models.tool_result import ToolResult
from app.security.permissions import PermissionKernel
from app.security.safety import ToolSafety
from app.tools.registry import ToolRegistry
from app.tools.runtime import ToolRuntime


class ToolExecutor:
    def __init__(
        self,
        registry: ToolRegistry,
        permission_kernel: PermissionKernel,
        safety: ToolSafety,
        runtime: ToolRuntime,
    ):
        self.registry = registry
        self.permission_kernel = permission_kernel
        self.safety = safety
        self.runtime = runtime

    def execute(self, tool_call: ToolCall) -> ToolResult:
        try:
            tool = self.registry.get(tool_call.tool_name)
        except KeyError as exc:
            return ToolResult(
                success=False,
                error=str(exc),
            )

        decision = self.permission_kernel.check(tool_call.tool_name)

        if decision.requires_approval:
            return ToolResult(
                success=False,
                error=decision.reason,
            )

        if not decision.allowed:
            return ToolResult(
                success=False,
                error=decision.reason,
            )

        safety_decision = self.safety.check(tool_call)

        if not safety_decision.safe:
            return ToolResult(
                success=False,
                error=safety_decision.reason,
            )

        return self.runtime.execute(
            tool,
            **tool_call.arguments,
        )