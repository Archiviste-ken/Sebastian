# 📦 Import Intent model from app.intent.models
from app.intent.models import Intent
# 📦 Import CAPABILITIES tuple and Capability class from app.planning.capabilities
from app.planning.capabilities import CAPABILITIES, Capability
# 🈳 Blank line
# 🈳 Blank line

# 🔍 Define CapabilitySelector class for selecting appropriate tools
class CapabilitySelector:
    # 🔍 Define select method taking an Intent and returning capabilities
    def select(
        # ⚙️ Pass self reference
        self,
        # 🎯 Pass Intent object
        intent: Intent,
    # ⚙️ Return a list of Capability objects
    ) -> list[Capability]:
        # 🔍 Lowercase the goal for case-insensitive matching
        goal = intent.goal.lower()
        # 🔍 Lowercase the expected_outcome for case-insensitive matching
        outcome = intent.expected_outcome.lower()
        # 🔍 Join and lowercase constraints for matching
        constraints = " ".join(intent.constraints).lower()
        # 🔍 Join and lowercase success criteria for matching
        criteria = " ".join(intent.success_criteria).lower()
# 🈳 Blank line

        # 🔍 Initialize empty list for selected capabilities
        selected: list[Capability] = []
# 🈳 Blank line

        # 📖 Explicit file-reading intent.
        if self._is_file_read_request(
            # 🎯 Pass goal
            goal=goal,
            # 🎯 Pass outcome
            outcome=outcome,
        # 🔍 Check if the condition evaluates to True
        ):
            # 🧩 Append the read_file capability to selected list
            selected.append(self._get("read_file"))
# 🈳 Blank line

        # 📂 Explicit directory inspection.
        if self._is_directory_listing_request(
            # 🎯 Pass goal
            goal=goal,
            # 🎯 Pass outcome
            outcome=outcome,
        # 🔍 Check if the condition evaluates to True
        ):
            # 🧩 Append the list_directory capability
            selected.append(self._get("list_directory"))
# 🈳 Blank line

        # 🧪 Test execution.
        if self._is_test_execution_request(
            # 🎯 Pass goal
            goal=goal,
            # 🎯 Pass outcome
            outcome=outcome,
            # 🎯 Pass criteria
            criteria=criteria,
        # 🔍 Check if the condition evaluates to True
        ):
            # 🧩 Append the run_command capability
            selected.append(self._get("run_command"))
# 🈳 Blank line

        # 🐍 Direct Python-script execution.
        # Do NOT infer this merely because the user mentioned Python.
        if self._is_python_execution_request(
            # 🎯 Pass goal
            goal=goal,
            # 🎯 Pass outcome
            outcome=outcome,
        # 🔍 Check if the condition evaluates to True
        ):
            # 🧩 Append the run_python capability
            selected.append(self._get("run_python"))
# 🈳 Blank line

        # 🔀 File movement / archiving.
        if self._is_move_request(
            # 🎯 Pass goal
            goal=goal,
            # 🎯 Pass outcome
            outcome=outcome,
            # 🎯 Pass constraints
            constraints=constraints,
        # 🔍 Check if the condition evaluates to True
        ):
            # 🧩 Append the move_file capability
            selected.append(self._get("move_file"))
# 🈳 Blank line

        # 🐙 Git inspection.
        if "git status" in goal or "working tree" in goal:
            # 🧩 Append the git_status capability
            selected.append(self._get("git_status"))
# 🈳 Blank line

        # 🐙 Git diff check
        if "git diff" in goal or "show the diff" in goal:
            # 🧩 Append the git_diff capability
            selected.append(self._get("git_diff"))
# 🈳 Blank line

        # 🐙 Git log check condition start
        if (
            # 🐙 Check for git log
            "git log" in goal
            # 🐙 Check for recent commits
            or "recent commits" in goal
            # 🐙 Check for commit history
            or "commit history" in goal
        # 🐙 Close condition parenthesis
        ):
            # 🧩 Append the git_log capability
            selected.append(self._get("git_log"))
# 🈳 Blank line

        # 🔍 Deduplicate and return the selected capabilities
        return self._deduplicate(selected)
# 🈳 Blank line

    # 🔍 Define static helper method to detect file read requests
    @staticmethod
    def _is_file_read_request(
        # 🎯 Pass goal string
        goal: str,
        # 🎯 Pass outcome string
        outcome: str,
    # ⚙️ Return boolean indicating match
    ) -> bool:
        # 🔍 Combine text fields for searching
        text = " ".join(
            # 🔍 List containing goal and outcome
            [
                # 🎯 Goal string
                goal,
                # 🎯 Outcome string
                outcome,
            # 🔍 Close list
            ]
        # 🔍 Close join method
        )
