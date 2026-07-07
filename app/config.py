from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # APP
    app_name: str = "DcHubs User API"
    app_port: int = 8080
    app_env: str = "dev"
    app_debug: bool = False
    # JWT
    jwt_secret_key: str = "12345789@98765431"
    refresh_jwt_secret_key: str = "98765431@12345789"
    jwt_algorithm: str = "HS256"
    jwt_iss: str = "dchubs"
    jwt_audience: str = "dchubs-api"

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings() -> Settings:
    load_dotenv()
    return Settings()
