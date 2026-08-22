from app.security.permissions import (
    PermissionKernel,
    PermissionLevel,
)


def test_autonomous_permission():
    kernel = PermissionKernel(
        {
            "read_file": PermissionLevel.AUTONOMOUS,
        }
    )

    assert kernel.get_level("read_file") == PermissionLevel.AUTONOMOUS


def test_approval_permission():
    kernel = PermissionKernel(
        {
            "write_file": PermissionLevel.APPROVAL,
        }
    )

    assert kernel.get_level("write_file") == PermissionLevel.APPROVAL


def test_blocked_permission():
    kernel = PermissionKernel(
        {
            "delete_file": PermissionLevel.BLOCKED,
        }
    )

    assert kernel.get_level("delete_file") == PermissionLevel.BLOCKED


def test_unknown_tool_defaults_to_blocked():
    kernel = PermissionKernel({})

    assert kernel.get_level("unknown_tool") == PermissionLevel.BLOCKED
    
    
def test_autonomous_tool_is_allowed():
    kernel = PermissionKernel(
        {
            "read_file": PermissionLevel.AUTONOMOUS,
        }
    )

    decision = kernel.check("read_file")

    assert decision.allowed is True
    assert decision.requires_approval is False


def test_approval_tool_requires_approval():
    kernel = PermissionKernel(
        {
            "write_file": PermissionLevel.APPROVAL,
        }
    )

    decision = kernel.check("write_file")

    assert decision.allowed is False
    assert decision.requires_approval is True


def test_blocked_tool_is_denied():
    kernel = PermissionKernel(
        {
            "delete_file": PermissionLevel.BLOCKED,
        }
    )

    decision = kernel.check("delete_file")

    assert decision.allowed is False
    assert decision.requires_approval is False


def test_unknown_tool_is_blocked():
    kernel = PermissionKernel({})

    decision = kernel.check("unknown_tool")

    assert decision.allowed is False
    assert decision.requires_approval is False