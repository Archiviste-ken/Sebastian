from pathlib import Path  # 📦 Import Path object for filesystem path resolution

from dotenv import dotenv_values, load_dotenv  # 📦 Import functions to load environment variables from .env


PROJECT_ROOT = Path(__file__).resolve().parent.parent  # 🔧 Calculate absolute path to the root of the project
DOTENV_PATH = PROJECT_ROOT / ".env"  # 🔧 Define the path to the .env configuration file

# 📝 Load the project-local file explicitly.  ``override=True`` prevents an old
# 📝 Windows process environment value from being used by any code that consults
# 📝 ``os.environ`` directly.
load_dotenv(dotenv_path=DOTENV_PATH, override=True)  # 🔧 Load the .env file variables into the environment, overriding existing ones


class Settings:  # 🔧 Define a Settings class to hold application configuration state
    def __init__(self):  # 🏗️ Constructor to initialize the Settings object
        # 📝 Read this credential from the project-local .env as the single
        # 📝 source of truth, rather than falling back to the process environment.
        self.groq_api_key = dotenv_values(DOTENV_PATH).get("GROQ_API_KEY") or ""  # 🔑 Retrieve the GROQ_API_KEY from .env or default to empty string

        if not self.groq_api_key.strip():  # 🛡️ Validate that the API key is not empty or just whitespace
            raise RuntimeError(  # ❌ Raise a RuntimeError exception if validation fails
                "GROQ_API_KEY is not configured in .env."  # ❌ Error message indicating the missing configuration
            )  # ❌ Close the raise statement
