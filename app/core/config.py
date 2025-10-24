import os
import secrets
from typing import Annotated, Any, Literal

from pydantic import AnyUrl, BeforeValidator, computed_field, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    FRONTEND_HOST: str = "http://localhost:5173"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = (
        []
    )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    JWT_ALGORITHM: str = "HS256"

    DB_URL: str = Field(
        "postgresql://postgres:navat@localhost/yourdb",
        env="DATABASE_URL",
    )
    # Microsoft Graph / Azure AD configuration (optional)
    AZURE_TENANT_ID: str | None = None
    AZURE_CLIENT_ID: str | None = None
    AZURE_CLIENT_SECRET: str | None = None
    # Optional mailbox (userPrincipalName or id) to query. If not set, callers
    # should provide the mailbox; otherwise the app client id is sometimes used
    # as a fallback but it's recommended to set an actual mailbox/email.
    AZURE_MAILBOX: str | None = None


settings = Settings()
