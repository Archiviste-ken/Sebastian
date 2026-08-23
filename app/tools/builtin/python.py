import subprocess
import sys


def run_python(script: str) -> dict:
    completed = subprocess.run(
        [sys.executable, script],
        capture_output=True,
        text=True,
        shell=False,
        check=False,
    )

    return {
        "return_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }