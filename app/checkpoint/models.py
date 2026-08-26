"""Mutable execution state that can be checkpointed and resumed."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class TaskState:
    """Snapshot of task execution progress."""

    task_id: str
    status: str
    plan_goal: str | None = None
    current_action_index: int = 0
    completed_actions: list[str] = field(default_factory=list)
    failed_actions: list[str] = field(default_factory=list)
    results: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""

    def __post_init__(self) -> None:
        now = datetime.now(timezone.utc).isoformat()
        if not self.created_at:
            self.created_at = now
        if not self.updated_at:
            self.updated_at = now

    def touch(self) -> None:
        """Update the timestamp to now."""
        self.updated_at = datetime.now(timezone.utc).isoformat()
