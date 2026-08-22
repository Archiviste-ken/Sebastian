# 🧪 Repository test
# Confirms tasks can be created and retrieved from the database layer.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models import Base
from app.db.repositories.task_repository import TaskRepository
from app.models.task import Task, TaskStatus


def test_create_and_get_task():
    engine = create_engine("sqlite:///:memory:")

    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(bind=engine)

    with SessionLocal() as session:
        repository = TaskRepository(session)

        task = Task(
            id="task-1",
            goal="Fix my Python project",
        )

        repository.create(task)

        retrieved = repository.get("task-1")

        assert retrieved is not None
        assert retrieved.id == "task-1"
        assert retrieved.goal == "Fix my Python project"
        assert retrieved.status == TaskStatus.PENDING