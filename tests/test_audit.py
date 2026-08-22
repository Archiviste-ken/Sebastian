from app.models.audit_event import AuditEvent
from app.tools.audit import AuditRecorder


def test_audit_recorder_stores_events():
    recorder = AuditRecorder()

    event = AuditEvent(
        tool_name="hello",
        success=True,
        message="Tool executed successfully.",
    )

    recorder.record(event)

    events = recorder.events()

    assert len(events) == 1
    assert events[0] is event