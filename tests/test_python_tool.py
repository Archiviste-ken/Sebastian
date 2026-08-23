from pathlib import Path

from app.tools.builtin.python import run_python


def test_run_python(tmp_path: Path):
    script = tmp_path / "hello.py"

    script.write_text(
        "print('Hello from Sebastian Python!')",
        encoding="utf-8",
    )

    result = run_python(str(script))

    assert result["return_code"] == 0
    assert result["stdout"].strip() == (
        "Hello from Sebastian Python!"
    )
    assert result["stderr"] == ""