# 🚦 Tool execution coordinator
# This class runs a tool only after checking that it exists, is permitted,
# and is safe. Every outcome is saved to the audit trail.

from app.models.audit_event import AuditEvent
from app.models.tool_call import ToolCall
from app.models.tool_result import ToolResult
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
        # 🧩 Keep the collaborators together so one place controls the full flow.
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
        # 📝 Store a small, permanent record for both successes and failures.
        self.audit_recorder.record(
            AuditEvent(
                tool_name=tool_name,
                success=success,
                message=message,
            )
        )

    def execute(self, tool_call: ToolCall) -> ToolResult:
        # 1️⃣ Find the requested tool before doing any other work.
        try:
            tool = self.registry.get(tool_call.tool_name)
        except KeyError as exc:
            # ❌ Unknown tools cannot run, but the attempted call is still recorded.
            message = str(exc)

            self._record(
                tool_name=tool_call.tool_name,
                success=False,
                message=message,
            )

            return ToolResult(
                success=False,
                error=message,
            )

        # 2️⃣ Check whether this tool can run automatically, needs approval, or is blocked.
        decision = self.permission_kernel.check(tool_call.tool_name)

        if decision.requires_approval:
            # 🙋 Stop here until a person has approved the action.
            self._record(
                tool_name=tool_call.tool_name,
                success=False,
                message=decision.reason,
            )

            return ToolResult(
                success=False,
                error=decision.reason,
            )

        if not decision.allowed:
            # 🚫 A blocked tool never reaches the safety check or its handler.
            self._record(
                tool_name=tool_call.tool_name,
                success=False,
                message=decision.reason,
            )

            return ToolResult(
                success=False,
                error=decision.reason,
            )

        # 3️⃣ Validate the call itself, such as ensuring a file stays in the workspace.
        safety_decision = self.safety.check(tool_call)

        if not safety_decision.safe:
            # 🛡️ Reject unsafe arguments before anything can change or read data.
            self._record(
                tool_name=tool_call.tool_name,
                success=False,
                message=safety_decision.reason,
            )

            return ToolResult(
                success=False,
                error=safety_decision.reason,
            )

        # 4️⃣ The call passed all gates, so run the tool with its supplied arguments.
        result = self.runtime.execute(
            tool,
            **tool_call.arguments,
        )

        # 📣 Turn the result into a clear audit message.
        message = (
            "Tool executed successfully."
            if result.success
            else result.error or "Tool execution failed."
        )

        # ✅/❌ Always finish by recording what actually happened.
        self._record(
            tool_name=tool_call.tool_name,
            success=result.success,
            message=message,
        )

        return result
