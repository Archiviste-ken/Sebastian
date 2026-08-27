"""Data containers for action execution outcomes."""

from dataclasses import dataclass, field

from app.models.tool_result import ToolResult
from app.verification.models import VerificationResult


@dataclass
class ActionOutcome:
    """Result of executing and verifying a single plan action."""

    action_id: str
    tool_name: str
    tool_result: ToolResult
    verification: VerificationResult
    recovery_attempts: int = 0


@dataclass
class ExecutionReport:
    """Summary of executing an entire plan."""

    task_id: str
    success: bool
    actions_completed: int
    actions_failed: int
    actions_total: int
    outcomes: list[ActionOutcome] = field(default_factory=list)
    cancelled: bool = False
    reason: str = ""
