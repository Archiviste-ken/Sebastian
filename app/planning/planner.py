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
        # 🔍 Check if the intent has missing information
        if intent.missing_information:
            # 🗺️ Return a plan focused on retrieving missing information
            return Plan(
                # 🎯 Set the goal from the original intent
                goal=intent.goal,
                # 🗺️ Define the list of actions
                actions=[
                    # 🗺️ Define the action to request information
                    Action(
                        # 🗺️ Set action_id
                        action_id="request-missing-information",
                        # 🧰 Specify the tool to use
                        tool="ask_user",
                        # ⚙️ Provide the arguments for the tool
                        arguments={
                            # ⚙️ Pass the missing information as questions
                            "questions": intent.missing_information,
                        # ⚙️ Close arguments dictionary
                        },
                        # 🎯 Define the expected result of this action
                        expected_result=(
                            # 🎯 Describe user providing information
                            "The user provides the missing "
                            # 🎯 Describe required information
                            "information required to proceed."
                        # 🎯 Close expected_result string tuple
                        ),
                        # 🧩 Set the risk level to LOW
                        risk=ActionRisk.LOW,
                        # ⚙️ Set the timeout to 30 seconds
                        timeout_seconds=30,
                        # 🧩 Set the retry policy to NEVER
                        retry_policy=RetryPolicy.NEVER,
                        # 🔍 Define the method to verify success
                        verification_method=(
                            # 🔍 Describe confirmation
                            "Confirm all required information "
                            # 🔍 Describe provision
                            "has been provided."
                        # 🔍 Close verification_method string tuple
                        ),
                    # 🗺️ Close Action instantiation
                    )
                # 🗺️ Close actions list
                ],
                # 🎯 Define the success criteria for this plan
                success_criteria=[
                    # 🎯 Specify all information available
                    "All required information is available.",
                # 🎯 Close success_criteria list
                ],
            # 🗺️ Close Plan instantiation
            )
# 🈳 Blank line

        # 🔍 Use the selector to identify capabilities matching the intent
        capabilities = self.selector.select(intent)
# 🈳 Blank line

        # 🔍 Check if no capabilities were found
        if not capabilities:
            # 🗺️ Return a plan asking the user for clarification
            return Plan(
                # 🎯 Set the goal from the original intent
                goal=intent.goal,
                # 🗺️ Define the list of actions
                actions=[
                    # 🗺️ Define the action to ask the user
                    Action(
                        # 🗺️ Set action_id
                        action_id="no-capability-found",
                        # 🧰 Specify the ask_user tool
                        tool="ask_user",
                        # ⚙️ Provide the arguments for the tool
                        arguments={
                            # ⚙️ Set the questions list
                            "questions": [
                                # ⚙️ Provide the question text
                                "No available Sebastian capability "
                                # ⚙️ Provide the reason
                                "matches this request."
                            # ⚙️ Close questions list
                            ]
                        # ⚙️ Close arguments dictionary
                        },
                        # 🎯 Define expected result
                        expected_result=(
                            # 🎯 Describe user providing clarification
                            "The user provides clarification."
                        # 🎯 Close expected_result tuple
                        ),
                        # 🧩 Set risk to LOW
                        risk=ActionRisk.LOW,
                        # ⚙️ Set timeout to 30 seconds
                        timeout_seconds=30,
                        # 🧩 Set retry policy to NEVER
                        retry_policy=RetryPolicy.NEVER,
                        # 🔍 Define verification method
                        verification_method=(
                            # 🔍 Verify supported capability
                            "Confirm a supported capability exists."
                        # 🔍 Close verification_method tuple
                        ),
                    # 🗺️ Close Action instantiation
                    )
                # 🗺️ Close actions list
                ],
                # 🎯 Define the success criteria
                success_criteria=[
                    # 🎯 Specify identification of capability
                    "A supported capability is identified.",
                # 🎯 Close success_criteria list
                ],
            # 🗺️ Close Plan instantiation
            )
# 🈳 Blank line

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