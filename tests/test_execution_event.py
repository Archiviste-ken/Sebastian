# 🧪 Execution event test
# Confirms event metadata is captured correctly when a tool completes successfully.

from datetime import datetime, timezone

from app.models.execution_event import ExecutionEvent


def test_execution_event_creation():
    timestamp = datetime.now(timezone.utc)

    event = ExecutionEvent(
        id="event-1",
        tool_call_id="call-1",
        event_type="tool_completed",
        success=True,
        timestamp=timestamp,
        data={
            "exit_code": 0,
        },
    )

    assert event.tool_call_id == "call-1"
    assert event.success is True
    assert event.data["exit_code"] == 0