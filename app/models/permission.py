from enum import Enum

from pydantic import BaseModel


class PermissionLevel(str, Enum):
    AUTONOMOUS = "autonomous"
    APPROVAL = "approval"
    BLOCKED = "blocked"


class Permission(BaseModel):
    id: str
    tool_name: str
    level: PermissionLevel