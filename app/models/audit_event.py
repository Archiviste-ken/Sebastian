# 🧾 Audit event model
# One event explains which tool was attempted and how it finished.

from dataclasses import dataclass


@dataclass(frozen=True)
class AuditEvent:
    # 🏷️ Name of the tool that was requested.
    tool_name: str
    # ✅/❌ Whether that attempt finished successfully.
    success: bool
    # 💬 Human-readable summary of the outcome.
    message: str
