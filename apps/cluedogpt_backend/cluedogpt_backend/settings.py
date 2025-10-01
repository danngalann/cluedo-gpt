"""
Settings module for the cluedogpt_backend app.
Uses pydantic_settings for environment variable management with sensible defaults.
"""

import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(PROJECT_PATH)
ENV_PATH = os.path.join(ROOT_DIR, ".env")


class Settings(BaseSettings):
    # CORS Settings
    cors_allow_origins: list[str] = Field(
        ["*"],
        json_schema_extra={"env_names": ["CORS_ALLOW_ORIGINS"]},
    )
    cors_allow_credentials: bool = Field(
        True,
        json_schema_extra={"env_names": ["CORS_ALLOW_CREDENTIALS"]},
    )
    cors_allow_methods: list[str] = Field(
        ["*"],
        json_schema_extra={"env_names": ["CORS_ALLOW_METHODS"]},
    )
    cors_allow_headers: list[str] = Field(
        ["*"],
        json_schema_extra={"env_names": ["CORS_ALLOW_HEADERS"]},
    )

    # PostgreSQL settings
    postgres_dsn: str = Field(
        "postgres://postgres:postgres@localhost:5432/cluedogpt_backend",
        json_schema_extra={"env_names": ["POSTGRES_DSN"]},
    )

    # API Settings
    api_host: str = Field(
        ...,
        json_schema_extra={"env_names": ["API_HOST"]},
    )
    api_port: int = Field(
        8000,
        json_schema_extra={"env_names": ["API_PORT"]},
    )

    # AI Model Settings
    ai_model_name: str = Field(
        "deepseek/deepseek-chat-v3.1:free",
        json_schema_extra={"env_names": ["AI_MODEL_NAME"]},
    )
    ai_provider_base_url: str = Field(
        "https://openrouter.ai/api/v1",
        json_schema_extra={"env_names": ["AI_PROVIDER_BASE_URL"]},
    )
    ai_model_api_key: str = Field(
        ...,
        json_schema_extra={"env_names": ["AI_MODEL_API_KEY"]},
    )

    # Documentation Settings
    enable_docs: bool = Field(
        True,
        json_schema_extra={"env_names": ["ENABLE_DOCS"]},
    )

    model_config = SettingsConfigDict(env_file=ENV_PATH, case_sensitive=False)


settings = Settings()
