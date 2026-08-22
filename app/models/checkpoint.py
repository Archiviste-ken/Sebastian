# 🧭 Checkpoint model
# A checkpoint is a snapshot of the system state at a specific moment.
# Sebastian can save progress, inspect what happened, and recover if a later step fails.

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel


class Checkpoint(BaseModel):
    # 🆔 Unique checkpoint identifier.
    id: str

    # 🧵 Task this checkpoint belongs to.
    task_id: str

    # ⚙️ Optional action that was active when the checkpoint was created.
    action_id: str | None = None

    # 🗂️ Saved execution state, such as progress, flags, or partial results.
    state: dict[str, Any]

    # 🕒 Timestamp of the snapshot.
    created_at: datetime