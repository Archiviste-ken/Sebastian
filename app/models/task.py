# 🧵 Task lifecycle model
# 🎯 A task represents the user's objective and the current execution phase.
# 🔄 Sebastian moves through states such as planning, execution, verification, and recovery.

# 📦 Import Enum for creating enumeration classes.
from enum import Enum

# 📦 Import BaseModel and Field from pydantic for data modeling and validation.
from pydantic import BaseModel, Field


# 🏷️ Define TaskStatus enum, inheriting from str and Enum for string-based enumeration.
class TaskStatus(str, Enum):
    # ⏳ New task waiting to begin.
    # 🔄 Represents the pending state.
    PENDING = "pending"

    # 🧠 Task is being reasoned about and planned.
    # 🔄 Represents the planning state.
    PLANNING = "planning"

    # 🛑 Waiting for explicit approval before continuing.
    # 🛡️ Represents the waiting approval state.
    WAITING_APPROVAL = "waiting_approval"

    # ⚙️ Task is actively running actions.
    # 🔄 Represents the executing state.
    EXECUTING = "executing"

    # ⏸️ Work has been paused.
    # 🔄 Represents the paused state.
    PAUSED = "paused"

    # ✅ Result is being checked against evidence.
    # 🔄 Represents the verifying state.
    VERIFYING = "verifying"

    # 🔁 Failure is being diagnosed and the task is re-planned.
    # 🔄 Represents the recovering state.
    RECOVERING = "recovering"

    # 🏁 The task finished successfully.
    # ✅ Represents the completed state.
    COMPLETED = "completed"

    # ❌ The task failed and reached a terminal state.
    # ❌ Represents the failed state.
    FAILED = "failed"

    # 🚫 The task was cancelled.
    # ❌ Represents the cancelled state.
    CANCELLED = "cancelled"


# 🏷️ Define the Task class, inheriting from BaseModel.
class Task(BaseModel):
    # 🆔 Unique task identifier.
    # 📝 Represents the string ID of the task.
    id: str

    # 🎯 User's desired outcome.
    # 🔧 Uses Field to enforce a minimum length of 1 character for the goal.
    goal: str = Field(min_length=1)

    # 🔄 Current execution state.
    # 🔧 Defaults to TaskStatus.PENDING when a new task is created.
    status: TaskStatus = TaskStatus.PENDING


# 📍 Dictionary mapping each state to its allowed subsequent states.
# 🔄 Defines the valid transitions within the task lifecycle.
VALID_TRANSITIONS: dict[TaskStatus, set[TaskStatus]] = {
    # ⏳ PENDING can begin work or be cancelled.
    # 🔄 Valid next states for PENDING.
    TaskStatus.PENDING: {
        TaskStatus.PLANNING,
        TaskStatus.CANCELLED,
    },

    # 🧠 PLANNING can move into approval, execution, or cancellation.
    # 🔄 Valid next states for PLANNING.
    TaskStatus.PLANNING: {
        TaskStatus.WAITING_APPROVAL,
        TaskStatus.EXECUTING,
        TaskStatus.CANCELLED,
    },

    # 🛑 WAITING_APPROVAL may proceed or stop.
    # 🛡️ Valid next states for WAITING_APPROVAL.
    TaskStatus.WAITING_APPROVAL: {
        TaskStatus.EXECUTING,
        TaskStatus.CANCELLED,
    },

    # ⚙️ EXECUTING may pause, verify, recover, fail, or cancel.
    # 🔄 Valid next states for EXECUTING.
    TaskStatus.EXECUTING: {
        TaskStatus.PAUSED,
        TaskStatus.VERIFYING,
        TaskStatus.RECOVERING,
        TaskStatus.FAILED,
        TaskStatus.CANCELLED,
    },

    # ⏸️ PAUSED can resume or be cancelled.
    # 🔄 Valid next states for PAUSED.
    TaskStatus.PAUSED: {
        TaskStatus.EXECUTING,
        TaskStatus.CANCELLED,
    },

    # ✅ VERIFYING can finish, recover, or fail.
    # 🔄 Valid next states for VERIFYING.
    TaskStatus.VERIFYING: {
        TaskStatus.COMPLETED,
        TaskStatus.RECOVERING,
        TaskStatus.FAILED,
    },

    # 🔁 RECOVERING can re-plan, resume execution, or fail.
    # 🔄 Valid next states for RECOVERING.
    TaskStatus.RECOVERING: {
        TaskStatus.PLANNING,
        TaskStatus.EXECUTING,
        TaskStatus.FAILED,
    },

    # 🏁 Terminal states do not transition onward.
    # ✅ COMPLETED has no further transitions.
    TaskStatus.COMPLETED: set(),
    # ❌ FAILED has no further transitions.
    TaskStatus.FAILED: set(),
    # ❌ CANCELLED has no further transitions.
    TaskStatus.CANCELLED: set(),
}


# 🎯 Function to determine if a state transition is allowed.
# 🏷️ Takes the current TaskStatus and the target TaskStatus as inputs.
def can_transition(
    current: TaskStatus,
    target: TaskStatus,
) -> bool:
    # 🧭 Check if the next state is allowed in the lifecycle model.
    # ✅ Returns True if the target state is in the allowed transitions for the current state.
    return target in VALID_TRANSITIONS[current]