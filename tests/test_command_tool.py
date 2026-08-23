from app.tools.builtin.command import run_command


def test_run_command():
    result = run_command(
        ["python", "-c", "print('Hello from Sebastian!')"]
    )

    assert result["return_code"] == 0
    assert result["stdout"].strip() == "Hello from Sebastian!"
    assert result["stderr"] == ""