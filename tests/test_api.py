# 🧪 API integration tests
# These tests exercise the public HTTP layer and verify the task lifecycle endpoints work.

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.main import app, get_db
from app.db.models import Base


TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)

Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task():
    response = client.post(
        "/tasks",
        json={
            "id": "api-task-1",
            "goal": "Fix my Python project",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == "api-task-1"
    assert data["goal"] == "Fix my Python project"
    assert data["status"] == "pending"


def test_get_task():
    create_response = client.post(
        "/tasks",
        json={
            "id": "api-task-get",
            "goal": "Test task persistence",
        },
    )

    assert create_response.status_code == 200

    response = client.get("/tasks/api-task-get")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == "api-task-get"
    assert data["goal"] == "Test task persistence"
    assert data["status"] == "pending"


def test_get_missing_task():
    response = client.get("/tasks/does-not-exist")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"