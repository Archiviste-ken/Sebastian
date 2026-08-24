import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    def __init__(self):
        self.groq_api_key = os.getenv(
            "GROQ_API_KEY",
            "",
        )

        if not self.groq_api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not configured."
            )