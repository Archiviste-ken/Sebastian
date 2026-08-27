# 📦 Import Intent model from app.intent.models
from app.intent.models import Intent
# 📦 Import Action, ActionRisk, Plan, RetryPolicy from app.planning.models
from app.planning.models import (
    # 📦 Import Action model
    Action,
    # 📦 Import ActionRisk enum
    ActionRisk,
    # 📦 Import Plan model
    Plan,
    # 📦 Import RetryPolicy enum
    RetryPolicy,
# 📦 Close imports block
)
# 📦 Import CapabilitySelector from app.planning.selector
from app.planning.selector import CapabilitySelector
# 🈳 Blank line
# 🈳 Blank line

# 🗺️ Define Planner class responsible for generating execution plans
class Planner:
    # ⚙️ Initialize the Planner with an optional CapabilitySelector
    def __init__(
        # ⚙️ Pass self reference
        self,
        # 🔍 Pass selector instance, default None
        selector: CapabilitySelector | None = None,
    # ⚙️ End of parameters
    ):
        # 🔗 Store provided selector or create a new CapabilitySelector
        self.selector = selector or CapabilitySelector()
# 🈳 Blank line

    # 🗺️ Define build method to create a Plan from an Intent
    def build(self, intent: Intent) -> Plan:
        # 🔍 Use the selector to identify capabilities matching the intent
        capabilities = self.selector.select(intent)

        # 🔍 Check if no capabilities were found
        if not capabilities:
            raise ValueError("No available Sebastian capability matches this request.")

        # 🗺️ Initialize empty list for actions
        actions = []
# 🈳 Blank line

        # 🗺️ Iterate over selected capabilities to create actions
        for index, capability in enumerate(
            # 🗺️ Iterate over capabilities list
            capabilities,
            # 🗺️ Start enumeration at 1
            start=1,
        # 🗺️ End of for loop definition
        ):
            # 🗺️ Append a new Action for the capability
            actions.append(
                # 🗺️ Instantiate a new Action
                Action(
                    # 🗺️ Generate action_id with index
                    action_id=f"candidate-{index}",
                    # 🧰 Set tool to capability name
                    tool=capability.name,
                    # ⚙️ Set empty arguments (to be resolved later)
                    arguments={},
                    # 🎯 Set expected result using capability description
                    expected_result=(
                        # 🎯 Format description
                        f"{capability.description} succeeds."
                    # 🎯 Close expected_result tuple
                    ),
                    # 🧩 Wrap capability risk in ActionRisk enum
                    risk=ActionRisk(
                        # 🧩 Provide risk string
                        capability.risk
                    # 🧩 Close ActionRisk call
                    ),
                    # ⚙️ Set timeout to 30 seconds
                    timeout_seconds=30,
                    # 🧩 Set retry policy to NEVER
                    retry_policy=RetryPolicy.NEVER,
                    # 🔍 Define verification method
                    verification_method=(
                        # 🔍 Instruct to inspect tool result
                        "Inspect the structured tool result."
                    # 🔍 Close verification_method tuple
                    ),
                # 🗺️ Close Action instantiation
                )
            # 🗺️ Close append call
            )
# 🈳 Blank line

        # 🗺️ Return the complete assembled plan
        return Plan(
            # 🎯 Set goal from intent
            goal=intent.goal,
            # 🗺️ Pass the accumulated actions
            actions=actions,
            # 🎯 Set success criteria, falling back to expected_outcome
            success_criteria=intent.success_criteria or [
                # 🎯 Use expected_outcome as criteria fallback
                intent.expected_outcome,
            # 🎯 Close fallback list
            ],
        # 🗺️ Close Plan instantiation
        )