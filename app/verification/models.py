"""Verification outcome types: PASS / FAIL / UNCERTAIN."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class VerificationStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    UNCERTAIN = "uncertain"


@dataclass(frozen=True)
class VerificationResult:
    status: VerificationStatus
    method: str
    reason: str
    evidence: dict[str, Any] = field(default_factory=dict)
