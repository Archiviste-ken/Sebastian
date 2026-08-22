# 🧵 Task lifecycle model
# A task represents the user's objective and the current execution phase.
# Sebastian moves through states such as planning, execution, verification, and recovery.

from enum import Enum

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    # ⏳ New task waiting to begin.
    PENDING = "pending"

    # 🧠 Task is being reasoned about and planned.
    PLANNING = "planning"

    # 🛑 Waiting for explicit approval before continuing.
    WAITING_APPROVAL = "waiting_approval"

    # ⚙️ Task is actively running actions.
    EXECUTING = "executing"

    # ⏸️ Work has been paused.
    PAUSED = "paused"

    # ✅ Result is being checked against evidence.
    VERIFYING = "verifying"

    # 🔁 Failure is being diagnosed and the task is re-planned.
    RECOVERING = "recovering"

    # 🏁 The task finished successfully.
    COMPLETED = "completed"

    # ❌ The task failed and reached a terminal state.
    FAILED = "failed"

    # 🚫 The task was cancelled.
    CANCELLED = "cancelled"


class Task(BaseModel):
    # 🆔 Unique task identifier.
    id: str

    # 🎯 User's desired outcome.
    goal: str = Field(min_length=1)

    # 🔄 Current execution state.
    status: TaskStatus = TaskStatus.PENDING


VALID_TRANSITIONS: dict[TaskStatus, set[TaskStatus]] = {
    # PENDING can begin work or be cancelled.
    TaskStatus.PENDING: {
        TaskStatus.PLANNING,
        TaskStatus.CANCELLED,
    },

    # PLANNING can move into approval, execution, or cancellation.
    TaskStatus.PLANNING: {
        TaskStatus.WAITING_APPROVAL,
        TaskStatus.EXECUTING,
        TaskStatus.CANCELLED,
    },

    # WAITING_APPROVAL may proceed or stop.
    TaskStatus.WAITING_APPROVAL: {
        TaskStatus.EXECUTING,
        TaskStatus.CANCELLED,
    },

    # EXECUTING may pause, verify, recover, fail, or cancel.
    TaskStatus.EXECUTING: {
        TaskStatus.PAUSED,
        TaskStatus.VERIFYING,
        TaskStatus.RECOVERING,
        TaskStatus.FAILED,
        TaskStatus.CANCELLED,
    },

    # PAUSED can resume or be cancelled.
    TaskStatus.PAUSED: {
        TaskStatus.EXECUTING,
        TaskStatus.CANCELLED,
    },

    # VERIFYING can finish, recover, or fail.
    TaskStatus.VERIFYING: {
        TaskStatus.COMPLETED,
        TaskStatus.RECOVERING,
        TaskStatus.FAILED,
    },

    # RECOVERING can re-plan, resume execution, or fail.
    TaskStatus.RECOVERING: {
        TaskStatus.PLANNING,
        TaskStatus.EXECUTING,
        TaskStatus.FAILED,
    },

    # Terminal states do not transition onward.
    TaskStatus.COMPLETED: set(),
    TaskStatus.FAILED: set(),
    TaskStatus.CANCELLED: set(),
}


def can_transition(
    current: TaskStatus,
    target: TaskStatus,
) -> bool:
    # 🧭 Check if the next state is allowed in the lifecycle model.
    return target in VALID_TRANSITIONS[current]