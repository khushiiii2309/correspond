from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "development"
    database_url: str = "postgresql+psycopg://correspond:correspond@localhost:5433/correspond"
    cors_origins: str = "http://localhost:5173"

    openai_api_key: str | None = None

    google_client_id: str | None = None
    google_client_secret: str | None = None
    google_redirect_uri: str | None = None

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
