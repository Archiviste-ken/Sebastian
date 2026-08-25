# ✅ Verification model
# 🎯 Verification is the evidence-based conclusion step.
# 🛡️ Sebastian does not assume work succeeded; it records how success was checked.

# 📦 Import Any from typing to support arbitrary types in evidence.
from typing import Any

# 📦 Import BaseModel and Field from pydantic for model definition and constraints.
from pydantic import BaseModel, Field


# 🏷️ Define the Verification class, inheriting from BaseModel.
class Verification(BaseModel):
    # 🆔 Unique verification record identifier.
    # 📝 String ID for the verification instance.
    id: str

    # 🧵 Task being verified.
    # 🏷️ Links the verification to a specific task ID.
    task_id: str

    # ✅ Whether verification succeeded.
    # 📝 Boolean indicating true if verification passed, false otherwise.
    success: bool

    # 🔎 Method used for verification, such as tests or a diff check.
    # 🔧 Uses Field to ensure the method string is at least 1 character long.
    method: str = Field(min_length=1)

    # 📚 Evidence collected to support the result.
    # 📝 A dictionary to store evidence data, defaulting to an empty dict.
    evidence: dict[str, Any] = {}