from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = "sqlite+aiosqlite:///./campaign_planner.db"

    # Auth
    jwt_secret: str = "campaign_planner"
    jwt_algorithm: str = "HS256"
    jwt_expiry_hours: int = 24

    # AI
    groq_api_key: str = ""
    groq_model: str = "llama-3.1-8b-instant"
    use_mock_ai: bool = True

    # App
    cors_origins: str = "http://localhost:5173"

    @property
    def async_database_url(self) -> str:
        url = self.database_url
        if url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://") and not url.startswith("postgresql+asyncpg://"):
            return url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return url

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
