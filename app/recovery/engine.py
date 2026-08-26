"""Bounded, policy-driven recovery engine."""

from app.models.tool_result import ToolResult
from app.planning.models import Action, ActionRisk, RetryPolicy
from app.recovery.models import RecoveryDecision, RecoveryStrategy

MAX_RETRIES = 3


class RecoveryEngine:
    """Decides whether a failed action should be retried, skipped, or abandoned.

    Rules (all deterministic, no LLM calls):
    - NEVER policy → always FAIL
    - Exceeded MAX_RETRIES → FAIL
    - HIGH risk + SAFE policy → FAIL (never retry dangerous ops with conservative policy)
    - SAFE policy + LOW/MEDIUM risk → RETRY
    - ALWAYS policy → RETRY (regardless of risk, up to MAX_RETRIES)
    """

    def attempt(
        self,
        action: Action,
        tool_result: ToolResult,
        attempt_count: int,
    ) -> RecoveryDecision:
        if action.retry_policy == RetryPolicy.NEVER:
            return RecoveryDecision(
                strategy=RecoveryStrategy.FAIL,
                reason="Retry policy is NEVER.",
            )

        if attempt_count >= MAX_RETRIES:
            return RecoveryDecision(
                strategy=RecoveryStrategy.FAIL,
                reason=f"Maximum retries ({MAX_RETRIES}) exceeded.",
            )

        if action.risk == ActionRisk.HIGH and action.retry_policy == RetryPolicy.SAFE:
            return RecoveryDecision(
                strategy=RecoveryStrategy.FAIL,
                reason="HIGH risk action cannot be retried with SAFE policy.",
            )

        if action.retry_policy == RetryPolicy.SAFE:
            return RecoveryDecision(
                strategy=RecoveryStrategy.RETRY,
                reason=(
                    f"SAFE retry for {action.risk.value} risk action "
                    f"(attempt {attempt_count + 1}/{MAX_RETRIES})."
                ),
            )

        if action.retry_policy == RetryPolicy.ALWAYS:
            return RecoveryDecision(
                strategy=RecoveryStrategy.RETRY,
                reason=f"ALWAYS retry (attempt {attempt_count + 1}/{MAX_RETRIES}).",
            )

        return RecoveryDecision(
            strategy=RecoveryStrategy.FAIL,
            reason="No applicable recovery strategy.",
        )
