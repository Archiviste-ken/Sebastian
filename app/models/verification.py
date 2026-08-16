from typing import Any

from pydantic import BaseModel, Field


class Verification(BaseModel):
    id: str
    task_id: str
    success: bool
    method: str = Field(min_length=1)
    evidence: dict[str, Any] = {}