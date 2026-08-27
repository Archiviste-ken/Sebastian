"""Sebastian: top-level orchestrator for V1.

Wires the complete pipeline:
  User request → Intent → Context → Plan → ActionExecutor → Verification
  → Recovery → Checkpoint → TaskReport

The LLM proposes (intent, argument resolution).
The deterministic system validates, authorizes, executes, verifies, and records.
"""

from dataclasses import dataclass, field
from pathlib import Path
from uuid import uuid4

from app.checkpoint.store import CheckpointStore
from app.context.compiler import ContextCompiler
from app.execution.action_executor import ActionExecutor
from app.execution.models import ExecutionReport
from app.intent.engine import IntentEngine
from app.llm.gateway import ModelGateway
from app.models.audit_event import AuditEvent
from app.planning.argument_resolver import ArgumentResolver
from app.planning.compiler import PlanCompiler
from app.planning.planner import Planner
from app.planning.selector import CapabilitySelector
from app.recovery.engine import RecoveryEngine
from app.security.permissions import PermissionKernel, PermissionLevel
from app.security.safety import ToolSafety
from app.tools.audit import AuditRecorder
from app.tools.builtin.command import run_command
from app.tools.builtin.filesystem import (
    create_directory,
    list_directory,
    move_file,
    read_file,
    write_file,
)
from app.tools.builtin.git import git_diff, git_log, git_status
from app.tools.builtin.python import run_python
from app.tools.context import ExecutionContext
from app.tools.definition import ToolDefinition
from app.tools.executor import ToolExecutor
from app.tools.registry import ToolRegistry
from app.tools.runtime import ToolRuntime
from app.verification.engine import VerificationEngine


from app.response.models import FinalResponse

@dataclass
class TaskReport:
    """Final outcome returned to the caller after a full run."""

    task_id: str
    success: bool
    goal: str
    plan_goal: str
    execution: ExecutionReport
    audit_events: list[AuditEvent] = field(default_factory=list)
    missing_information: list[str] = field(default_factory=list)
    response: FinalResponse | None = None


# Default permission mapping for all builtin tools.
DEFAULT_PERMISSIONS: dict[str, PermissionLevel] = {
    "read_file": PermissionLevel.AUTONOMOUS,
    "list_directory": PermissionLevel.AUTONOMOUS,
    "write_file": PermissionLevel.APPROVAL,
    "create_directory": PermissionLevel.APPROVAL,
    "move_file": PermissionLevel.APPROVAL,
    "run_command": PermissionLevel.APPROVAL,
    "run_python": PermissionLevel.APPROVAL,
    "git_status": PermissionLevel.AUTONOMOUS,
    "git_diff": PermissionLevel.AUTONOMOUS,
    "git_log": PermissionLevel.AUTONOMOUS,
}


