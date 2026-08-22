from pathlib import Path


def read_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def list_directory(path: str) -> list[str]:
    return sorted(
        entry.name
        for entry in Path(path).iterdir()
    )