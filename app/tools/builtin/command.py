# ⌨️ Command execution tool
# ⚙️ Runs arbitrary terminal commands safely.

# 📦 Import subprocess to spawn new processes and connect to their pipes.
import subprocess


# 🔌 Define the handler to run a command and capture its output.
def run_command(command: list[str]) -> dict:
    # 🚀 Execute the command synchronously and capture all output.
    completed = subprocess.run(
        # ⌨️ Pass the command list directly.
        command,
        # 📥 Capture stdout and stderr for later inspection.
        capture_output=True,
        # 📝 Decode the output as text rather than raw bytes.
        text=True,
        # 🔒 Explicitly disable shell to prevent injection attacks.
        shell=False,
        # ⚠️ Do not raise an exception on non-zero exit codes.
        check=False,
    )

    # 🏗️ Return a structured dictionary with the command's results.
    return {
        # 🔢 Include the numeric exit code.
        "return_code": completed.returncode,
        # 💬 Include the standard output stream content.
        "stdout": completed.stdout,
        # 💬 Include the standard error stream content.
        "stderr": completed.stderr,
    }