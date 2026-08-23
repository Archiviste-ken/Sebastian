# # 📁 Safe-to-compose filesystem helpers
# # Permission and workspace checks happen in ToolSafety before these functions run.

# from pathlib import Path


# def read_file(path: str) -> str:
#     # 📖 Open a UTF-8 text file and return all of its text.
#     return Path(path).read_text(encoding="utf-8")


# def list_directory(path: str) -> list[str]:
#     # 🗂️ Return entry names in a predictable alphabetical order.
#     return sorted(
#         entry.name
#         for entry in Path(path).iterdir()
#     )


from pathlib import Path


def read_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def list_directory(path: str) -> list[str]:
    return sorted(
        entry.name
        for entry in Path(path).iterdir()
    )


def write_file(path: str, content: str) -> None:
    Path(path).write_text(
        content,
        encoding="utf-8",
    )