# 🧾 Audit event model
# One event explains which tool was attempted and how it finished.

# 📦 Import dataclass decorator from the dataclasses module
from dataclasses import dataclass


# 🔧 Apply the dataclass decorator with frozen=True to make instances immutable
@dataclass(frozen=True)
# 🧪 Define the AuditEvent class to record an event
class AuditEvent:
    # 🏷️ Name of the tool that was requested.
    # 📝 Store the tool name as a string
    tool_name: str
    # ✅/❌ Whether that attempt finished successfully.
    # 📝 Boolean indicating success or failure
    success: bool
    # 💬 Human-readable summary of the outcome.
    # 📝 Store the outcome message as a string
    message: str