# 🈳 Blank line

        # 🔍 Define a tuple of explicit search terms
        explicit_terms = (
            # 🔍 Term 'read file'
            "read file",
            # 🔍 Term 'read the file'
            "read the file",
            # 🔍 Term 'read '
            "read ",
            # 🔍 Term 'open file'
            "open file",
            # 🔍 Term 'open the file'
            "open the file",
            # 🔍 Term 'file contents'
            "file contents",
            # 🔍 Term 'contents of the file'
            "contents of the file",
            # 🔍 Term 'content of'
            "content of",
            # 🔍 Term 'readme'
            "readme",
        # 🔍 Close explicit_terms tuple
        )
# 🈳 Blank line

        # 🔍 Return True if any term is found in the text
        return any(
            # 🔍 Check if term is in text
            term in text
            # 🔍 Iterate over explicit terms
            for term in explicit_terms
        # 🔍 Close any function
        )
# 🈳 Blank line

    # 🔍 Define static helper method to detect directory listing requests
    @staticmethod
    def _is_directory_listing_request(
        # 🎯 Pass goal string
        goal: str,
        # 🎯 Pass outcome string
        outcome: str,
    # ⚙️ Return boolean indicating match
    ) -> bool:
        # 🔍 Define a tuple of explicit search terms
        explicit_terms = (
            # 🔍 Term 'list directory'
            "list directory",
            # 🔍 Term 'list the directory'
            "list the directory",
            # 🔍 Term 'list folder'
            "list folder",
            # 🔍 Term 'list the folder'
            "list the folder",
            # 🔍 Term 'directory contents'
            "directory contents",
            # 🔍 Term 'folder contents'
            "folder contents",
            # 🔍 Term 'inspect this folder'
            "inspect this folder",
            # 🔍 Term 'inspect the folder'
            "inspect the folder",
            # 🔍 Term 'inspect this directory'
            "inspect this directory",
            # 🔍 Term 'inspect the directory'
            "inspect the directory",
        # 🔍 Close explicit_terms tuple
        )
# 🈳 Blank line

        # 🔍 Return True if any term is found in goal or outcome
        return any(
            # 🔍 Check if term is in goal or outcome
            term in goal or term in outcome
            # 🔍 Iterate over explicit terms
            for term in explicit_terms
        # 🔍 Close any function
        )
# 🈳 Blank line

    # 🔍 Define static helper method to detect test execution requests
    @staticmethod
    def _is_test_execution_request(
        # 🎯 Pass goal string
        goal: str,
        # 🎯 Pass outcome string
        outcome: str,
        # 🎯 Pass criteria string
        criteria: str,
    # ⚙️ Return boolean indicating match
    ) -> bool:
        # 🔍 Combine text fields for searching
        text = " ".join(
            # 🔍 List containing goal, outcome, criteria
            [
                # 🎯 Goal string
                goal,
                # 🎯 Outcome string
                outcome,
                # 🎯 Criteria string
                criteria,
            # 🔍 Close list
            ]
        # 🔍 Close join method
        )
# 🈳 Blank line

        # 🔍 Define a tuple of test execution search terms
        test_terms = (
            # 🔍 Term 'run the tests'
            "run the tests",
            # 🔍 Term 'run tests'
            "run tests",
            # 🔍 Term 'run the test suite'
            "run the test suite",
            # 🔍 Term 'run test suite'
            "run test suite",
            # 🔍 Term 'run the project tests'
            "run the project tests",
            # 🔍 Term 'run the project's tests'
            "run the project's tests",
            # 🔍 Term 'pytest'
            "pytest",
            # 🔍 Term 'execute the tests'
            "execute the tests",
            # 🔍 Term 'execute tests'
            "execute tests",
            # 🔍 Term 'execute the test suite'
            "execute the test suite",
        # 🔍 Close test_terms tuple
        )
# 🈳 Blank line

        # 🔍 Return True if any term is found in the text
        return any(
            # 🔍 Check if term is in text
            term in text
            # 🔍 Iterate over test terms
            for term in test_terms
        # 🔍 Close any function
        )
