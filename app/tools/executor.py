# 🚦 Tool execution coordinator
# This class runs a tool only after checking that it exists, is permitted,
# and is safe. Every outcome is saved to the audit trail.

from app.models.audit_event import AuditEvent
from app.models.tool_call import ToolCall
from app.models.tool_result import ToolResult, ToolResultStatus
from app.security.permissions import PermissionKernel
from app.security.safety import ToolSafety
from app.tools.audit import AuditRecorder
from app.tools.registry import ToolRegistry
from app.tools.runtime import ToolRuntime


class ToolExecutor:
    def __init__(
        self,
        registry: ToolRegistry,
        permission_kernel: PermissionKernel,
        safety: ToolSafety,
        runtime: ToolRuntime,
        audit_recorder: AuditRecorder,
    ):
        self.registry = registry
        self.permission_kernel = permission_kernel
        self.safety = safety
        self.runtime = runtime
        self.audit_recorder = audit_recorder

    def _record(
        self,
        tool_name: str,
        success: bool,
        message: str,
    ) -> None:
        self.audit_recorder.record(
            AuditEvent(
                tool_name=tool_name,
                success=success,
                message=message,
            )
        )

    def execute(self, tool_call: ToolCall) -> ToolResult:
        # 🧰 Step 1: resolve the requested tool.
        try:
            tool = self.registry.get(tool_call.tool_name)

        except KeyError as exc:
            message = str(exc)

            self._record(
                tool_name=tool_call.tool_name,
                success=False,
                message=message,
            )

            return ToolResult(
                status=ToolResultStatus.FAILED,
                error=message,
            )

        # 🛡️ Step 2: check permission.
        decision = self.permission_kernel.check(
            tool_call.tool_name
        )

        # 🟡 Approval means execution has NOT failed.
        # It is waiting for authorization.
        if decision.requires_approval:
            self._record(
                tool_name=tool_call.tool_name,
                success=False,
                message=decision.reason,
            )

            return ToolResult(
                status=ToolResultStatus.WAITING_APPROVAL,
                error=decision.reason,
            )

        # 🔴 Blocked means the system explicitly rejects execution.
        if not decision.allowed:
            self._record(
                tool_name=tool_call.tool_name,
                success=False,
                message=decision.reason,
            )

            return ToolResult(
                status=ToolResultStatus.BLOCKED,
                error=decision.reason,
            )

        # 🔒 Step 3: safety checks.
        safety_decision = self.safety.check(tool_call)

        if not safety_decision.safe:
            self._record(
                tool_name=tool_call.tool_name,
                success=False,
                message=safety_decision.reason,
            )

            return ToolResult(
                status=ToolResultStatus.FAILED,
                error=safety_decision.reason,
            )

        # ⚙️ Step 4: actually execute the tool.
        result = self.runtime.execute(
            tool,
            **tool_call.arguments,
        )

        # 📝 Step 5: audit the actual execution outcome.
        message = (
            "Tool executed successfully."
            if result.success
            else result.error or "Tool execution failed."
        )

        self._record(
            tool_name=tool_call.tool_name,
            success=result.success,
            message=message,
        )

        return result