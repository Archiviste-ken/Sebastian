import logging

from app.core.logging import configure_logging


def test_logging_configuration(caplog):
    configure_logging()

    logger = logging.getLogger("sebastian")

    with caplog.at_level(logging.INFO):
        logger.info("test_event")

    assert "test_event" in caplog.text