class Sebastian:
    """Top-level agent that composes all V1 subsystems.

    Usage::

        agent = Sebastian(workspace=Path("."), gateway=GroqModelGateway(...))
        report = agent.run("Read the file README.md")
    """

    def __init__(
        self,
        workspace: Path,
        gateway: ModelGateway,
        permissions: dict[str, PermissionLevel] | None = None,
        max_actions: int = 50,
    ):
        self._workspace = workspace.resolve()

        # Phase 1 — Tool infrastructure
        self._registry = ToolRegistry()
        self._register_builtins()
        self._permission_kernel = PermissionKernel(permissions or DEFAULT_PERMISSIONS)
        self._safety = ToolSafety(workspace=self._workspace)
        self._runtime = ToolRuntime()
        self._audit = AuditRecorder()
        self._context = ExecutionContext(workspace=self._workspace)
        self._tool_executor = ToolExecutor(
            registry=self._registry,
            permission_kernel=self._permission_kernel,
            safety=self._safety,
            runtime=self._runtime,
            audit_recorder=self._audit,
            context=self._context,
        )

        # Phase 2 — LLM
        self._intent_engine = IntentEngine(gateway)

        # Phase 3 — Context
        self._context_compiler = ContextCompiler(
            registry=self._registry,
            permission_kernel=self._permission_kernel,
            workspace=self._workspace,
        )

        # Phase 4 — Planning (existing keyword-based selector, no LLM planning)
        self._planner = Planner(selector=CapabilitySelector())
        self._compiler = PlanCompiler(registry=self._registry)
        self._arg_resolver = ArgumentResolver(gateway)

        # Phase 6 — Verification
        self._verification_engine = VerificationEngine()

        # Phase 7 — Recovery
        self._recovery_engine = RecoveryEngine()

        # Phase 8 — Checkpoint
        self._checkpoint_store = CheckpointStore()

        # Phase 5+9 — Action Executor (delegates to ToolExecutor)
        self._action_executor = ActionExecutor(
            tool_executor=self._tool_executor,
            verification_engine=self._verification_engine,
            recovery_engine=self._recovery_engine,
            checkpoint_store=self._checkpoint_store,
            max_actions=max_actions,
        )
        from app.response.generator import ResponseGenerator
        self._response_generator = ResponseGenerator(gateway)

    # ── public API ────────────────────────────────────────────────────

    def _finalize(self, request: str, report: TaskReport) -> TaskReport:
        try:
            report.response = self._response_generator.generate(request, report)
        except Exception as e:
            # Fallback if generator fails
            from app.response.models import FinalResponse
            report.response = FinalResponse(status="failure", answer=f"Failed to generate response: {e}")
        return report

    def run(self, request: str) -> TaskReport:
        """Execute a natural-language request through the full V1 pipeline."""
        task_id = str(uuid4())

        # Phase 2: Intent extraction (LLM)
        intent = self._intent_engine.parse(request)

        # Stop safely if information is genuinely missing
        if intent.missing_information:
            return self._finalize(request, TaskReport(
                task_id=task_id,
                success=False,
                goal=intent.goal,
                plan_goal="Pending Information",
                execution=ExecutionReport(
                    task_id=task_id, success=False, actions_completed=0, actions_failed=0, actions_total=0, reason="Missing information"
                ),
                audit_events=[],
                missing_information=intent.missing_information,
            ))

        # Phase 3: Context compilation (deterministic)
        self._context_compiler.compile(
            user_request=request,
            intent=intent,
        )

        try:
            # Phase 4: Plan generation (deterministic keyword selector)
            plan = self._planner.build(intent)
        except ValueError as e:
            # Handle cases where no capabilities are found
            return self._finalize(request, TaskReport(
                task_id=task_id,
                success=False,
                goal=intent.goal,
                plan_goal="Planning Failed",
                execution=ExecutionReport(
                    task_id=task_id, success=False, actions_completed=0, actions_failed=0, actions_total=0, reason=str(e)
                ),
                audit_events=[],
            ))

        # Resolve arguments for each action via LLM (existing Phase 4 infra)
        resolved_actions = []
        for action in plan.actions:
            try:
                tool_def = self._registry.get(action.tool)
                if tool_def.argument_schema is not None:
                    args = self._arg_resolver.resolve(intent=intent, tool=tool_def)
                    action = action.model_copy(update={"arguments": args})
                    # Validate arguments against schema
                    self._compiler.compile(action)
            except (KeyError, ValueError):
                # Unknown tool or invalid args — ActionExecutor will handle
                # the failure cleanly via ToolExecutor → audit.
                pass
            resolved_actions.append(action)

        resolved_plan = plan.model_copy(update={"actions": resolved_actions})

        # Phase 5: Execute plan (delegates each ToolCall to ToolExecutor)
        report = self._action_executor.execute_plan(
            task_id=task_id,
            plan=resolved_plan,
            workspace=self._workspace,
        )

        return self._finalize(request, TaskReport(
            task_id=task_id,
            success=report.success,
            goal=intent.goal,
            plan_goal=plan.goal,
            execution=report,
            audit_events=list(self._audit.events()),
        ))

    def cancel(self, task_id: str) -> None:
        """Cancel a running task by ID."""
        self._action_executor.cancel(task_id)

    # ── builtin tool registration ─────────────────────────────────────

    def _register_builtins(self) -> None:
        tools = [
            ToolDefinition(
                name="read_file",
                description="Read the contents of a text file.",
                handler=read_file,
                argument_schema={
                    "type": "object",
                    "properties": {"path": {"type": "string"}},
                    "required": ["path"],
                },
            ),
            ToolDefinition(
                name="list_directory",
                description="List the contents of a directory.",
                handler=list_directory,
                argument_schema={
                    "type": "object",
                    "properties": {"path": {"type": "string"}},
                    "required": ["path"],
                },
            ),
            ToolDefinition(
                name="write_file",
                description="Write text content to a file.",
                handler=write_file,
                argument_schema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "content": {"type": "string"},
                    },
                    "required": ["path", "content"],
                },
            ),
            ToolDefinition(
                name="create_directory",
                description="Create a directory.",
                handler=create_directory,
                argument_schema={
                    "type": "object",
                    "properties": {"path": {"type": "string"}},
                    "required": ["path"],
                },
            ),
            ToolDefinition(
                name="move_file",
                description="Move a file from one path to another.",
                handler=move_file,
                argument_schema={
                    "type": "object",
                    "properties": {
                        "source": {"type": "string"},
                        "destination": {"type": "string"},
                    },
                    "required": ["source", "destination"],
                },
            ),
            ToolDefinition(
                name="run_command",
                description="Run an approved shell command.",
                handler=run_command,
                argument_schema={
                    "type": "object",
                    "properties": {
                        "command": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["command"],
                },
            ),
            ToolDefinition(
                name="run_python",
                description="Run a Python script inside the workspace.",
                handler=run_python,
                argument_schema={
                    "type": "object",
                    "properties": {"script": {"type": "string"}},
                    "required": ["script"],
                },
            ),
            ToolDefinition(
                name="git_status",
                description="Inspect the current Git working tree.",
                handler=git_status,
                uses_context=True,
            ),
            ToolDefinition(
                name="git_diff",
                description="Inspect the current Git diff.",
                handler=git_diff,
                uses_context=True,
            ),
            ToolDefinition(
                name="git_log",
                description="Inspect recent Git commits.",
                handler=git_log,
                uses_context=True,
            ),
        ]
        for tool in tools:
            self._registry.register(tool)
