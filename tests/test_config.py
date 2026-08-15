from app.models.config import load_settings


def test_default_settings():
    settings = load_settings()

    assert settings.app_name == "Sebastian"
    assert settings.environment == "development"
    assert settings.log_level == "INFO"