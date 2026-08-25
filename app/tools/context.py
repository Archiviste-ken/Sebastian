# 📦 Import dataclass to create structured, immutable data objects.
from dataclasses import dataclass
# 📁 Import Path for object-oriented filesystem path manipulation.
from pathlib import Path


# 🏗️ Define a frozen dataclass to represent the context of an execution.
@dataclass(frozen=True)
# ⚙️ This class holds the environment settings needed when a tool runs.
class ExecutionContext:
    # 📁 The absolute path to the active workspace directory.
    workspace: Path