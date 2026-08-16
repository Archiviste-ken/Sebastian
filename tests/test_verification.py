from app.models.verification import Verification


def test_verification_creation():
    verification = Verification(
        id="verification-1",
        task_id="task-1",
        success=True,
        method="pytest",
        evidence={
            "tests_passed": 15,
            "tests_failed": 0,
        },
    )

    assert verification.success is True
    assert verification.evidence["tests_failed"] == 0