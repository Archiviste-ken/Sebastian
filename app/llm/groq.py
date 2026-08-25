from typing import Any # 📦 Import Any type for generic type annotations

from groq import AuthenticationError, Groq # 📦 Import Groq client and its authentication error class

from app.llm.gateway import ModelGateway, ModelResponse # 📦 Import base classes for the gateway implementation


class GroqModelGateway(ModelGateway): # 📡 Groq-specific implementation of the ModelGateway
    def __init__( # 🏗️ Constructor for the Groq gateway
        self, # 🎯 Reference to the instance
        model: str, # 📝 The specific model identifier to use
        client: Any | None = None, # 📦 Optional pre-configured client instance
        api_key: str | None = None, # 🔐 Optional API key string
    ): # ✅ End of constructor arguments
        self.model = model # 💾 Store the model identifier

        if client is not None: # 🔍 Check if a client was explicitly provided
            self.client = client # 💾 Use the provided client
        else: # 🔍 Fall back to creating a new client
            key = api_key or "" # 🔐 Retrieve the API key or use an empty string

            if not key.strip(): # 🔍 Check if the key is effectively empty
                raise RuntimeError( # ❌ Raise a runtime error if no valid key is found
                    "Groq API key is required." # ❌ Error message indicating the missing key
                ) # ✅ End of raise statement

            self.client = Groq( # 🏗️ Instantiate a new Groq client
                api_key=key, # 🔐 Pass the API key to the client
            ) # ✅ End of Groq client initialization

    def generate( # 📡 Implement the generate method for Groq
        self, # 🎯 Reference to the instance
        messages: list[dict[str, str]], # 📝 The conversation messages
        response_format: dict[str, Any] | None = None, # 📝 Optional specific format for the output
    ) -> ModelResponse: # 📝 Promise to return a ModelResponse
        request: dict[str, Any] = { # 📝 Initialize the request payload dictionary
            "model": self.model, # 📝 Set the model identifier in the request
            "messages": messages, # 📝 Include the messages in the request
        } # ✅ End of base request payload

        if response_format is not None: # 🔍 Check if a specific response format is requested
            request["response_format"] = response_format # 📝 Add the format to the payload if requested

        try: # 🔍 Begin error-handling block for the API call
            response = self.client.chat.completions.create( # 📡 Send the request to the Groq API
                **request, # 📦 Unpack the payload dictionary as keyword arguments
            ) # ✅ End of API call
        except AuthenticationError as exc: # ❌ Catch specific authentication errors
            raise RuntimeError( # ❌ Raise a unified runtime error
                "Groq authentication failed: verify GROQ_API_KEY in .env." # ❌ Provide a helpful error message
            ) from exc # 🔗 Chain the original exception for debugging context

        content = response.choices[0].message.content or "" # 🔍 Extract the text content safely, falling back to empty string

        return ModelResponse( # 📝 Construct the unified response object
            content=content, # 📝 Pass the extracted text content
            raw=response, # 📦 Include the raw Groq response for advanced access
        ) # ✅ End of return statement
