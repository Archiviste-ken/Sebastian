# 🧾 In-memory audit log
# This keeps a simple history of tool attempts for later inspection or testing.

from app.models.audit_event import AuditEvent


class AuditRecorder:
    def __init__(self):
        # 📚 Start with an empty ordered list of events.
        self._events: list[AuditEvent] = []

    def record(self, event: AuditEvent) -> None:
        # ➕ Add one completed tool attempt to the history.
        self._events.append(event)

    def events(self) -> list[AuditEvent]:
        # 🛡️ Return a copy so callers cannot change the stored history by accident.
        return list(self._events)