# 🈳 Blank line

    # 🔍 Define static helper method to detect python execution requests
    @staticmethod
    def _is_python_execution_request(
        # 🎯 Pass goal string
        goal: str,
        # 🎯 Pass outcome string
        outcome: str,
    # ⚙️ Return boolean indicating match
    ) -> bool:
        # 🔍 Combine text fields for searching
        text = " ".join(
            # 🔍 List containing goal, outcome
            [
                # 🎯 Goal string
                goal,
                # 🎯 Outcome string
                outcome,
            # 🔍 Close list
            ]
        # 🔍 Close join method
        )
# 🈳 Blank line

        # 🔍 Define a tuple of python execution search terms
        python_execution_terms = (
            # 🔍 Term 'run this python script'
            "run this python script",
            # 🔍 Term 'run the python script'
            "run the python script",
            # 🔍 Term 'execute this python script'
            "execute this python script",
            # 🔍 Term 'execute the python script'
            "execute the python script",
            # 🔍 Term 'run a python script'
            "run a python script",
            # 🔍 Term 'execute a python script'
            "execute a python script",
        # 🔍 Close python_execution_terms tuple
        )
# 🈳 Blank line

        # 🔍 Return True if any term is found in the text
        return any(
            # 🔍 Check if term is in text
            term in text
            # 🔍 Iterate over python execution terms
            for term in python_execution_terms
        # 🔍 Close any function
        )
# 🈳 Blank line

    # 🔍 Define static helper method to detect move requests
    @staticmethod
    def _is_move_request(
        # 🎯 Pass goal string
        goal: str,
        # 🎯 Pass outcome string
        outcome: str,
        # 🎯 Pass constraints string
        constraints: str,
    # ⚙️ Return boolean indicating match
    ) -> bool:
        # 🔍 Combine text fields for searching
        text = " ".join(
            # 🔍 List containing goal, outcome, constraints
            [
                # 🎯 Goal string
                goal,
                # 🎯 Outcome string
                outcome,
                # 🎯 Constraints string
                constraints,
            # 🔍 Close list
            ]
        # 🔍 Close join method
        )
# 🈳 Blank line

        # 🔍 Define a tuple of move request search terms
        move_terms = (
            # 🔍 Term 'move file'
            "move file",
            # 🔍 Term 'move the file'
            "move the file",
            # 🔍 Term 'move files'
            "move files",
            # 🔍 Term 'move the files'
            "move the files",
            # 🔍 Term 'archive file'
            "archive file",
            # 🔍 Term 'archive the file'
            "archive the file",
            # 🔍 Term 'archive files'
            "archive files",
            # 🔍 Term 'archive the files'
            "archive the files",
        # 🔍 Close move_terms tuple
        )
# 🈳 Blank line

        # 🔍 Return True if any term is found in the text
        return any(
            # 🔍 Check if term is in text
            term in text
            # 🔍 Iterate over move terms
            for term in move_terms
        # 🔍 Close any function
        )
# 🈳 Blank line

    # 🔍 Define static helper method to retrieve a capability by name
    @staticmethod
    def _get(name: str) -> Capability:
        # 🔍 Iterate through globally defined capabilities
        for capability in CAPABILITIES:
            # 🔍 Check if capability name matches the requested name
            if capability.name == name:
                # 🧩 Return the matching capability
                return capability
# 🈳 Blank line

        # 🛑 Raise ValueError if no matching capability is found
        raise ValueError(
            # 🛑 Format error message with unknown capability name
            f"Unknown capability: {name}"
        # 🛑 Close ValueError parenthesis
        )
# 🈳 Blank line

    # 🔍 Define static helper method to deduplicate a list of capabilities
    @staticmethod
    def _deduplicate(
        # 🧩 Pass list of capabilities
        capabilities: list[Capability],
    # ⚙️ Return deduplicated list of capabilities
    ) -> list[Capability]:
        # 🔍 Initialize a set to track seen capability names
        seen: set[str] = set()
        # 🔍 Initialize empty list for unique capabilities
        result: list[Capability] = []
# 🈳 Blank line

        # 🔍 Iterate over input capabilities
        for capability in capabilities:
            # 🔍 Check if capability name has already been seen
            if capability.name in seen:
                # 🔍 Skip to next capability if already seen
                continue
# 🈳 Blank line

            # 🔍 Add capability name to seen set
            seen.add(capability.name)
            # 🧩 Append the unique capability to result list
            result.append(capability)
# 🈳 Blank line

        # 🔍 Return the list of unique capabilities
        return result