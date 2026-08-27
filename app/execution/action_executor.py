"""ActionExecutor: orchestrates a Plan by delegating each ToolCall to ToolExecutor.

KEY ARCHITECTURAL CONSTRAINT:
  ActionExecutor NEVER duplicates permission, safety, runtime, or audit logic.
  It builds a ToolCall from each Action and delegates to the existing ToolExecutor,
  which owns the full pipeline: registry → permission → safety → runtime → audit.
"""

import threading
from pathlib import Path

from app.checkpoint.models import TaskState
from app.checkpoint.store import CheckpointStore
from app.execution.models import ActionOutcome, ExecutionReport
from app.models.task import TaskStatus
from app.models.tool_call import ToolCall
from app.planning.models import Plan
from app.recovery.engine import RecoveryEngine
from app.recovery.models import RecoveryStrategy
from app.tools.executor import ToolExecutor
from app.verification.engine import VerificationEngine
from app.verification.models import VerificationStatus

DEFAULT_MAX_ACTIONS = 50


class ActionExecutor:
    """Iterates plan actions, delegating each to ToolExecutor.

    Adds: verification, recovery, checkpointing, cancellation, action limits.
    Does NOT add: permission checks, safety checks, audit recording (ToolExecutor does those).
    """

    def __init__(
        self,
        tool_executor: ToolExecutor,
        verification_engine: VerificationEngine,
        recovery_engine: RecoveryEngine,
        checkpoint_store: CheckpointStore,
        max_actions: int = DEFAULT_MAX_ACTIONS,
    ):
        self._tool_executor = tool_executor
        self._verification_engine = verification_engine
        self._recovery_engine = recovery_engine
        self._checkpoint_store = checkpoint_store
        self._max_actions = max_actions
        self._cancel_flags: dict[str, bool] = {}
        self._lock = threading.Lock()

    # ── cancellation ──────────────────────────────────────────────────
    def cancel(self, task_id: str) -> None:
        with self._lock:
            self._cancel_flags[task_id] = True

    def _is_cancelled(self, task_id: str) -> bool:
        with self._lock:
            return self._cancel_flags.get(task_id, False)

    # ── main entry point ──────────────────────────────────────────────
    def execute_plan(
        self,
        task_id: str,
        plan: Plan,
        workspace: Path,
    ) -> ExecutionReport:
        outcomes: list[ActionOutcome] = []
        completed = 0
        failed = 0
        actions = plan.actions
        total = len(actions)

        # Initialise checkpoint.
        state = TaskState(
            task_id=task_id,
            status=TaskStatus.EXECUTING.value,
            plan_goal=plan.goal,
        )
        self._checkpoint_store.save(state)

        for index, action in enumerate(actions):
            # ── cancellation gate ─────────────────────────────────────
            if self._is_cancelled(task_id):
                state.status = TaskStatus.CANCELLED.value
                self._checkpoint_store.save(state)
                return ExecutionReport(
                    task_id=task_id,
                    success=False,
                    actions_completed=completed,
                    actions_failed=failed,
                    actions_total=total,
                    outcomes=outcomes,
                    cancelled=True,
                    reason="Task was cancelled.",
                )

            # ── action-limit gate ─────────────────────────────────────
            if completed + failed >= self._max_actions:
                state.status = TaskStatus.FAILED.value
                self._checkpoint_store.save(state)
                return ExecutionReport(
                    task_id=task_id,
                    success=False,
                    actions_completed=completed,
                    actions_failed=failed,
                    actions_total=total,
                    outcomes=outcomes,
                    cancelled=False,
                    reason=f"Action limit ({self._max_actions}) reached.",
                )

            # ── execute with bounded recovery loop ────────────────────
            attempt_count = 0
            action_succeeded = False

            while True:
                tool_call = ToolCall(
                    tool_name=action.tool,
                    arguments=action.arguments,
                )

                # DELEGATE to existing ToolExecutor — all permission,
                # safety, runtime, and audit logic lives there.
                tool_result = self._tool_executor.execute(tool_call)

                verification = self._verification_engine.verify(
                    action=action,
                    tool_result=tool_result,
                    workspace=workspace,
                )

                if verification.status == VerificationStatus.PASS:
                    action_succeeded = True
                    break

                # UNCERTAIN with a successful tool → accept cautiously.
                if (
                    verification.status == VerificationStatus.UNCERTAIN
                    and tool_result.success
                ):
                    action_succeeded = True
                    break

                # FAIL or UNCERTAIN-with-failure → attempt recovery.
                recovery = self._recovery_engine.attempt(
                    action=action,
                    tool_result=tool_result,
                    attempt_count=attempt_count,
                )
                attempt_count += 1

                if recovery.strategy == RecoveryStrategy.RETRY:
                    continue
                # FAIL or SKIP → break out.
                break

            outcome = ActionOutcome(
                action_id=action.action_id,
                tool_name=action.tool,
                tool_result=tool_result,
                verification=verification,
                recovery_attempts=attempt_count,
            )
            outcomes.append(outcome)

            if action_succeeded:
                completed += 1
                state.completed_actions.append(action.action_id)
            else:
                failed += 1
                state.failed_actions.append(action.action_id)
                # Stop on first failure — subsequent actions likely
                # depend on this one and would also fail.
                state.status = TaskStatus.FAILED.value
                state.current_action_index = index + 1
                state.results[action.action_id] = {
                    "status": tool_result.status.value,
                    "success": tool_result.success,
                    "error": tool_result.error,
                }
                self._checkpoint_store.save(state)
                return ExecutionReport(
                    task_id=task_id,
                    success=False,
                    actions_completed=completed,
                    actions_failed=failed,
                    actions_total=total,
                    outcomes=outcomes,
                    cancelled=False,
                    reason=f"Action '{action.action_id}' failed.",
                )

            # Update checkpoint after each successful action.
            state.current_action_index = index + 1
            state.results[action.action_id] = {
                "status": tool_result.status.value,
                "success": tool_result.success,
                "error": tool_result.error,
            }
            self._checkpoint_store.save(state)

        # All actions completed successfully.
        state.status = TaskStatus.COMPLETED.value
        self._checkpoint_store.save(state)

        return ExecutionReport(
            task_id=task_id,
            success=True,
            actions_completed=completed,
            actions_failed=failed,
            actions_total=total,
            outcomes=outcomes,
            cancelled=False,
            reason="All actions completed successfully.",
        )
