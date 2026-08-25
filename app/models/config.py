# ⚙️ Configuration model
# 📖 Sebastian reads runtime settings from environment variables so it can behave
# 🔄 differently in local, staging, or production environments without editing code.
# 💨 Empty line for spacing
import os # 📦 Import os module for environment variables
# 💨 Empty line for spacing
from pydantic import BaseModel # 📦 Import BaseModel from pydantic for validation
# 💨 Empty line for spacing
# 💨 Empty line for spacing
class Settings(BaseModel): # 🏷️ Define Settings class inheriting from BaseModel
    # 🤖 Application name shown in logs and metadata.
    app_name: str = "Sebastian" # 📝 App name string with default value
# 💨 Empty line for spacing
    # 🌍 Environment label, such as development or production.
    environment: str = "development" # 📝 Environment string with default development
# 💨 Empty line for spacing
    # 🪵 Logging level for runtime diagnostics.
    log_level: str = "INFO" # 📝 Log level string with default INFO
# 💨 Empty line for spacing
    # 🔐 Optional API key for external model/provider access.
    model_api_key: str | None = None # 📝 Optional model API key
# 💨 Empty line for spacing
# 💨 Empty line for spacing
def load_settings() -> Settings: # 🎯 Function to load settings
    # 📥 Read environment variables and build a typed settings object.
    return Settings( # 🔄 Return new Settings instance
        app_name=os.getenv("SEBASTIAN_APP_NAME", "Sebastian"), # 📝 Read SEBASTIAN_APP_NAME or default
        environment=os.getenv("SEBASTIAN_ENV", "development"), # 📝 Read SEBASTIAN_ENV or default
        log_level=os.getenv("SEBASTIAN_LOG_LEVEL", "INFO"), # 📝 Read SEBASTIAN_LOG_LEVEL or default
        model_api_key=os.getenv("MODEL_API_KEY"), # 📝 Read MODEL_API_KEY
    ) # ✅ Close Settings instantiation