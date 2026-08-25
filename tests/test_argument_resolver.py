from app.intent.models import Intent
from app.llm.gateway import ModelResponse
from app.planning.argument_resolver import ArgumentResolver
from app.tools.definition import ToolDefinition


class FakeGateway:
    def generate(self, messages, response_format=None):
        return ModelResponse(
            content=(
                "{"
                '"tool_name":"read_file",'
                '"arguments":{"path":"README.md"}'
                "}"
            )
        )


def test_argument_resolver_resolves_file_path():
    resolver = ArgumentResolver(
        gateway=FakeGateway(),
    )

    tool = ToolDefinition(
        name="read_file",
        description="Read a file.",
        handler=lambda path: path,
        argument_schema={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                },
            },
            "required": ["path"],
            "additionalProperties": False,
        },
    )

    intent = Intent(
        goal="Read README.md",
        constraints=[],
        expected_outcome="Return the README contents.",
        forbidden_actions=[],
        missing_information=[],
        required_permissions=["filesystem"],
        success_criteria=[
            "README contents are returned.",
        ],
    )

    arguments = resolver.resolve(
        intent=intent,
        tool=tool,
    )

    assert arguments == {
        "path": "README.md",
    }