from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="SENTIMENT_",
        env_file=(".env",),
        extra="ignore",
    )

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: str = Field(
        default="*",
        description="Comma-separated list or * for all origins (dev only).",
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def strip_origins(cls, v: str) -> str:
        if v is None:
            return "*"
        return v.strip() if isinstance(v, str) else v

    def origin_list(self) -> list[str]:
        if self.cors_origins == "*":
            return ["*"]
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


def get_settings() -> Settings:
    return Settings()
