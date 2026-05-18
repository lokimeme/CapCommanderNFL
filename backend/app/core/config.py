from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    Enterprise configuration management for CapCommander.
    Handles environment variables with validation.
    """
    PROJECT_NAME: str = "CapCommander NFL Enterprise"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "SUPER_SECRET_FRONT_OFFICE_KEY"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    
    # DATABASE
    POSTGRES_SERVER: Optional[str] = "localhost"
    POSTGRES_USER: Optional[str] = "postgres"
    POSTGRES_PASSWORD: Optional[str] = "password"
    POSTGRES_DB: Optional[str] = "capcommander"
    DATABASE_URL: Optional[str] = "sqlite:///./capcommander_v2.db"

    # NFL DATA SETTINGS
    DEFAULT_YEARS: list = [2023, 2024]
    CACHE_EXPIRY: int = 3600 # 1 hour
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
