# 📦 Import dataclass decorator from dataclasses module
from dataclasses import dataclass
# 🈳 Blank line
# 🈳 Blank line

# 🧩 Apply dataclass decorator and make instances frozen (immutable)
@dataclass(frozen=True)
# 🧩 Define the Capability class to represent a tool or action capability
class Capability:
    # 🧩 Define the name of the capability as a string
    name: str
    # 🧩 Define the description of the capability as a string
    description: str
    # 🧩 Define the risk level of the capability as a string
    risk: str
# 🈳 Blank line
# 🈳 Blank line

# 🧩 Define a tuple of standard capabilities available to the system
CAPABILITIES = (
    # 🧩 Define the read_file capability
    Capability(
        # 🧩 Set capability name to read_file
        name="read_file",
        # 🧩 Describe the read_file capability
        description="Read the contents of a text file.",
        # 🧩 Set risk level to low
        risk="low",
    # 🧩 Close read_file capability definition
    ),
    # 🧩 Define the list_directory capability
    Capability(
        # 🧩 Set capability name to list_directory
        name="list_directory",
        # 🧩 Describe the list_directory capability
        description="List the contents of a directory.",
        # 🧩 Set risk level to low
        risk="low",
    # 🧩 Close list_directory capability definition
    ),
    # 🧩 Define the write_file capability
    Capability(
        # 🧩 Set capability name to write_file
        name="write_file",
        # 🧩 Describe the write_file capability
        description="Write text content to a file.",
        # 🧩 Set risk level to medium
        risk="medium",
    # 🧩 Close write_file capability definition
    ),
    # 🧩 Define the create_directory capability
    Capability(
        # 🧩 Set capability name to create_directory
        name="create_directory",
        # 🧩 Describe the create_directory capability
        description="Create a directory.",
        # 🧩 Set risk level to medium
        risk="medium",
    # 🧩 Close create_directory capability definition
    ),
    # 🧩 Define the move_file capability
    Capability(
        # 🧩 Set capability name to move_file
        name="move_file",
        # 🧩 Describe the move_file capability
        description="Move a file from one path to another.",
        # 🧩 Set risk level to medium
        risk="medium",
    # 🧩 Close move_file capability definition
    ),
    # 🧩 Define the run_command capability
    Capability(
        # 🧩 Set capability name to run_command
        name="run_command",
        # 🧩 Describe the run_command capability
        description="Run an approved command.",
        # 🧩 Set risk level to high
        risk="high",
    # 🧩 Close run_command capability definition
    ),
    # 🧩 Define the run_python capability
    Capability(
        # 🧩 Set capability name to run_python
        name="run_python",
        # 🧩 Describe the run_python capability
        description="Run a Python script inside the workspace.",
        # 🧩 Set risk level to high
        risk="high",
    # 🧩 Close run_python capability definition
    ),
    # 🧩 Define the git_status capability
    Capability(
        # 🧩 Set capability name to git_status
        name="git_status",
        # 🧩 Describe the git_status capability
        description="Inspect the current Git working tree.",
        # 🧩 Set risk level to low
        risk="low",
    # 🧩 Close git_status capability definition
    ),
    # 🧩 Define the git_diff capability
    Capability(
        # 🧩 Set capability name to git_diff
        name="git_diff",
        # 🧩 Describe the git_diff capability
        description="Inspect the current Git diff.",
        # 🧩 Set risk level to low
        risk="low",
    # 🧩 Close git_diff capability definition
    ),
    # 🧩 Define the git_log capability
    Capability(
        # 🧩 Set capability name to git_log
        name="git_log",
        # 🧩 Describe the git_log capability
        description="Inspect recent Git commits.",
        # 🧩 Set risk level to low
        risk="low",
    # 🧩 Close git_log capability definition
    ),
# 🧩 Close the CAPABILITIES tuple
)