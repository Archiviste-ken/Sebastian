# 🪵 Logging configuration
# This file configures Python's logging system for the project.
# It gives each log entry a consistent, readable format for debugging execution flow.

import logging

from app.models.config import Settings


def configure_logging(settings: Settings) -> None:
    # 🔧 Set the log level and format used by the global logger.
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    
