from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pg_user: str = 'postgres'
    pg_password: str = 'admin'
    pg_database: str = 'rinha'
    pg_host: str = 'localhost'
    pg_port: int = 5432
    pg_max_size: int = 150
    pg_max_queries: int = 150


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
