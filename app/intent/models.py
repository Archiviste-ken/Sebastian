from pydantic import BaseModel, Field # 📦 Import BaseModel and Field for defining data models

class Intent(BaseModel): # 📝 Define the Intent data model inheriting from Pydantic's BaseModel
    goal: str = Field( # 🎯 Define the goal field as a string with extra metadata
        min_length=1, # 🎯 Require the goal to be at least 1 character long
        description="What the user ultimately wants accomplished.", # 📝 Provide a description for the goal field
    ) # ✅ End of goal field definition

    constraints: list[str] = Field( # 🎯 Define the constraints field as a list of strings
        default_factory=list, # 📝 Default to an empty list if not provided
        description="Rules or limitations that must be respected.", # 📝 Provide a description for the constraints field
    ) # ✅ End of constraints field definition

    expected_outcome: str = Field( # 🎯 Define the expected_outcome field as a string
        min_length=1, # 🎯 Require the expected outcome to be at least 1 character long
        description="What the successful final result should look like.", # 📝 Provide a description for the expected outcome field
    ) # ✅ End of expected_outcome field definition

    forbidden_actions: list[str] = Field( # ❌ Define the forbidden_actions field as a list of strings
        default_factory=list, # 📝 Default to an empty list if not provided
        description="Actions Sebastian must not take.", # 📝 Provide a description for the forbidden actions field
    ) # ✅ End of forbidden_actions field definition

    missing_information: list[str] = Field( # 🔍 Define the missing_information field as a list of strings
        default_factory=list, # 📝 Default to an empty list if not provided
        description="Information needed before execution can safely proceed.", # 📝 Provide a description for the missing information field
    ) # ✅ End of missing_information field definition

    required_permissions: list[str] = Field( # 🔐 Define the required_permissions field as a list of strings
        default_factory=list, # 📝 Default to an empty list if not provided
        description="Permissions that may be required.", # 📝 Provide a description for the required permissions field
    ) # ✅ End of required_permissions field definition

    success_criteria: list[str] = Field( # ✅ Define the success_criteria field as a list of strings
        default_factory=list, # 📝 Default to an empty list if not provided
        description="Checks that determine whether the task succeeded.", # 📝 Provide a description for the success criteria field
    ) # ✅ End of success_criteria field definition