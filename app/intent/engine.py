from typing import Any # 📦 Import Any type for generic type annotations

from app.intent.models import Intent # 📦 Import the Intent Pydantic model
from app.llm.gateway import ModelGateway # 📦 Import the base ModelGateway for LLM calls


class IntentEngine: # 🧠 Main class for extracting user intents using LLMs
    def __init__(self, gateway: ModelGateway): # 🏗️ Constructor requiring an LLM gateway instance
        self.gateway = gateway # 💾 Save the gateway instance as a class attribute

    def _strict_schema(self) -> dict[str, Any]: # 🔍 Helper method to create a strict JSON schema
        schema = Intent.model_json_schema() # 📝 Generate base JSON schema from the Intent model

        properties = schema.get("properties", {}) # 🔍 Extract properties from the schema safely

        # 🧠 Groq strict Structured Outputs requires every property
        # 🧠 to be required.
        schema["required"] = list(properties.keys()) # 🎯 Force all properties to be required in the schema
        schema["additionalProperties"] = False # ❌ Reject any additional properties not in schema

        # 🧠 Pydantic adds defaults for fields with default_factory.
        # 🧠 Those defaults are useful locally, but the LLM schema should
        # 🧠 describe every field as an explicit output field.
        for property_schema in properties.values(): # 🔄 Iterate over all property schemas
            property_schema.pop("default", None) # ❌ Remove default values to force LLM generation

        return schema # ✅ Return the strictly formatted schema

    def parse(self, user_request: str) -> Intent: # 📡 Main method to parse a user string into an Intent
        messages = [ # 📝 Initialize the message list for the LLM prompt
            { # 📝 Create the system message dictionary
                "role": "system", # 🎯 Set the role to system for instructions
                "content": ( # 📝 Start multi-line string for system prompt content
                    "You are Sebastian's intent extraction engine.\n\n" # 🧠 Define the persona and purpose
                    "Your job is to extract a COMPLETE structured intent " # 🎯 Emphasize complete extraction
                    "from the user's request.\n\n" # 🎯 Refer to the input request
                    "You MUST return every field defined by the schema.\n" # 🎯 Strictly enforce returning all fields
                    "NEVER omit a field.\n" # ❌ Forbid omitting fields
                    "When a list has no applicable items, return [].\n" # 🎯 Instruct on how to handle empty lists
                    "Do not omit fields merely because they are empty.\n\n" # ❌ Prevent omitting empty fields
                    "Fields:\n" # 📝 Begin field descriptions
                    "- goal: the user's primary objective\n" # 🎯 Describe the goal field
                    "- constraints: rules or limitations; use [] if none\n" # 🎯 Describe constraints field
                    "- expected_outcome: what success should produce\n" # 🎯 Describe expected outcome field
                    "- forbidden_actions: actions that must not happen; " # ❌ Describe forbidden actions field
                    "use [] if none\n" # 🎯 Instruct on empty forbidden actions
                    "- missing_information: information genuinely required FROM THE USER before "
                    "safe execution can begin. Use [] if none. "
                    "CRITICAL: Do NOT list tool-obtainable information (e.g., file contents, directory structures) "
                    "merely because Sebastian does not have it yet. If a path is explicitly provided (e.g., 'README.md'), "
                    "do NOT ask for it. Only list information that cannot be safely obtained via tools.\n"
                    "- required_permissions: permissions/capabilities that " # 🔐 Describe required permissions field
                    "may be needed; use [] if none\n" # 🎯 Instruct on empty permissions
                    "- success_criteria: conditions that indicate success; " # ✅ Describe success criteria field
                    "use [] if none" # 🎯 Instruct on empty success criteria
                ), # ✅ End of system prompt content string
            }, # ✅ End of system message dictionary
            { # 📝 Create the user message dictionary
                "role": "user", # 🎯 Set the role to user for the input
                "content": user_request, # 📝 Provide the actual user request string
            }, # ✅ End of user message dictionary
        ] # ✅ End of messages list

        response_format: dict[str, Any] = { # 📝 Define the expected response format dictionary
            "type": "json_schema", # 🎯 Specify json_schema as the format type
            "json_schema": { # 📝 Configure the json_schema details
                "name": "sebastian_intent", # 🎯 Name the schema for the LLM
                "strict": True, # 🎯 Enforce strict schema adherence
                "schema": self._strict_schema(), # 🔍 Provide the generated strict schema
            }, # ✅ End of json_schema configuration
        } # ✅ End of response_format dictionary

        response = self.gateway.generate( # 📡 Call the LLM gateway to generate a response
            messages=messages, # 📝 Pass the prepared messages list
            response_format=response_format, # 📝 Pass the strictly defined response format
        ) # ✅ End of generate call

        return Intent.model_validate_json(response.content) # 🔍 Parse and return the validated Intent model