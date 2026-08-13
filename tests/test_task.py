import pytest
from pydantic import ValidationError

from app.models.task import Task, TaskStatus


def test_task_defaults_to_pending():
    task = Task(
        id="task-1",
        goal="Fix this Python project",
    )

    assert task.status == TaskStatus.PENDING


def test_task_rejects_empty_goal():
    with pytest.raises(ValidationError):
        Task(
            id="task-2",
            goal="",
        )