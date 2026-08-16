from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel


class Checkpoint(BaseModel):
    id: str
    task_id: str
    action_id: str | None = None
    state: dict[str, Any]
    created_at: datetime