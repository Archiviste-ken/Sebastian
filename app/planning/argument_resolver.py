# 📦 Import Any type from typing module
from typing import Any
# 🈳 Blank line

# 📦 Import Intent model from app.intent.models
from app.intent.models import Intent
# 📦 Import ModelGateway from app.llm.gateway
from app.llm.gateway import ModelGateway
# 📦 Import ResolvedArguments from app.planning.models
from app.planning.models import ResolvedArguments
# 📦 Import ToolDefinition from app.tools.definition
from app.tools.definition import ToolDefinition
# 🈳 Blank line
# 🈳 Blank line

# 🧠 Define ArgumentResolver class responsible for LLM argument resolution
class ArgumentResolver:
    # ⚙️ Initialize the ArgumentResolver with a ModelGateway
    def __init__(self, gateway: ModelGateway):
        # 🔗 Store the gateway instance variable
        self.gateway = gateway
# 🈳 Blank line

    # ⚙️ Define resolve method to get tool arguments based on intent
    def resolve(
        # ⚙️ Pass self reference
        self,
        # 🎯 Pass the validated Intent object
        intent: Intent,
        # 🧩 Pass the selected ToolDefinition object
        tool: ToolDefinition,
    # ⚙️ Return a dictionary of resolved arguments
    ) -> dict[str, Any]:
        # 🔍 Check if the tool has an argument schema defined
        if tool.argument_schema is None:
            # 🛑 Raise ValueError if schema is missing
            raise ValueError(
                # 🛑 Format the error message with the tool name
                f"Tool '{tool.name}' has no argument schema."
            # 🛑 Close ValueError parenthesis
            )
# 🈳 Blank line

        # 🧠 Construct the messages list for the LLM
        messages = [
            # 🧠 Start system message dictionary
            {
                # 🧠 Set role to system
                "role": "system",
                # 🧠 Provide the system prompt content
                "content": (
                    # 🧠 Define the persona
                    "You are Sebastian's tool argument resolver. "
                    # 🧠 Explain the input
                    "Given a validated intent and a selected tool, "
                    # 🧠 Explain the task
                    "produce only the arguments required by that tool. "
                    # 🛑 Add negative constraint: no execution
                    "Never execute the tool. "
                    # 🛑 Add negative constraint: no hallucination
                    "Never invent missing information. "
                    # 🧠 Define fallback behavior
                    "If the required information is unavailable, "
                    # 🧠 Define fallback return value
                    "return an empty arguments object."
                # 🧠 Close content string tuple
                ),
            # 🧠 Close system message dictionary
            },
            # 🧠 Start user message dictionary
            {
                # 🧠 Set role to user
                "role": "user",
                # 🧠 Provide the user prompt content
                "content": (
                    # 🧠 Provide the serialized intent
                    f"Intent:\n{intent.model_dump_json()}\n\n"
                    # 🧠 Introduce the selected tool
                    f"Selected tool:\n"
                    # 🧠 Provide the tool name
                    f"{tool.name}\n\n"
                    # 🧠 Introduce the tool argument schema
                    f"Tool argument schema:\n"
                    # 🧠 Provide the tool argument schema
                    f"{tool.argument_schema}"
                # 🧠 Close content string tuple
                ),
            # 🧠 Close user message dictionary
            },
        # 🧠 Close messages list
        ]
# 🈳 Blank line

        # ⚙️ Call the LLM gateway to generate a response
        response = self.gateway.generate(
            # 🧠 Pass the constructed messages
            messages=messages,
        # ⚙️ Close generate method call
        )
# 🈳 Blank line

        # 🧠 Parse the LLM response into ResolvedArguments model
        resolved = ResolvedArguments.model_validate_json(
            # 🧠 Pass the text content of the LLM response
            response.content
        # 🧠 Close model_validate_json call
        )
# 🈳 Blank line

        # 🔍 Validate that the resolved tool name matches the selected tool name
        if resolved.tool_name != tool.name:
            # 🛑 Raise ValueError on mismatch
            raise ValueError(
                # 🛑 Provide error message for mismatch
                "Resolved tool does not match the selected tool."
            # 🛑 Close ValueError parenthesis
            )
# 🈳 Blank line

        # 🎯 Return the extracted arguments dictionary
        return resolved.arguments