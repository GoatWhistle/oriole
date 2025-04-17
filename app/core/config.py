from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from pydantic import PostgresDsn
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class DbConfig(BaseModel):
    db_url: PostgresDsn
    db_echo: bool = False
    db_echo_pool: bool = False
    db_max_overflow: int = 10
    db_pool_size: int = 50

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    users: str = "/users"
    groups: str = "/groups"
    assignments: str = "/assignments"
    tasks: str = "/tasks"
    auth: str = "/auth"
    learn: str = "/learn"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "jwt-public.pem"
    algorithm: str = "RS256"
    lifetime_seconds: int = 3600


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    db: DbConfig
    api: ApiPrefix = ApiPrefix()
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
