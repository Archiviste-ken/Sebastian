import logging

from app.core.logging import configure_logging


def test_logging_configuration(caplog):
    configure_logging()

    logger = logging.getLogger("sebastian")

    with caplog.at_level(logging.INFO):
        logger.info("test_event")

    assert "test_event" in caplog.text
    
    
#     configure_logging()
#         ↓
# ⚙️ Tell logging system:
# "Use this format"
#         ↓
# function ends
#         ↓
# logging system REMEMBERS the configuration
#         ↓
# logger.info("test_event")
#         ↓
# 📨 logging system receives the event
#         ↓
# 🎨 applies the saved format
#         ↓
# 2026-08-12 | INFO | sebastian | test_event


# So configure_logging() is like setting your printer settings. 🖨️

# configure_logging()
#       ↓
# "Print using:
#  date | level | name | message"

# Later:

# logger.info("test_event")

# is like:

# "Print this."

# The printer uses the settings you already configured.

# One subtle thing

# In your test:

# assert "test_event" in caplog.text

# you're only checking that the message exists.

# You're not yet checking that your custom format is correct.

# A format-specific test would check that things like INFO and sebastian also appear.

# So the flow is:

# logging.py
#    ↓
# defines configuration
#    ↓
# configure_logging()
#    ↓
# Python logging system stores/uses that configuration
#    ↓
# logger.info(...)
#    ↓
# format gets applied

# That's exactly how the format= line in logging.py affects logs created later.