"""
Configuration settings for FunLearn
Powered by DigitalOcean Gradient AI
"""

import os
import secrets
import logging
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional

logger = logging.getLogger(__name__)


def get_secret_key() -> str:
    """
    Get SECRET_KEY from environment or generate a secure one for development.
    In production, SECRET_KEY must be set via environment variable.
    """
    secret_key = os.getenv("SECRET_KEY")
    app_env = os.getenv("APP_ENV", "development")

    if secret_key and secret_key != "your_secret_key_change_in_production":
        return secret_key

    if app_env == "production":
        raise ValueError(
            "SECRET_KEY environment variable must be set in production! "
            "Generate one with: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
        )

    # Generate a random key for development (will change on restart)
    generated_key = secrets.token_urlsafe(32)
    logger.warning(
        "SECRET_KEY not set - using generated key for development. "
        "Set SECRET_KEY environment variable for persistent sessions."
    )
    return generated_key


class Settings(BaseSettings):
    """Application settings with validation"""

    # App Settings
    APP_NAME: str = "FunLearn"
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    SECRET_KEY: str = get_secret_key()

    # Server
    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_WINDOW_SECONDS: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
    LOGIN_RATE_LIMIT_REQUESTS: int = int(os.getenv("LOGIN_RATE_LIMIT_REQUESTS", "5"))
    LOGIN_RATE_LIMIT_WINDOW_SECONDS: int = int(os.getenv("LOGIN_RATE_LIMIT_WINDOW_SECONDS", "60"))

    # Provider Selection
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "digitalocean")
    IMAGE_PROVIDER: str = os.getenv("IMAGE_PROVIDER", "none")
    VOICE_TTS_PROVIDER: str = os.getenv("VOICE_TTS_PROVIDER", "none")
    VOICE_STT_PROVIDER: str = os.getenv("VOICE_STT_PROVIDER", "none")

    # DigitalOcean Gradient AI
    GRADIENT_API_KEY: str = os.getenv("GRADIENT_API_KEY", "")
    GRADIENT_BASE_URL: str = os.getenv("GRADIENT_BASE_URL", "https://inference.do-ai.run/v1")
    GRADIENT_MODEL: str = os.getenv("GRADIENT_MODEL", "meta-llama/Meta-Llama-3.3-70B-Instruct")
    RITTY_AGENT_UUID: str = os.getenv("RITTY_AGENT_UUID", "")

    # Legacy API Keys (kept for compatibility)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3-pro-preview")
    GEMINI_IMAGE_MODEL: str = os.getenv("GEMINI_IMAGE_MODEL", "gemini-3-pro-image-preview")

    # Legacy GCP
    GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "")
    GCP_STT_API_KEY: str = os.getenv("GCP_STT_API_KEY", "")
    GCP_TTS_API_KEY: str = os.getenv("GCP_TTS_API_KEY", "")

    # Legacy FIBO
    FIBO_API_KEY: str = os.getenv("FIBO_API_KEY", "")
    FIBO_API_ENDPOINT: str = os.getenv("FIBO_API_ENDPOINT", "https://api.fibo.ai/v1")

    # Application API Key for client authentication
    APP_API_KEY: str = os.getenv("APP_API_KEY", "kd_dreaming007")

    # Fallback API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    STABILITY_API_KEY: str = os.getenv("STABILITY_API_KEY", "")

    # File Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    CSV_DIR: Path = DATA_DIR / "csv"
    MEDIA_DIR: Path = DATA_DIR / "media"

    # JWT Settings
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

    # File Upload Settings
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "10"))
    ALLOWED_IMAGE_TYPES: list = ["image/jpeg", "image/png", "image/gif", "image/webp"]

    # Pagination Settings
    MAX_PAGE_SIZE: int = int(os.getenv("MAX_PAGE_SIZE", "100"))
    DEFAULT_PAGE_SIZE: int = int(os.getenv("DEFAULT_PAGE_SIZE", "20"))

    # API Retry Settings
    API_RETRY_ATTEMPTS: int = int(os.getenv("API_RETRY_ATTEMPTS", "3"))
    API_RETRY_DELAY_SECONDS: float = float(os.getenv("API_RETRY_DELAY_SECONDS", "1.0"))

    # Video Generation Settings
    VIDEO_GENERATION_TIMEOUT_SECONDS: int = int(os.getenv("VIDEO_GENERATION_TIMEOUT_SECONDS", "300"))
    FFMPEG_TIMEOUT_SECONDS: int = int(os.getenv("FFMPEG_TIMEOUT_SECONDS", "120"))

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields from .env file


settings = Settings()

# Ensure directories exist
settings.CSV_DIR.mkdir(parents=True, exist_ok=True)
settings.MEDIA_DIR.mkdir(parents=True, exist_ok=True)
(settings.MEDIA_DIR / "avatars").mkdir(exist_ok=True)
(settings.MEDIA_DIR / "characters").mkdir(exist_ok=True)
(settings.MEDIA_DIR / "generated_images").mkdir(exist_ok=True)
(settings.MEDIA_DIR / "generated_videos").mkdir(exist_ok=True)
(settings.MEDIA_DIR / "audio").mkdir(exist_ok=True)
(settings.MEDIA_DIR / "uploads").mkdir(exist_ok=True)
(settings.MEDIA_DIR / "temp").mkdir(exist_ok=True)
