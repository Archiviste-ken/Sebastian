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