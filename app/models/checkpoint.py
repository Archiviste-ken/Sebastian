# 🧭 Checkpoint model
# A checkpoint is a snapshot of the system state at a specific moment.
# Sebastian can save progress, inspect what happened, and recover if a later step fails.

# 📦 Import datetime and timezone from the datetime module
from datetime import datetime, timezone
# 📦 Import Any from the typing module for type hinting
from typing import Any

# 📦 Import BaseModel from pydantic for data validation and schema generation
from pydantic import BaseModel


# 📍 Define the Checkpoint class, inheriting from BaseModel
class Checkpoint(BaseModel):
    # 🆔 Unique checkpoint identifier.
    # 📝 Represents the id of the checkpoint
    id: str

    # 🧵 Task this checkpoint belongs to.
    # 🏷️ Identifier for the associated task
    task_id: str

    # ⚙️ Optional action that was active when the checkpoint was created.
    # 📝 Identifier for the associated action, which can be None
    action_id: str | None = None

    # 🗂️ Saved execution state, such as progress, flags, or partial results.
    # 🔄 Dictionary holding the state variables
    state: dict[str, Any]

    # 🕒 Timestamp of the snapshot.
    # 📝 The creation timestamp of this checkpoint
    created_at: datetime