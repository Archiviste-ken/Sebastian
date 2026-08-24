from dataclasses import dataclass


@dataclass(frozen=True)
class Capability:
    name: str
    description: str
    risk: str


CAPABILITIES = (
    Capability(
        name="read_file",
        description="Read the contents of a text file.",
        risk="low",
    ),
    Capability(
        name="list_directory",
        description="List the contents of a directory.",
        risk="low",
    ),
    Capability(
        name="write_file",
        description="Write text content to a file.",
        risk="medium",
    ),
    Capability(
        name="create_directory",
        description="Create a directory.",
        risk="medium",
    ),
    Capability(
        name="move_file",
        description="Move a file from one path to another.",
        risk="medium",
    ),
    Capability(
        name="run_command",
        description="Run an approved command.",
        risk="high",
    ),
    Capability(
        name="run_python",
        description="Run a Python script inside the workspace.",
        risk="high",
    ),
    Capability(
        name="git_status",
        description="Inspect the current Git working tree.",
        risk="low",
    ),
    Capability(
        name="git_diff",
        description="Inspect the current Git diff.",
        risk="low",
    ),
    Capability(
        name="git_log",
        description="Inspect recent Git commits.",
        risk="low",
    ),
)