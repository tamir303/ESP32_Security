from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    debug: bool = True
    profile: str = "dev"
    api_key_secret: str = "secret"
    database_url: str = "sqlite:///database.db"
    kafka_url: str = "localhost"
    kafka_port: int = 9092

    class Config:
        env_file = ".env"


@lru_cache()
def get_config():
    return Settings()
