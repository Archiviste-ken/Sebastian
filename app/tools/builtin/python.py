# 🐍 Python script execution tool
# ⚙️ Runs arbitrary python scripts safely.

# 📦 Import subprocess to run the python interpreter.
import subprocess
# 📦 Import sys to discover the current python executable path.
import sys


# 🔌 Define a handler to execute a python script.
def run_python(script: str) -> dict:
    # 🚀 Execute the target script as a child python process.
    completed = subprocess.run(
        # ⌨️ Use the same python executable running this app to execute the script.
        [sys.executable, script],
        # 📥 Capture the script's output and error streams.
        capture_output=True,
        # 📝 Decode streams as text.
        text=True,
        # 🔒 Disable shell execution for safety.
        shell=False,
        # ⚠️ Do not raise exceptions on script failure.
        check=False,
    )

    # 🏗️ Return a structured dictionary with the script's results.
    return {
        # 🔢 The numeric exit status of the script.
        "return_code": completed.returncode,
        # 💬 The text printed to standard output by the script.
        "stdout": completed.stdout,
        # 💬 The text printed to standard error by the script.
        "stderr": completed.stderr,
    }