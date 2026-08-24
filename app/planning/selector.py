from app.intent.models import Intent
from app.planning.capabilities import CAPABILITIES, Capability


class CapabilitySelector:
    def select(
        self,
        intent: Intent,
    ) -> list[Capability]:
        goal = intent.goal.lower()
        outcome = intent.expected_outcome.lower()
        constraints = " ".join(intent.constraints).lower()
        criteria = " ".join(intent.success_criteria).lower()

        selected: list[Capability] = []

        # 📖 Explicit file-reading intent.
        if self._is_file_read_request(
            goal=goal,
            outcome=outcome,
        ):
            selected.append(self._get("read_file"))

        # 📂 Explicit directory inspection.
        if self._is_directory_listing_request(
            goal=goal,
            outcome=outcome,
        ):
            selected.append(self._get("list_directory"))

        # 🧪 Test execution.
        if self._is_test_execution_request(
            goal=goal,
            outcome=outcome,
            criteria=criteria,
        ):
            selected.append(self._get("run_command"))

        # 🐍 Direct Python-script execution.
        # Do NOT infer this merely because the user mentioned Python.
        if self._is_python_execution_request(
            goal=goal,
            outcome=outcome,
        ):
            selected.append(self._get("run_python"))

        # 🔀 File movement / archiving.
        if self._is_move_request(
            goal=goal,
            outcome=outcome,
            constraints=constraints,
        ):
            selected.append(self._get("move_file"))

        # 🐙 Git inspection.
        if "git status" in goal or "working tree" in goal:
            selected.append(self._get("git_status"))

        if "git diff" in goal or "show the diff" in goal:
            selected.append(self._get("git_diff"))

        if (
            "git log" in goal
            or "recent commits" in goal
            or "commit history" in goal
        ):
            selected.append(self._get("git_log"))

        return self._deduplicate(selected)

    @staticmethod
    def _is_file_read_request(
        goal: str,
        outcome: str,
    ) -> bool:
        text = " ".join(
            [
                goal,
                outcome,
            ]
        )

        explicit_terms = (
            "read file",
            "read the file",
            "read ",
            "open file",
            "open the file",
            "file contents",
            "contents of the file",
        )

        return any(
            term in text
            for term in explicit_terms
        )

    @staticmethod
    def _is_directory_listing_request(
        goal: str,
        outcome: str,
    ) -> bool:
        explicit_terms = (
            "list directory",
            "list the directory",
            "list folder",
            "list the folder",
            "directory contents",
            "folder contents",
            "inspect this folder",
            "inspect the folder",
            "inspect this directory",
            "inspect the directory",
        )

        return any(
            term in goal or term in outcome
            for term in explicit_terms
        )

    @staticmethod
    def _is_test_execution_request(
        goal: str,
        outcome: str,
        criteria: str,
    ) -> bool:
        text = " ".join(
            [
                goal,
                outcome,
                criteria,
            ]
        )

        test_terms = (
            "run the tests",
            "run tests",
            "run the test suite",
            "run test suite",
            "pytest",
            "execute the tests",
            "execute tests",
        )

        return any(
            term in text
            for term in test_terms
        )

    @staticmethod
    def _is_python_execution_request(
        goal: str,
        outcome: str,
    ) -> bool:
        text = " ".join(
            [
                goal,
                outcome,
            ]
        )

        python_execution_terms = (
            "run this python script",
            "run the python script",
            "execute this python script",
            "execute the python script",
            "run a python script",
            "execute a python script",
        )

        return any(
            term in text
            for term in python_execution_terms
        )

    @staticmethod
    def _is_move_request(
        goal: str,
        outcome: str,
        constraints: str,
    ) -> bool:
        text = " ".join(
            [
                goal,
                outcome,
                constraints,
            ]
        )

        move_terms = (
            "move file",
            "move the file",
            "move files",
            "move the files",
            "archive file",
            "archive the file",
            "archive files",
            "archive the files",
        )

        return any(
            term in text
            for term in move_terms
        )

    @staticmethod
    def _get(name: str) -> Capability:
        for capability in CAPABILITIES:
            if capability.name == name:
                return capability

        raise ValueError(
            f"Unknown capability: {name}"
        )

    @staticmethod
    def _deduplicate(
        capabilities: list[Capability],
    ) -> list[Capability]:
        seen: set[str] = set()
        result: list[Capability] = []

        for capability in capabilities:
            if capability.name in seen:
                continue

            seen.add(capability.name)
            result.append(capability)

        return result