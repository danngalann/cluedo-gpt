"""
Settings module for the cluedogpt_backend app.
Uses pydantic_settings for environment variable management with sensible defaults.
"""

import os
from functools import lru_cache

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

    # Logging Settings
    log_level: str = Field(
        "INFO",
        json_schema_extra={"env_names": ["LOG_LEVEL"]},
    )
    console_log_level: str = Field(
        "INFO",
        json_schema_extra={"env_names": ["CONSOLE_LOG_LEVEL"]},
    )
    file_log_level: str = Field(
        "INFO",
        json_schema_extra={"env_names": ["FILE_LOG_LEVEL"]},
    )

    # JWT Settings
    jwt_secret_key: str = Field(
        ...,
        json_schema_extra={"env_names": ["JWT_SECRET_KEY"]},
    )
    jwt_algorithm: str = Field(
        "HS256",
        json_schema_extra={"env_names": ["JWT_ALGORITHM"]},
    )
    jwt_access_token_expire_minutes: int = Field(
        15,
        json_schema_extra={"env_names": ["JWT_ACCESS_TOKEN_EXPIRE_MINUTES"]},
    )
    jwt_refresh_token_expire_days: int = Field(
        30,
        json_schema_extra={"env_names": ["JWT_REFRESH_TOKEN_EXPIRE_DAYS"]},
    )

    model_config = SettingsConfigDict(env_file=ENV_PATH, case_sensitive=False)


@lru_cache
def settings() -> Settings:
    return Settings()
