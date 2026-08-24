import importlib

import app.config as config


def test_settings_uses_project_root_dotenv_over_process_environment(monkeypatch):
    """Safe diagnostic: the credential is present and does not come from a stale environment value."""
    assert config.DOTENV_PATH.is_file()

    monkeypatch.setenv("GROQ_API_KEY", "stale-process-value")
    reloaded_config = importlib.reload(config)
    settings = reloaded_config.Settings()

    assert settings.groq_api_key
    assert settings.groq_api_key != "stale-process-value"
