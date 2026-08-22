# 🌐 FastAPI entrypoint
# This is the public HTTP layer for Sebastian.
# It exposes the core task API and ensures the database schema is ready at startup.

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.api.schemas import TaskCreateRequest
from app.db.database import SessionLocal, create_tables
from app.db.repositories.task_repository import TaskRepository
from app.models.task import Task


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🏗️ Ensure the SQL schema exists whenever the app starts.
    create_tables()
    yield


app = FastAPI(
    title="Sebastian",
    version="0.1.0",
    lifespan=lifespan,
)


def get_db():
    # 🔌 Create a per-request database session and close it afterward.
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health_check():
    # ❤️ Lightweight liveness check for deployment or smoke testing.
    return {"status": "ok"}


@app.post("/tasks")
def create_task(
    request: TaskCreateRequest,
    db: Session = Depends(get_db),
):
    # 🧠 Turn the API request into a domain task and persist it.
    task = Task(
        id=request.id,
        goal=request.goal,
    )

    repository = TaskRepository(db)
    repository.create(task)

    return task


@app.get("/tasks/{task_id}")
def get_task(
    task_id: str,
    db: Session = Depends(get_db),
):
    # 🔎 Fetch a task by ID and return 404 if it does not exist.
    repository = TaskRepository(db)
    task = repository.get(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return task