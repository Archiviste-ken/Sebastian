# 🧾 In-memory audit log
# This keeps a simple history of tool attempts for later inspection or testing.

# 📦 Import the AuditEvent model to represent a single recorded action.
from app.models.audit_event import AuditEvent


# 📝 Define the AuditRecorder class to track a sequence of events.
class AuditRecorder:
    # 🛠️ Initialize a new recorder instance.
    def __init__(self):
        # 📚 Start with an empty ordered list of events.
        self._events: list[AuditEvent] = []

    # ➕ Method to store a new event in the log.
    def record(self, event: AuditEvent) -> None:
        # ➕ Add one completed tool attempt to the history.
        self._events.append(event)

    # 📋 Method to retrieve all stored events.
    def events(self) -> list[AuditEvent]:
        # 🛡️ Return a copy so callers cannot change the stored history by accident.
        return list(self._events)
