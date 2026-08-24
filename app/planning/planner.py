from app.intent.models import Intent
from app.planning.models import (
    Action,
    ActionRisk,
    Plan,
    RetryPolicy,
)
from app.planning.selector import CapabilitySelector


class Planner:
    def __init__(
        self,
        selector: CapabilitySelector | None = None,
    ):
        self.selector = selector or CapabilitySelector()

    def build(self, intent: Intent) -> Plan:
        if intent.missing_information:
            return Plan(
                goal=intent.goal,
                actions=[
                    Action(
                        action_id="request-missing-information",
                        tool="ask_user",
                        arguments={
                            "questions": intent.missing_information,
                        },
                        expected_result=(
                            "The user provides the missing "
                            "information required to proceed."
                        ),
                        risk=ActionRisk.LOW,
                        timeout_seconds=30,
                        retry_policy=RetryPolicy.NEVER,
                        verification_method=(
                            "Confirm all required information "
                            "has been provided."
                        ),
                    )
                ],
                success_criteria=[
                    "All required information is available.",
                ],
            )

        capabilities = self.selector.select(intent)

        if not capabilities:
            return Plan(
                goal=intent.goal,
                actions=[
                    Action(
                        action_id="no-capability-found",
                        tool="ask_user",
                        arguments={
                            "questions": [
                                "No available Sebastian capability "
                                "matches this request."
                            ]
                        },
                        expected_result=(
                            "The user provides clarification."
                        ),
                        risk=ActionRisk.LOW,
                        timeout_seconds=30,
                        retry_policy=RetryPolicy.NEVER,
                        verification_method=(
                            "Confirm a supported capability exists."
                        ),
                    )
                ],
                success_criteria=[
                    "A supported capability is identified.",
                ],
            )

        actions = []

        for index, capability in enumerate(
            capabilities,
            start=1,
        ):
            actions.append(
                Action(
                    action_id=f"candidate-{index}",
                    tool=capability.name,
                    arguments={},
                    expected_result=(
                        f"{capability.description} succeeds."
                    ),
                    risk=ActionRisk(
                        capability.risk
                    ),
                    timeout_seconds=30,
                    retry_policy=RetryPolicy.NEVER,
                    verification_method=(
                        "Inspect the structured tool result."
                    ),
                )
            )

        return Plan(
            goal=intent.goal,
            actions=actions,
            success_criteria=intent.success_criteria or [
                intent.expected_outcome,
            ],
        )