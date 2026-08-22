from dataclasses import dataclass


@dataclass(frozen=True)
class AuditEvent:
    tool_name: str
    success: bool
    message: str