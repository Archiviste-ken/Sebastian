import pytest
from pydantic import ValidationError

from app.core.task import Task, TaskStatus


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