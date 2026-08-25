# 🪵 Logging configuration
# 📖 This file configures Python's logging system for the project.
# 🔄 It gives each log entry a consistent, readable format for debugging execution flow.
# 💨 Empty line for spacing
import logging # 📦 Import logging module for diagnostics
# 💨 Empty line for spacing
from app.models.config import Settings # 📦 Import Settings model for config
# 💨 Empty line for spacing
# 💨 Empty line for spacing
def configure_logging(settings: Settings) -> None: # 🎯 Function to configure logging with Settings
    # 🔧 Set the log level and format used by the global logger.
    logging.basicConfig( # 🔄 Setup basic config for logging
        level=getattr(logging, settings.log_level.upper(), logging.INFO), # 🔧 Get log level from settings or fallback to INFO
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s", # 📝 Set log message format
    ) # ✅ Close basicConfig call
# 💨 Empty line for spacing
# 💨 Empty line for spacing
