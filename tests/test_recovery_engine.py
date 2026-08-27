import pytest

from app.models.tool_result import ToolResult, ToolResultStatus
from app.planning.models import Action, ActionRisk, RetryPolicy
from app.recovery.engine import RecoveryEngine, MAX_RETRIES
from app.recovery.models import RecoveryStrategy


def _action(risk=ActionRisk.LOW, retry_policy=RetryPolicy.SAFE):
    return Action(
        action_id="a-1",
        tool="read_file",
        arguments={},
        expected_result="ok",
        risk=risk,
        retry_policy=retry_policy,
        verification_method="test",
    )


def _fail():
    return ToolResult(status=ToolResultStatus.FAILED, error="broke")


@pytest.fixture
def engine():
    return RecoveryEngine()


def test_never_policy_always_fails(engine):
    d = engine.attempt(_action(retry_policy=RetryPolicy.NEVER), _fail(), 0)
    assert d.strategy == RecoveryStrategy.FAIL


def test_safe_low_risk_retries(engine):
    d = engine.attempt(_action(risk=ActionRisk.LOW, retry_policy=RetryPolicy.SAFE), _fail(), 0)
    assert d.strategy == RecoveryStrategy.RETRY


def test_safe_medium_risk_retries(engine):
    d = engine.attempt(_action(risk=ActionRisk.MEDIUM, retry_policy=RetryPolicy.SAFE), _fail(), 1)
    assert d.strategy == RecoveryStrategy.RETRY


def test_safe_high_risk_fails(engine):
    d = engine.attempt(_action(risk=ActionRisk.HIGH, retry_policy=RetryPolicy.SAFE), _fail(), 0)
    assert d.strategy == RecoveryStrategy.FAIL


def test_always_policy_retries(engine):
    d = engine.attempt(_action(retry_policy=RetryPolicy.ALWAYS), _fail(), 0)
    assert d.strategy == RecoveryStrategy.RETRY


def test_always_high_risk_retries(engine):
    d = engine.attempt(_action(risk=ActionRisk.HIGH, retry_policy=RetryPolicy.ALWAYS), _fail(), 0)
    assert d.strategy == RecoveryStrategy.RETRY


def test_max_retries_exceeded(engine):
    d = engine.attempt(_action(retry_policy=RetryPolicy.ALWAYS), _fail(), MAX_RETRIES)
    assert d.strategy == RecoveryStrategy.FAIL
    assert "exceeded" in d.reason.lower()


def test_max_retries_boundary(engine):
    d = engine.attempt(_action(retry_policy=RetryPolicy.ALWAYS), _fail(), MAX_RETRIES - 1)
    assert d.strategy == RecoveryStrategy.RETRY
