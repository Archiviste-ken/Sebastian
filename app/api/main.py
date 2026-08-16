from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.api.schemas import TaskCreateRequest
from app.db.database import SessionLocal
from app.db.repositories.task_repository import TaskRepository
from app.models.task import Task


app = FastAPI(
    title="Sebastian",
    version="0.1.0",
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/tasks")
def create_task(
    request: TaskCreateRequest,
    db: Session = Depends(get_db),
):
    task = Task(
        id=request.id,
        goal=request.goal,
    )

    repository = TaskRepository(db)
    repository.create(task)

    return task