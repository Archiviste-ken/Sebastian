from dataclasses import dataclass # 📦 Import dataclass decorator for simple data structures
from typing import Any # 📦 Import Any type for generic type annotations


@dataclass(frozen=True) # 🏗️ Define an immutable dataclass using the frozen parameter
class ModelResponse: # 📝 Class to encapsulate the response from a language model
    content: str # 📝 The main string content returned by the model
    raw: Any = None # 📦 The raw, provider-specific response object for advanced usage


class ModelGateway: # 📡 Base class for model gateways handling API interactions
    def generate( # 📡 Define the abstract generate method
        self, # 🎯 Reference to the instance
        messages: list[dict[str, str]], # 📝 List of message dictionaries for the conversation
        response_format: dict[str, Any] | None = None, # 📝 Optional response format specification
    ) -> ModelResponse: # 📝 Return a ModelResponse instance
        raise NotImplementedError # ❌ Raise error to enforce implementation in subclasses