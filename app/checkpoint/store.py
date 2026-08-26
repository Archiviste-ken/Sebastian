"""In-memory checkpoint store for V1."""

from app.checkpoint.models import TaskState


class CheckpointStore:
    """Save and load task execution state.

    V1 implementation is in-memory.  The interface is designed so a
    database-backed store can be swapped in for V2 without changing callers.
    """

    def __init__(self) -> None:
        self._store: dict[str, TaskState] = {}

    def save(self, state: TaskState) -> None:
        state.touch()
        self._store[state.task_id] = state

    def load(self, task_id: str) -> TaskState | None:
        return self._store.get(task_id)

    def exists(self, task_id: str) -> bool:
        return task_id in self._store

    def delete(self, task_id: str) -> None:
        self._store.pop(task_id, None)
