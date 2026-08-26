"""Recovery outcome types."""

from dataclasses import dataclass
from enum import Enum


class RecoveryStrategy(str, Enum):
    RETRY = "retry"
    SKIP = "skip"
    FAIL = "fail"


@dataclass(frozen=True)
class RecoveryDecision:
    strategy: RecoveryStrategy
    reason: str
