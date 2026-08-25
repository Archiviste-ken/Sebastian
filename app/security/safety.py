# 🛡️ Call safety checks
# These checks reject malformed calls and prevent filesystem tools from escaping
# the workspace chosen for this Sebastian session.

# 📦 Import dataclass to create structured, immutable data objects.
from dataclasses import dataclass
# 📁 Import Path for object-oriented filesystem path manipulation.
from pathlib import Path

# 📦 Import ToolCall model to represent incoming tool execution requests.
from app.models.tool_call import ToolCall


# 🔒 Only these executables are currently allowed by the command safety policy.
# 🗃️ Define a set of allowed command names and their executable counterparts.
ALLOWED_COMMANDS = {
    # 🐍 Allow standard python executable.
    "python",
    # 🐍 Allow Windows python executable.
    "python.exe",
    # 🧪 Allow standard pytest executable.
    "pytest",
    # 🧪 Allow Windows pytest executable.
    "pytest.exe",
    # 🐙 Allow standard git executable.
    "git",
    # 🐙 Allow Windows git executable.
    "git.exe",
}


# 🏗️ Define a frozen dataclass to represent the result of a safety check.
@dataclass(frozen=True)
# 🛡️ This class encapsulates whether a call is safe and the reasoning behind it.
class SafetyDecision:
    # ✅ True means the call can continue to execution.
    safe: bool

    # 💬 Short explanation that can be shown in a result or audit record.
    reason: str


