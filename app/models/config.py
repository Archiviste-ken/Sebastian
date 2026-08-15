import os

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Sebastian"
    environment: str = "development"
    log_level: str = "INFO"

    model_api_key: str | None = None


def load_settings() -> Settings:
    return Settings(
        app_name=os.getenv("SEBASTIAN_APP_NAME", "Sebastian"),
        environment=os.getenv("SEBASTIAN_ENV", "development"),
        log_level=os.getenv("SEBASTIAN_LOG_LEVEL", "INFO"),
        model_api_key=os.getenv("MODEL_API_KEY"),
    )