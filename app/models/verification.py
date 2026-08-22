# ✅ Verification model
# Verification is the evidence-based conclusion step.
# Sebastian does not assume work succeeded; it records how success was checked.

from typing import Any

from pydantic import BaseModel, Field


class Verification(BaseModel):
    # 🆔 Unique verification record identifier.
    id: str

    # 🧵 Task being verified.
    task_id: str

    # ✅ Whether verification succeeded.
    success: bool

    # 🔎 Method used for verification, such as tests or a diff check.
    method: str = Field(min_length=1)

    # 📚 Evidence collected to support the result.
    evidence: dict[str, Any] = {}