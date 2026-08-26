"""Structured context that travels from intent to planning/execution."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class TaskContext:
    """Bounded, traceable snapshot of everything the planner needs to know."""

    user_request: str
    intent_goal: str
    intent_constraints: list[str]
    intent_forbidden_actions: list[str]
    intent_expected_outcome: str
    intent_success_criteria: list[str]
    intent_required_permissions: list[str]
    workspace_path: str
    workspace_files: list[str]
    available_tools: list[str]
    tool_permissions: dict[str, str] = field(default_factory=dict)
    prior_results: list[dict[str, Any]] = field(default_factory=list)
    execution_history: list[dict[str, Any]] = field(default_factory=list)
