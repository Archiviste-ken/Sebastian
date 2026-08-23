from pathlib import Path

from app.tools.builtin.filesystem import (
    create_directory,
    list_directory,
    read_file,
    write_file,
)

def test_read_file(tmp_path: Path):
    file_path = tmp_path / "hello.txt"

    file_path.write_text(
        "Hello from Sebastian!",
        encoding="utf-8",
    )

    result = read_file(str(file_path))

    assert result == "Hello from Sebastian!"


def test_list_directory(tmp_path: Path):
    (tmp_path / "b.txt").write_text(
        "B",
        encoding="utf-8",
    )

    (tmp_path / "a.txt").write_text(
        "A",
        encoding="utf-8",
    )

    (tmp_path / "folder").mkdir()

    result = list_directory(str(tmp_path))

    assert result == [
        "a.txt",
        "b.txt",
        "folder",
    ]


def test_write_file(tmp_path: Path):
    file_path = tmp_path / "hello.txt"

    result = write_file(
        str(file_path),
        "Hello from Sebastian!",
    )

    assert result is None
    assert file_path.read_text(encoding="utf-8") == (
        "Hello from Sebastian!"
    )
    
def test_create_directory(tmp_path: Path):
    directory_path = tmp_path / "data" / "reports"

    result = create_directory(str(directory_path))

    assert result is None
    assert directory_path.is_dir()