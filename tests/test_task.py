# 🧪 Task lifecycle tests
# Ensures the project state machine behaves as designed for planning, execution, and recovery.

import pytest
from pydantic import ValidationError
from app.models.task import (
    Task,
    TaskStatus,
    can_transition,
)
from app.models.task import Task, TaskStatus


def test_task_defaults_to_pending():
    task = Task(
        id="task-1",
        goal="Fix this Python project",
    )

    assert task.status == TaskStatus.PENDING


def test_all_task_statuses_exist():
    expected_statuses = {
        "pending",
        "planning",
        "waiting_approval",
        "executing",
        "paused",
        "verifying",
        "recovering",
        "completed",
        "failed",
        "cancelled",
    }

    actual_statuses = {status.value for status in TaskStatus}

    assert actual_statuses == expected_statuses


def test_task_rejects_empty_goal():
    with pytest.raises(ValidationError):
        Task(
            id="task-2",
            goal="",
        )


def test_valid_transition():
    assert can_transition(
        TaskStatus.PENDING,
        TaskStatus.PLANNING,
    )


def test_invalid_transition():
    assert not can_transition(
        TaskStatus.COMPLETED,
        TaskStatus.EXECUTING,
    )