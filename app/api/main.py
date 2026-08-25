# 🌐 FastAPI entrypoint
# 🌐 This is the public HTTP layer for Sebastian.
# 🌐 It exposes the core task API and ensures the database schema is ready at startup.

from contextlib import asynccontextmanager  # 📦 Import asynccontextmanager to manage app lifecycle

from fastapi import Depends, FastAPI, HTTPException  # 📦 Import FastAPI framework and its dependencies/exceptions
from sqlalchemy.orm import Session  # 📦 Import Session for database transactions

from app.api.schemas import TaskCreateRequest  # 📦 Import the TaskCreateRequest schema for input validation
from app.db.database import SessionLocal, create_tables  # 📦 Import DB session factory and schema initialization function
from app.db.repositories.task_repository import TaskRepository  # 📦 Import TaskRepository for database operations
from app.models.task import Task  # 📦 Import the domain Task model


@asynccontextmanager  # 🔧 Decorator to define the lifespan context manager for the FastAPI app
async def lifespan(app: FastAPI):  # 🚀 Lifespan function that runs on startup and shutdown
    # 🏗️ Ensure the SQL schema exists whenever the app starts.
    create_tables()  # 💾 Create database tables if they do not exist
    yield  # 🚀 Yield control to the FastAPI application


app = FastAPI(  # 🚀 Initialize the FastAPI application instance
    title="Sebastian",  # 📝 Set the API title
    version="0.1.0",  # 📝 Set the API version
    lifespan=lifespan,  # 🚀 Attach the lifespan manager to the app
)  # 🚀 Close the FastAPI initialization


def get_db():  # 🔧 Dependency function to yield a database session
    # 🔌 Create a per-request database session and close it afterward.
    db = SessionLocal()  # 💾 Instantiate a new database session

    try:  # 🛡️ Start a try block to ensure the session is always closed
        yield db  # 🔌 Yield the session to the path operation
    finally:  # 🛡️ Finally block executes after the request is processed
        db.close()  # 🔌 Close the database session to release resources


@app.get("/health")  # 📡 Define a GET endpoint for health checks
def health_check():  # 📡 Handler function for the health check endpoint
    # ❤️ Lightweight liveness check for deployment or smoke testing.
    return {"status": "ok"}  # ✅ Return a simple JSON response indicating the app is healthy


@app.post("/tasks")  # 📡 Define a POST endpoint to create a new task
def create_task(  # 📡 Handler function for task creation
    request: TaskCreateRequest,  # 📝 Parse and validate the request body against TaskCreateRequest
    db: Session = Depends(get_db),  # 🔌 Inject the database session using the get_db dependency
):  # 📡 Close the function signature
    # 🧠 Turn the API request into a domain task and persist it.
    task = Task(  # 🏗️ Instantiate a new domain Task object
        id=request.id,  # 📝 Map the requested ID to the task
        goal=request.goal,  # 📝 Map the requested goal to the task
    )  # 🏗️ Close Task instantiation

    repository = TaskRepository(db)  # 💾 Instantiate the TaskRepository with the DB session
    repository.create(task)  # 💾 Persist the new task in the database

    return task  # ✅ Return the created task as the API response


@app.get("/tasks/{task_id}")  # 📡 Define a GET endpoint to retrieve a task by ID
def get_task(  # 📡 Handler function for fetching a task
    task_id: str,  # 📝 Capture the task_id from the URL path
    db: Session = Depends(get_db),  # 🔌 Inject the database session
):  # 📡 Close the function signature
    # 🔎 Fetch a task by ID and return 404 if it does not exist.
    repository = TaskRepository(db)  # 💾 Instantiate the TaskRepository
    task = repository.get(task_id)  # 🔎 Query the repository for the task

    if task is None:  # 🛡️ Check if the task was not found
        raise HTTPException(  # ❌ Raise an HTTP exception
            status_code=404,  # ❌ Set the HTTP status code to 404 Not Found
            detail="Task not found",  # ❌ Provide an error detail message
        )  # ❌ Close the exception instantiation

    return task  # ✅ Return the found task as the API response