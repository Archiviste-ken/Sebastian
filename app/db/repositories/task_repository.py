# 🧳 Task repository
# This repository handles task persistence between the domain model and SQLite.

from sqlalchemy.orm import Session

from app.db.models import TaskRecord
from app.models.task import Task


class TaskRepository:
    def __init__(self, session: Session):
        # 🧵 SQLAlchemy session used for database operations.
        self.session = session

    def create(self, task: Task) -> Task:
        # 📝 Convert the domain task into a database record and save it.
        record = TaskRecord(
            id=task.id,
            goal=task.goal,
            status=task.status.value,
        )

        self.session.add(record)
        self.session.commit()

        return task

    def get(self, task_id: str) -> Task | None:
        # 🔎 Retrieve a task by ID and convert it back into a domain object.
        record = self.session.get(TaskRecord, task_id)

        if record is None:
            return None

        return Task(
            id=record.id,
            goal=record.goal,
            status=record.status,
        )