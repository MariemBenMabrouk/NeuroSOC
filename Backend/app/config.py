from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(alias="APP_NAME")
    app_version: str = Field(alias="APP_VERSION")

    host: str = Field(alias="HOST")
    port: int = Field(alias="PORT")

    debug: bool = Field(alias="DEBUG")

    nmap_binary: str = Field(alias="NMAP_BINARY")
    default_scan_arguments: str = Field(alias="DEFAULT_SCAN_ARGUMENTS")

    ollama_url: str = Field(alias="OLLAMA_URL")
    ollama_model: str = Field(alias="OLLAMA_MODEL")

    database_url: str = Field(alias="DATABASE_URL")

    log_level: str = Field(alias="LOG_LEVEL")

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()