# 🛡️ Define the ToolSafety class to perform safety validations on tool calls.
class ToolSafety:
    # 🛠️ Initialize the ToolSafety instance, optionally taking a workspace path.
    def __init__(self, workspace: Path | None = None):
        # 📍 Resolve once so every later path comparison uses the same
        # absolute folder.
        # 📁 Set the workspace to the provided path, or default to the current working directory.
        self.workspace = (
            # ⚖️ Check if a workspace path was explicitly provided.
            workspace if workspace is not None else Path.cwd()
        # 🔍 Resolve the final path to an absolute, normalized path.
        ).resolve()

    # 🛡️ Method to check if a given tool call is safe to execute.
    def check(self, tool_call: ToolCall) -> SafetyDecision:
        # 🏷️ A blank tool name cannot be looked up or run safely.
        # ⚖️ Check if the tool name is empty or only whitespace.
        if not tool_call.tool_name.strip():
            # 🚫 Return a negative safety decision for empty tool names.
            return SafetyDecision(
                # 🔴 Mark as unsafe.
                safe=False,
                # 📝 Provide a reason stating the tool name is empty.
                reason="Tool name cannot be empty.",
            )

        # 🔒 Single-path filesystem tools.
        # ⚖️ Check if the tool is one of the standard single-path filesystem tools.
        if tool_call.tool_name in {
            # 📁 Read file operation.
            "read_file",
            # 📁 List directory operation.
            "list_directory",
            # 📁 Write file operation.
            "write_file",
            # 📁 Create directory operation.
            "create_directory",
        }:
            # 🔍 Delegate to the specific filesystem path safety check.
            return self._check_filesystem_path(tool_call)

        # 🔀 move_file has TWO paths.
        # ⚖️ Check if the tool is a file move operation.
        if tool_call.tool_name == "move_file":
            # 🔍 Delegate to the specific move file safety check.
            return self._check_move_file(tool_call)

        # ⌨️ run_command has a command list.
        # ⚖️ Check if the tool is a shell command execution.
        if tool_call.tool_name == "run_command":
            # 🔍 Delegate to the specific run command safety check.
            return self._check_run_command(tool_call)

        # 🐍 run_python has a script path.
        # ⚖️ Check if the tool is a python script execution.
        if tool_call.tool_name == "run_python":
            # 🔍 Delegate to the specific python script safety check.
            return self._check_python_script(tool_call)

        # 🐙 Git inspection tools operate only on the approved workspace.
        # ⚖️ Check if the tool is a read-only git operation.
        if tool_call.tool_name in {
            # 🐙 Git status operation.
            "git_status",
            # 🐙 Git diff operation.
            "git_diff",
            # 🐙 Git log operation.
            "git_log",
        }:
            # 🔍 Delegate to the specific git workspace safety check.
            return self._check_git_workspace(tool_call)

        # ✅ Other tools currently need only the basic name check.
        # 🏗️ Return a positive safety decision for any unhandled tools.
        return SafetyDecision(
            # 🟢 Mark as safe.
            safe=True,
            # 📝 Provide a reason stating basic checks passed.
            reason="Tool call passed basic safety checks.",
        )

    # 🛡️ Internal method to validate single-path filesystem tool calls.
    def _check_filesystem_path(
        # 🧍 Reference to the current instance.
        self,
        # 📥 The tool call object to validate.
        tool_call: ToolCall,
    ) -> SafetyDecision:
        # 📥 Read the common `path` argument used by single-path tools.
        path_value = tool_call.arguments.get("path")

        # ⚖️ Ensure the path argument is a non-empty string.
        if not isinstance(path_value, str) or not path_value.strip():
            # 🚫 Return a negative safety decision for invalid path arguments.
            return SafetyDecision(
                # 🔴 Mark as unsafe.
                safe=False,
                # 📝 Provide a reason specifying the missing path requirement.
                reason=f"{tool_call.tool_name} requires a non-empty path.",
            )

        # 📁 Convert the string path value into a Path object for manipulation.
        candidate = Path(path_value)

        # ⚖️ Check if the candidate path is relative.
        if not candidate.is_absolute():
            # 📁 Anchor the relative path to the allowed workspace directory.
            candidate = self.workspace / candidate

        # 🛡️ Attempt to resolve the path and verify it stays within bounds.
        try:
            # 🔍 Resolve `..` and symlinks, then prove the path remains
            # inside the workspace.
            resolved = candidate.resolve()
            # 📏 Calculate the path relative to the workspace, which raises ValueError if outside.
            resolved.relative_to(self.workspace)

        # ⚠️ Catch the ValueError raised when the path escapes the workspace.
        except ValueError:
            # 🚫 Return a negative safety decision because the path escaped.
            return SafetyDecision(
                # 🔴 Mark as unsafe.
                safe=False,
                # 📝 Provide a reason stating the path is outside allowed bounds.
                reason="Path is outside the allowed workspace.",
            )

        # 🏗️ Return a positive safety decision since the path is valid and contained.
        return SafetyDecision(
            # 🟢 Mark as safe.
            safe=True,
            # 📝 Provide a reason stating the path is properly bounded.
            reason="Path is inside the allowed workspace.",
        )

    # 🛡️ Internal method to validate the two paths required for a move operation.
    def _check_move_file(
        # 🧍 Reference to the current instance.
        self,
        # 📥 The tool call object to validate.
        tool_call: ToolCall,
    ) -> SafetyDecision:
        # 📥 move_file has two paths instead of one.
        # 📥 Extract the source path argument.
        source = tool_call.arguments.get("source")
        # 📥 Extract the destination path argument.
        destination = tool_call.arguments.get("destination")

        # ⚖️ Ensure the source argument is a non-empty string.
        if not isinstance(source, str) or not source.strip():
            # 🚫 Return a negative safety decision for invalid source arguments.
            return SafetyDecision(
                # 🔴 Mark as unsafe.
                safe=False,
                # 📝 Provide a reason specifying the missing source requirement.
                reason="move_file requires a non-empty source.",
            )

        # ⚖️ Ensure the destination argument is a non-empty string.
        if not isinstance(destination, str) or not destination.strip():
            # 🚫 Return a negative safety decision for invalid destination arguments.
            return SafetyDecision(
                # 🔴 Mark as unsafe.
                safe=False,
                # 📝 Provide a reason specifying the missing destination requirement.
                reason="move_file requires a non-empty destination.",
            )

        # 🔒 Both paths must remain inside the workspace.
        # 🔄 Loop through both the source and destination paths to validate them.
        for path_value in (source, destination):
            # 📁 Convert the string path value into a Path object.
            candidate = Path(path_value)

            # ⚖️ Check if the candidate path is relative.
            if not candidate.is_absolute():
                # 📁 Anchor the relative path to the allowed workspace directory.
                candidate = self.workspace / candidate

            # 🛡️ Attempt to resolve the path and verify it stays within bounds.
            try:
                # 🔍 Resolve `..` and symlinks.
                resolved = candidate.resolve()
                # 📏 Ensure the resolved path is relative to the workspace.
                resolved.relative_to(self.workspace)

            # ⚠️ Catch the ValueError if the path escapes the workspace.
            except ValueError:
                # 🚫 Return a negative safety decision because a path escaped.
                return SafetyDecision(
                    # 🔴 Mark as unsafe.
                    safe=False,
                    # 📝 Provide a reason stating a path is outside allowed bounds.
                    reason="Path is outside the allowed workspace.",
                )

        # 🏗️ Return a positive safety decision since both paths are valid and contained.
        return SafetyDecision(
            # 🟢 Mark as safe.
            safe=True,
            # 📝 Provide a reason stating both paths are properly bounded.
            reason="Source and destination are inside the allowed workspace.",
        )

    # 🛡️ Internal method to validate run_command tool calls.
    def _check_run_command(
        # 🧍 Reference to the current instance.
        self,
        # 📥 The tool call object to validate.
        tool_call: ToolCall,
    ) -> SafetyDecision:
        # 📥 Get the command argument.
        command = tool_call.arguments.get("command")

        # ⚖️ Ensure the command argument is a non-empty list.
        if not isinstance(command, list) or not command:
            # 🚫 Return a negative safety decision for invalid command list.
            return SafetyDecision(
                # 🔴 Mark as unsafe.
                safe=False,
                # 📝 Provide a reason specifying the missing command list requirement.
                reason="run_command requires a non-empty command list.",
            )

        # ⚖️ Ensure all elements within the command list are non-empty strings.
        if not all(
            # 🔍 Check if the part is a string and is not just whitespace.
            isinstance(part, str) and part.strip()
            # 🔄 Iterate through each part of the command list.
            for part in command
        ):
            # 🚫 Return a negative safety decision for invalid command parts.
            return SafetyDecision(
                # 🔴 Mark as unsafe.
                safe=False,
                # 📝 Provide a reason stating command arguments must be non-empty strings.
                reason="run_command arguments must be non-empty strings.",
            )

        # 🔎 Extract the executable name.
        # 📁 Get the name of the executable (first item) and convert to lowercase for comparison.
        executable = Path(command[0]).name.lower()

        # ⚖️ Check if the extracted executable is in the predefined allowed list.
        if executable not in ALLOWED_COMMANDS:
            # 🚫 Return a negative safety decision for forbidden executables.
            return SafetyDecision(
                # 🔴 Mark as unsafe.
                safe=False,
                # 📝 Provide a reason specifying which command was blocked.
                reason=f"Command is not allowed: {executable}",
            )

        # 🏗️ Return a positive safety decision since the command is permitted.
        return SafetyDecision(
            # 🟢 Mark as safe.
            safe=True,
            # 📝 Provide a reason stating the command passed safety checks.
            reason="Command passed safety checks.",
        )

    # 🛡️ Internal method to validate python script execution calls.
    def _check_python_script(
        # 🧍 Reference to the current instance.
        self,
        # 📥 The tool call object to validate.
        tool_call: ToolCall,
    ) -> SafetyDecision:
        # 📥 Get the script path.
        script = tool_call.arguments.get("script")

        # ⚖️ Ensure the script argument is a non-empty string.
        if not isinstance(script, str) or not script.strip():
            # 🚫 Return a negative safety decision for invalid script argument.
            return SafetyDecision(
                # 🔴 Mark as unsafe.
                safe=False,
                # 📝 Provide a reason specifying the missing script path requirement.
                reason="run_python requires a non-empty script path.",
            )

        # 📁 Convert the string script path into a Path object.
        candidate = Path(script)

        # ⚖️ Check if the candidate script path is relative.
        if not candidate.is_absolute():
            # 📁 Anchor the relative path to the allowed workspace directory.
            candidate = self.workspace / candidate

        # 🛡️ Attempt to resolve the script path and verify it stays within bounds.
        try:
            # 🔍 Resolve the path and ensure it stays inside the workspace.
            resolved = candidate.resolve()
            # 📏 Ensure the resolved path is relative to the workspace.
            resolved.relative_to(self.workspace)

        # ⚠️ Catch the ValueError if the script path escapes the workspace.
        except ValueError:
            # 🚫 Return a negative safety decision because the script escaped.
            return SafetyDecision(
                # 🔴 Mark as unsafe.
                safe=False,
                # 📝 Provide a reason stating the script is outside allowed bounds.
                reason="Python script is outside the allowed workspace.",
            )

        # 🐍 Only Python scripts are accepted.
        # ⚖️ Check if the resolved file extension is strictly .py.
        if resolved.suffix.lower() != ".py":
            # 🚫 Return a negative safety decision for non-python extensions.
            return SafetyDecision(
                # 🔴 Mark as unsafe.
                safe=False,
                # 📝 Provide a reason specifying that only .py scripts are allowed.
                reason="run_python requires a .py script.",
            )

        # 🏗️ Return a positive safety decision since the python script is valid.
        return SafetyDecision(
            # 🟢 Mark as safe.
            safe=True,
            # 📝 Provide a reason stating the python script passed checks.
            reason="Python script passed safety checks.",
        )

    # 🛡️ Internal method to validate git operations.
    def _check_git_workspace(
        # 🧍 Reference to the current instance.
        self,
        # 📥 The tool call object to validate.
        tool_call: ToolCall,
    ) -> SafetyDecision:
        # 🐙 Git tools do not accept an arbitrary repository path.
        # They operate only against the trusted Sebastian workspace.
        # 🏗️ Return a positive safety decision automatically for supported git ops.
        return SafetyDecision(
            # 🟢 Mark as safe.
            safe=True,
            # 📝 Provide a reason stating git ops are restricted safely.
            reason="Git operation is restricted to the Sebastian workspace.",
        )