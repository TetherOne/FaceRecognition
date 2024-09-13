from pydantic import BaseModel, PostgresDsn
from pydantic_settings import SettingsConfigDict, BaseSettings


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 40
    max_overflow: int = 8


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("envs/app.env",),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="TEVIAN__",
        arbitrary_types_allowed=True,
    )
    db: DatabaseConfig


settings = Settings()
