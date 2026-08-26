"""Evidence-based verification: checks concrete state, never trusts claims."""

from pathlib import Path

from app.models.tool_result import ToolResult
from app.planning.models import Action
from app.verification.models import VerificationResult, VerificationStatus


class VerificationEngine:
    """Deterministic verification using actual evidence (files, exit codes, output)."""

    def verify(
        self,
        action: Action,
        tool_result: ToolResult,
        workspace: Path,
    ) -> VerificationResult:
        # A tool that reports failure is a definitive FAIL.
        if not tool_result.success:
            return VerificationResult(
                status=VerificationStatus.FAIL,
                method="tool_result_status",
                reason=tool_result.error or "Tool execution failed.",
                evidence={"status": tool_result.status.value, "error": tool_result.error},
            )

        tool_name = action.tool
        dispatch = {
            "run_command": self._verify_command,
            "run_python": self._verify_command,
            "write_file": self._verify_write_file,
            "create_directory": self._verify_create_directory,
            "read_file": self._verify_read_file,
            "list_directory": self._verify_list_directory,
            "move_file": self._verify_move_file,
            "git_status": self._verify_command,
            "git_diff": self._verify_command,
            "git_log": self._verify_command,
        }

        handler = dispatch.get(tool_name)
        if handler is None:
            return VerificationResult(
                status=VerificationStatus.UNCERTAIN,
                method="default_success_check",
                reason="Tool reported success but no specific verification is available.",
                evidence={"tool_success": True},
            )

        if tool_name in ("write_file", "create_directory", "move_file"):
            return handler(action, workspace)
        return handler(tool_result)

    # ── command / script ──────────────────────────────────────────────
    @staticmethod
    def _verify_command(tool_result: ToolResult) -> VerificationResult:
        data = tool_result.data
        if isinstance(data, dict):
            rc = data.get("return_code")
            if rc == 0:
                return VerificationResult(
                    status=VerificationStatus.PASS,
                    method="exit_code_check",
                    reason="Command exited with code 0.",
                    evidence={"return_code": 0, "stdout": str(data.get("stdout", ""))[:500]},
                )
            return VerificationResult(
                status=VerificationStatus.FAIL,
                method="exit_code_check",
                reason=f"Command exited with code {rc}.",
                evidence={"return_code": rc, "stderr": str(data.get("stderr", ""))[:500]},
            )
        return VerificationResult(
            status=VerificationStatus.UNCERTAIN,
            method="exit_code_check",
            reason="Command result format unexpected.",
            evidence={"data_type": type(data).__name__},
        )

    # ── filesystem ────────────────────────────────────────────────────
    @staticmethod
    def _verify_write_file(action: Action, workspace: Path) -> VerificationResult:
        path_arg = action.arguments.get("path", "")
        if not path_arg:
            return VerificationResult(
                status=VerificationStatus.UNCERTAIN,
                method="file_existence_check",
                reason="No path argument to verify.",
            )
        target = Path(path_arg)
        if not target.is_absolute():
            target = workspace / target
        if target.exists():
            return VerificationResult(
                status=VerificationStatus.PASS,
                method="file_existence_check",
                reason="Written file exists on disk.",
                evidence={"path": str(target), "exists": True},
            )
        return VerificationResult(
            status=VerificationStatus.FAIL,
            method="file_existence_check",
            reason="Written file not found on disk.",
            evidence={"path": str(target), "exists": False},
        )

    @staticmethod
    def _verify_create_directory(action: Action, workspace: Path) -> VerificationResult:
        path_arg = action.arguments.get("path", "")
        if not path_arg:
            return VerificationResult(
                status=VerificationStatus.UNCERTAIN,
                method="directory_existence_check",
                reason="No path argument to verify.",
            )
        target = Path(path_arg)
        if not target.is_absolute():
            target = workspace / target
        if target.is_dir():
            return VerificationResult(
                status=VerificationStatus.PASS,
                method="directory_existence_check",
                reason="Created directory exists.",
                evidence={"path": str(target), "is_dir": True},
            )
        return VerificationResult(
            status=VerificationStatus.FAIL,
            method="directory_existence_check",
            reason="Created directory not found.",
            evidence={"path": str(target), "is_dir": False},
        )

    @staticmethod
    def _verify_read_file(tool_result: ToolResult) -> VerificationResult:
        if isinstance(tool_result.data, str) and tool_result.data:
            return VerificationResult(
                status=VerificationStatus.PASS,
                method="content_check",
                reason="File content returned successfully.",
                evidence={"content_length": len(tool_result.data)},
            )
        return VerificationResult(
            status=VerificationStatus.UNCERTAIN,
            method="content_check",
            reason="File read returned empty or unexpected data.",
            evidence={"data_type": type(tool_result.data).__name__},
        )

    @staticmethod
    def _verify_list_directory(tool_result: ToolResult) -> VerificationResult:
        if isinstance(tool_result.data, list):
            return VerificationResult(
                status=VerificationStatus.PASS,
                method="listing_check",
                reason="Directory listing returned.",
                evidence={"entry_count": len(tool_result.data)},
            )
        return VerificationResult(
            status=VerificationStatus.UNCERTAIN,
            method="listing_check",
            reason="Directory listing format unexpected.",
            evidence={"data_type": type(tool_result.data).__name__},
        )

    @staticmethod
    def _verify_move_file(action: Action, workspace: Path) -> VerificationResult:
        dest = action.arguments.get("destination", "")
        if not dest:
            return VerificationResult(
                status=VerificationStatus.UNCERTAIN,
                method="move_check",
                reason="No destination argument to verify.",
            )
        target = Path(dest)
        if not target.is_absolute():
            target = workspace / target
        if target.exists():
            return VerificationResult(
                status=VerificationStatus.PASS,
                method="move_check",
                reason="Destination file exists after move.",
                evidence={"destination": str(target), "exists": True},
            )
        return VerificationResult(
            status=VerificationStatus.FAIL,
            method="move_check",
            reason="Destination file not found after move.",
            evidence={"destination": str(target), "exists": False},
        )
