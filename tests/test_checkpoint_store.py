import pytest

from app.checkpoint.models import TaskState
from app.checkpoint.store import CheckpointStore


@pytest.fixture
def store():
    return CheckpointStore()


def test_save_and_load(store):
    state = TaskState(task_id="t-1", status="executing")
    store.save(state)
    loaded = store.load("t-1")
    assert loaded is not None
    assert loaded.task_id == "t-1"
    assert loaded.status == "executing"


def test_load_missing_returns_none(store):
    assert store.load("nonexistent") is None


def test_exists(store):
    assert not store.exists("t-1")
    store.save(TaskState(task_id="t-1", status="pending"))
    assert store.exists("t-1")


def test_delete(store):
    store.save(TaskState(task_id="t-1", status="pending"))
    store.delete("t-1")
    assert not store.exists("t-1")


def test_delete_nonexistent_no_error(store):
    store.delete("ghost")


def test_save_updates_timestamp(store):
    state = TaskState(task_id="t-1", status="pending")
    first_ts = state.updated_at
    store.save(state)
    assert state.updated_at >= first_ts


def test_completed_actions_tracked(store):
    state = TaskState(task_id="t-1", status="executing")
    state.completed_actions.append("action-1")
    state.results["action-1"] = {"status": "success"}
    store.save(state)
    loaded = store.load("t-1")
    assert "action-1" in loaded.completed_actions
    assert loaded.results["action-1"]["status"] == "success"


def test_task_state_timestamps_auto_set():
    state = TaskState(task_id="t-1", status="pending")
    assert state.created_at
    assert state.updated_at
