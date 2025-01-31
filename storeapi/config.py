from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None
    DATABASE_URL: Optional[str] = None

    class Config:
        env_file: str = ".env"
        env_prefix: str = ""
        extra = "allow"


class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLL_BACK: bool = False


class DevConfig(GlobalConfig):
    DATABASE_URL: str = "sqlite:///data.db"

    class Config:
        env_prefix: str = "Dev_"


class ProdConfig(GlobalConfig):
    class Config:
        env_prefix: str = "PROD_"


class TestConfig(GlobalConfig):
    DATABASE_URL: Optional[str] = "sqlite:///test.db"  # Type annotation added here
    DB_FORCE_ROLL_BACK: bool = True

    class Config:
        env_prefix: str = "TEST_"


@lru_cache()
def get_config(env_state: str):
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    return configs[env_state]()


config = get_config(BaseConfig().ENV_STATE)
