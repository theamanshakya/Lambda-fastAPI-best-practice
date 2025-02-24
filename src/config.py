from pydantic_settings import BaseSettings
from functools import lru_cache
from enum import Enum

class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class Settings(BaseSettings):
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    SNOWFLAKE_ACCOUNT: str
    SNOWFLAKE_USER: str
    SNOWFLAKE_PASSWORD: str
    SNOWFLAKE_DATABASE: str
    SNOWFLAKE_SCHEMA: str
    SNOWFLAKE_WAREHOUSE: str
    
    # Connection Pool Settings
    DB_POOL_MIN_CONNECTIONS: int = 1
    DB_POOL_MAX_CONNECTIONS: int = 10
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings() 