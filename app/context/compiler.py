"""Deterministic context compilation: gathers relevant, bounded information."""

import os
from pathlib import Path
from typing import Any

from app.context.models import TaskContext
from app.intent.models import Intent
from app.security.permissions import PermissionKernel
from app.tools.registry import ToolRegistry

# Hard bounds to prevent dumping the entire workspace into context.
MAX_WORKSPACE_ENTRIES = 100
MAX_WALK_DEPTH = 2


class ContextCompiler:
    def __init__(
        self,
        registry: ToolRegistry,
        permission_kernel: PermissionKernel,
        workspace: Path,
    ):
        self._registry = registry
        self._permission_kernel = permission_kernel
        self._workspace = workspace.resolve()

    def compile(
        self,
        user_request: str,
        intent: Intent,
        prior_results: list[dict[str, Any]] | None = None,
        execution_history: list[dict[str, Any]] | None = None,
    ) -> TaskContext:
        workspace_files = self._list_workspace_files()
        tools = self._registry.list_tools()
        tool_names = [t.name for t in tools]
        tool_permissions = {
            name: self._permission_kernel.get_level(name).value
            for name in tool_names
        }

        return TaskContext(
            user_request=user_request,
            intent_goal=intent.goal,
            intent_constraints=list(intent.constraints),
            intent_forbidden_actions=list(intent.forbidden_actions),
            intent_expected_outcome=intent.expected_outcome,
            intent_success_criteria=list(intent.success_criteria),
            intent_required_permissions=list(intent.required_permissions),
            workspace_path=str(self._workspace),
            workspace_files=workspace_files,
            available_tools=tool_names,
            tool_permissions=tool_permissions,
            prior_results=prior_results or [],
            execution_history=execution_history or [],
        )

    # ------------------------------------------------------------------
    def _list_workspace_files(self) -> list[str]:
        """Bounded directory walk: max depth, max entries, skip hidden."""
        entries: list[str] = []
        try:
            for root, dirs, filenames in os.walk(self._workspace):
                rel_root = Path(root).relative_to(self._workspace)
                depth = len(rel_root.parts)
                if depth >= MAX_WALK_DEPTH:
                    dirs.clear()
                    continue
                # Skip hidden directories and common noise.
                dirs[:] = [
                    d for d in sorted(dirs)
                    if not d.startswith(".") and d not in {"__pycache__", "node_modules", ".venv", "venv"}
                ]
                for name in sorted(filenames):
                    if name.startswith("."):
                        continue
                    rel = str(rel_root / name) if str(rel_root) != "." else name
                    entries.append(rel)
                    if len(entries) >= MAX_WORKSPACE_ENTRIES:
                        return entries
        except OSError:
            pass
        return entries
