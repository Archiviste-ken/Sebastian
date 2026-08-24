from pathlib import Path

from dotenv import dotenv_values, load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOTENV_PATH = PROJECT_ROOT / ".env"

# Load the project-local file explicitly.  ``override=True`` prevents an old
# Windows process environment value from being used by any code that consults
# ``os.environ`` directly.
load_dotenv(dotenv_path=DOTENV_PATH, override=True)


class Settings:
    def __init__(self):
        # Read this credential from the project-local .env as the single
        # source of truth, rather than falling back to the process environment.
        self.groq_api_key = dotenv_values(DOTENV_PATH).get("GROQ_API_KEY") or ""

        if not self.groq_api_key.strip():
            raise RuntimeError(
                "GROQ_API_KEY is not configured in .env."
            )
