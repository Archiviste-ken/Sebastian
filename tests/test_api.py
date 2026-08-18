from fastapi.testclient import TestClient

from app.api.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    
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
    
    
@app.get("/tasks/{task_id}")
def get_task(
    task_id: str,
    db: Session = Depends(get_db),
):
    repository = TaskRepository(db)
    task = repository.get(task_id)

    if task is None:
        return {"error": "Task not found"}

    return task