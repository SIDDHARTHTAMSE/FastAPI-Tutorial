from functools import lru_cache
from typing import Optional
from pydantic import BaseSetting


class BaseConfig(BaseSetting):
    ENV_STATE: Optional[str] = None

    class Config:
        env_file: str = ".env"


class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] = None
    DB_FORCE_BACK: bool = False


class DevConfig(GlobalConfig):
    class Config:
        env_prefix: str = "Dev_"


class ProdConfig(GlobalConfig):
    class Config:
        env_prefix: str = "PROD_"


class TestConfig(GlobalConfig):
    DATABASE_URL = "sqlite:///test.db"
    DB_FORCE_BACK = True

    class Config:
        env_prefix: str = "TEST_"


@lru_cache()
def get_config(env_state: str):
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    return configs[env_state]()


config = get_config(BaseConfig().ENV_STATE)
