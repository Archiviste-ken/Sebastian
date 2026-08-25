# 📁 Safe-to-compose filesystem helpers
# Permission and workspace checks happen in ToolSafety before these functions run.

# 📦 Import Path for object-oriented filesystem manipulation.
from pathlib import Path


# 📖 Define a handler to read the entire contents of a text file.
def read_file(path: str) -> str:
    # 📖 Open a UTF-8 text file and return all of its text.
    return Path(path).read_text(encoding="utf-8")


# 🗂️ Define a handler to list the contents of a directory.
def list_directory(path: str) -> list[str]:
    # 🗂️ Return entry names in a predictable alphabetical order.
    return sorted(
        # 🏷️ Extract the name of each filesystem entry.
        entry.name
        # 🔄 Iterate over all entries in the given directory path.
        for entry in Path(path).iterdir()
    )


# 📝 Define a handler to write string content into a text file.
def write_file(path: str, content: str) -> None:
    # 📝 Open (or create) the file and write the complete text.
    Path(path).write_text(
        # 💬 The text content to write.
        content,
        # 🔡 Force UTF-8 encoding for consistency.
        encoding="utf-8",
    )


# 📁 Define a handler to create a new directory and any necessary parents.
def create_directory(path: str) -> None:
    # 📁 Execute the underlying directory creation command.
    Path(path).mkdir(
        # ➕ Create intermediate parent directories if they don't exist.
        parents=True,
        # 🟢 Do not fail if the directory already exists.
        exist_ok=True,
    )


# 🔀 Define a handler to rename or move a file.
def move_file(source: str, destination: str) -> None:
    # 🔀 Execute the rename operation on the source path.
    Path(source).rename(destination)