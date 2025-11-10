"""Application configuration with Pydantic Settings."""
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Base application settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    app_env: Literal["dev", "prod"] = Field(default="dev", alias="APP_ENV")
    app_secret: str = Field(..., alias="APP_SECRET")
    app_locale_default: str = Field(default="en", alias="APP_LOCALE_DEFAULT")
    app_allowed_locales: str = Field(default="en,ru", alias="APP_ALLOWED_LOCALES")
    
    # Authentication
    app_login_user: str = Field(default="admin", alias="APP_LOGIN_USER")
    app_login_password: str = Field(..., alias="APP_LOGIN_PASSWORD")
    app_session_days: int = Field(default=30, alias="APP_SESSION_DAYS")
    
    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    cache_max_items: int = Field(default=50, alias="CACHE_MAX_ITEMS")
    
    # LLM Providers
    llm_default: str = Field(default="openai:openai-4nano", alias="LLM_DEFAULT")
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    
    # Whisper
    whisper_mode: Literal["local", "openai"] = Field(default="local", alias="WHISPER_MODE")
    whisper_model: str = Field(default="base", alias="WHISPER_MODEL")
    
    @property
    def is_dev(self) -> bool:
        """Check if running in development mode."""
        return self.app_env == "dev"
    
    @property
    def is_prod(self) -> bool:
        """Check if running in production mode."""
        return self.app_env == "prod"
    
    @property
    def allowed_locales_list(self) -> list[str]:
        """Get list of allowed locales."""
        return [loc.strip() for loc in self.app_allowed_locales.split(",")]
    
    @property
    def session_cookie_name(self) -> str:
        """Get session cookie name."""
        return "compresso_session"
    
    @property
    def session_max_age(self) -> int:
        """Get session max age in seconds."""
        return self.app_session_days * 24 * 60 * 60


# Global settings instance
settings = Settings()
