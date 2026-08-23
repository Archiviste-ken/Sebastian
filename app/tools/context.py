from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ExecutionContext:
    workspace: Path