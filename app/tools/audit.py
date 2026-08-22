from app.models.audit_event import AuditEvent


class AuditRecorder:
    def __init__(self):
        self._events: list[AuditEvent] = []

    def record(self, event: AuditEvent) -> None:
        self._events.append(event)

    def events(self) -> list[AuditEvent]:
        return list(self._events)