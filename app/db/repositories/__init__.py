# 🧳 Repository package
# Contains persistence abstractions for the project domain models.
# This package is the bridge between the app's business logic and its SQLite storage.

from sqlalchemy.orm import Session

from app.db.models import TaskRecord
from app.models.task import Task


class TaskRepository:
    def __init__(self, session: Session):
        # 🔌 Keep the database session that this repository will use.
        self.session = session

    def create(self, task: Task) -> Task:
        # 💾 Convert the app task into a database row, then save it.
        record = TaskRecord(
            id=task.id,
            goal=task.goal,
            status=task.status.value,
        )

        self.session.add(record)
        self.session.commit()

        return task

    def get(self, task_id: str) -> Task | None:
        # 🔎 Find a stored row and turn it back into the app's Task model.
        record = self.session.get(TaskRecord, task_id)

        if record is None:
            return None

        return Task(
            id=record.id,
            goal=record.goal,
            status=record.status,
        )
