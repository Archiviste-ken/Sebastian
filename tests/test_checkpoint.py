# 🧪 Checkpoint model test
# Verifies a checkpoint can capture system state and preserve progress metadata.

from datetime import datetime, timezone

from app.models.checkpoint import Checkpoint


def test_checkpoint_creation():
    checkpoint = Checkpoint(
        id="checkpoint-1",
        task_id="task-1",
        action_id="action-2",
        state={
            "task_status": "executing",
            "completed_actions": ["action-1"],
        },
        created_at=datetime.now(timezone.utc),
    )

    assert checkpoint.task_id == "task-1"
    assert checkpoint.action_id == "action-2"
    assert checkpoint.state["task_status"] == "executing"