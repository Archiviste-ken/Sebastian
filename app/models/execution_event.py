# 🧪 Execution event model
# 📖 This records what happened during a tool execution.
# 🔄 It turns raw tool behavior into traceable evidence for verification and debugging.
# 💨 Empty line for spacing
from datetime import datetime, timezone # 📦 Import datetime and timezone for timestamps
from typing import Any # 📦 Import Any for typing metadata
# 💨 Empty line for spacing
from pydantic import BaseModel, Field # 📦 Import BaseModel and Field for validation
# 💨 Empty line for spacing
# 💨 Empty line for spacing
class ExecutionEvent(BaseModel): # 🏷️ Define ExecutionEvent class inheriting from BaseModel
    # 🆔 Unique execution event identifier.
    id: str # 📝 ID string
# 💨 Empty line for spacing
    # 🔗 Tool call this event is associated with.
    tool_call_id: str # 📝 Tool call ID string
# 💨 Empty line for spacing
    # 🏷️ Event category, such as "tool_started" or "tool_completed".
    event_type: str = Field(min_length=1) # 📝 Event type string with min length 1
# 💨 Empty line for spacing
    # ✅ Whether the event indicates success or failure.
    success: bool # 📝 Success boolean flag
# 💨 Empty line for spacing
    # 🕒 When the event occurred.
    timestamp: datetime # 📝 Timestamp of the event
# 💨 Empty line for spacing
    # 📦 Additional execution metadata such as exit codes or outputs.
    data: dict[str, Any] = {} # 📝 Data dict with string keys and Any values