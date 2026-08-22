# ⚙️ Configuration model
# Sebastian reads runtime settings from environment variables so it can behave
# differently in local, staging, or production environments without editing code.

import os

from pydantic import BaseModel


class Settings(BaseModel):
    # 🤖 Application name shown in logs and metadata.
    app_name: str = "Sebastian"

    # 🌍 Environment label, such as development or production.
    environment: str = "development"

    # 🪵 Logging level for runtime diagnostics.
    log_level: str = "INFO"

    # 🔐 Optional API key for external model/provider access.
    model_api_key: str | None = None


def load_settings() -> Settings:
    # 📥 Read environment variables and build a typed settings object.
    return Settings(
        app_name=os.getenv("SEBASTIAN_APP_NAME", "Sebastian"),
        environment=os.getenv("SEBASTIAN_ENV", "development"),
        log_level=os.getenv("SEBASTIAN_LOG_LEVEL", "INFO"),
        model_api_key=os.getenv("MODEL_API_KEY"),
    )