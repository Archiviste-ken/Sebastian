# 🚦 Tool execution coordinator
# This class runs a tool only after checking that it exists, is permitted,
# and is safe. Every outcome is saved to the audit trail.
# 📁 Import Path to handle default workspace locations.
from pathlib import Path

# 📦 Import the audit event model to record execution attempts.
from app.models.audit_event import AuditEvent
# 📦 Import the tool call model representing the requested operation.
from app.models.tool_call import ToolCall
# 📦 Import the result models used to wrap the output of a tool execution.
from app.models.tool_result import ToolResult, ToolResultStatus
# 🔐 Import the permission kernel to enforce authorization rules.
from app.security.permissions import PermissionKernel
# 🛡️ Import the tool safety module to perform bounds and sanity checks.
from app.security.safety import ToolSafety
# 🧾 Import the audit recorder to persist the trail of execution outcomes.
from app.tools.audit import AuditRecorder
# ⚙️ Import the execution context to provide environment state to tools.
from app.tools.context import ExecutionContext
# 🗂️ Import the tool registry to look up handlers by name.
from app.tools.registry import ToolRegistry
# 🔌 Import the tool runtime to invoke the underlying python functions.
from app.tools.runtime import ToolRuntime


# 🚦 Define the primary coordinator class that orchestrates tool execution.
class ToolExecutor:
    # 🛠️ Initialize the executor with all required sub-systems.
    def __init__(
        # 🧍 Reference to the current instance.
        self,
        # 🗂️ The capability registry mapping names to definitions.
        registry: ToolRegistry,
        # 🔐 The policy engine checking if tools are permitted.
        permission_kernel: PermissionKernel,
        # 🛡️ The safety validator verifying arguments.
        safety: ToolSafety,
        # 🔌 The runtime engine that actually invokes the tools.
        runtime: ToolRuntime,
        # 🧾 The audit log where execution records are stored.
        audit_recorder: AuditRecorder,
        # ⚙️ Optional explicit execution context.
        context: ExecutionContext | None = None,
    ):
        # 🗂️ Store the injected registry dependency.
        self.registry = registry
        # 🔐 Store the injected permission kernel dependency.
        self.permission_kernel = permission_kernel
        # 🛡️ Store the injected safety validator dependency.
        self.safety = safety
        # 🔌 Store the injected runtime engine dependency.
        self.runtime = runtime
        # 🧾 Store the injected audit recorder dependency.
        self.audit_recorder = audit_recorder

        # ⚖️ Check if a specific execution context was provided.
        if context is not None:
            # ⚙️ Bind the explicit context to the instance.
            self.context = context
        # 🔄 Otherwise, build a default context from the safety workspace.
        else:
            # 🔍 Attempt to pull the workspace property from the safety object.
            workspace = getattr(
                # 🛡️ The target object to inspect.
                self.safety,
                # 🏷️ The name of the property to retrieve.
                "workspace",
                # 📁 Default to the current working directory if missing.
                Path.cwd(),
            )

            # ⚙️ Construct and store a new ExecutionContext instance.
            self.context = ExecutionContext(
                # 📁 Assign the resolved workspace path.
                workspace=workspace,
            )

    # 📝 Internal helper to encapsulate audit log recording logic.
    def _record(
        # 🧍 Reference to the current instance.
        self,
        # 🏷️ The name of the tool that was executed.
        tool_name: str,
        # ✅ Whether the execution was ultimately successful.
        success: bool,
        # 💬 A descriptive message summarizing the outcome.
        message: str,
    ) -> None:
        # 🧾 Delegate the storage action to the audit recorder.
        self.audit_recorder.record(
            # 📦 Construct a new AuditEvent object to record.
            AuditEvent(
                # 🏷️ Assign the tool name.
                tool_name=tool_name,
                # ✅ Assign the success boolean flag.
                success=success,
                # 💬 Assign the descriptive message.
                message=message,
            )
        )

    # 🚦 The primary public method to coordinate the full execution lifecycle.
    def execute(self, tool_call: ToolCall) -> ToolResult:
        # 🛡️ Wrap the registry lookup in a try block to handle unknown tools.
        try:
            # 🔍 Look up the tool definition from the registry by its name.
            tool = self.registry.get(tool_call.tool_name)

        # ⚠️ Catch the KeyError raised if the tool is not found.
        except KeyError as exc:
            # 💬 Extract the error message as a string.
            message = str(exc)

            # 📝 Record the lookup failure in the audit log.
            self._record(
                # 🏷️ The requested name that failed.
                tool_name=tool_call.tool_name,
                # 🔴 Mark the attempt as failed.
                success=False,
                # 💬 Provide the lookup error message.
                message=message,
            )

            # 🔴 Return a failure result directly.
            return ToolResult(
                # 🚫 Indicate that the tool failed outright.
                status=ToolResultStatus.FAILED,
                # 💬 Attach the specific error message.
                error=message,
            )

        # 🔐 Ask the permission kernel for a decision on this tool.
        decision = self.permission_kernel.check(
            # 🏷️ The name of the tool to verify.
            tool_call.tool_name,
        )

        # ⚖️ Check if the decision mandates user approval before proceeding.
        if decision.requires_approval:
            # 📝 Record the pause for approval in the audit log.
            self._record(
                # 🏷️ The name of the tool waiting for approval.
                tool_name=tool_call.tool_name,
                # 🔴 Mark as unsuccessful for now (it hasn't run yet).
                success=False,
                # 💬 Record the reason approval is needed.
                message=decision.reason,
            )

            # ⏸️ Return a special result indicating we are blocked on user input.
            return ToolResult(
                # 🟡 Indicate the tool requires approval.
                status=ToolResultStatus.WAITING_APPROVAL,
                # 💬 Return the explanation of why approval is needed.
                error=decision.reason,
            )

        # ⚖️ Check if the decision explicitly blocks execution.
        if not decision.allowed:
            # 📝 Record the blocked attempt in the audit log.
            self._record(
                # 🏷️ The name of the blocked tool.
                tool_name=tool_call.tool_name,
                # 🔴 Mark the attempt as failed.
                success=False,
                # 💬 Record the reason it was blocked.
                message=decision.reason,
            )

            # 🚫 Return a result indicating the tool was blocked by policy.
            return ToolResult(
                # 🔴 Indicate the policy block.
                status=ToolResultStatus.BLOCKED,
                # 💬 Attach the explanation for the block.
                error=decision.reason,
            )

        # 🛡️ Run the dynamic safety checks on the tool arguments.
        safety_decision = self.safety.check(tool_call)

        # ⚖️ Check if the safety checks found any violations.
        if not safety_decision.safe:
            # 📝 Record the safety failure in the audit log.
            self._record(
                # 🏷️ The name of the unsafe tool call.
                tool_name=tool_call.tool_name,
                # 🔴 Mark the attempt as failed.
                success=False,
                # 💬 Record the safety violation reason.
                message=safety_decision.reason,
            )

            # 🚫 Return a failure result based on safety grounds.
            return ToolResult(
                # 🔴 Indicate that execution failed.
                status=ToolResultStatus.FAILED,
                # 💬 Attach the specific safety reason.
                error=safety_decision.reason,
            )

        # 🔌 All checks passed; pass control to the runtime to invoke the handler.
        result = self.runtime.execute(
            # 🧩 The verified tool definition object.
            tool=tool,
            # 📦 The unchecked arguments requested by the caller.
            arguments=tool_call.arguments,
            # ⚙️ The execution context bound to this executor.
            context=self.context,
        )

        # 💬 Determine a sensible audit message based on the execution outcome.
        message = (
            # 🟢 Success case text.
            "Tool executed successfully."
            # ⚖️ Check if the runtime result was successful.
            if result.success
            # 🔴 Failure case text, preferring the explicit error if available.
            else result.error or "Tool execution failed."
        )

        # 📝 Record the final execution outcome in the audit log.
        self._record(
            # 🏷️ The name of the executed tool.
            tool_name=tool_call.tool_name,
            # ✅ Match the success flag to the runtime outcome.
            success=result.success,
            # 💬 Attach the summarized message.
            message=message,
        )

        # 🔄 Return the runtime's result back to the caller.
        return result