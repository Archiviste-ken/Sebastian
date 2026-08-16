from app.models.permission import Permission, PermissionLevel


def test_permission_creation():
    permission = Permission(
        id="permission-1",
        tool_name="read_file",
        level=PermissionLevel.AUTONOMOUS,
    )

    assert permission.tool_name == "read_file"
    assert permission.level == PermissionLevel.AUTONOMOUS