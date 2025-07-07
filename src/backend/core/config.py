from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

env_files = (".env.app_config",)

BASE_DIR = Path(__file__).resolve().parent.parent

for file in env_files:
    load_dotenv(BASE_DIR / file)


class RunConfig(BaseModel):
    host: str
    port: int


class GunicornConfig(BaseModel):
    workers: int = 5
    timeout: int = 900
    worker_class: str = "uvicorn.workers.UvicornWorker"


class DbConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 10
    pool_size: int = 50

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    users: str = "/users"
    groups: str = "/groups"
    modules: str = "/modules"
    tasks: str = "/tasks"
    auth: str = "/auth"
    learn: str = "/learn"
    email_verify: str = "/verify"
    reset_password: str = "/reset_password_redirect"
    forgot_password: str = "/forgot_password_redirect"
    websocket: str = "/websocket"


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_lifetime_seconds: int = 1800
    refresh_token_lifetime_seconds: int = 2_592_000
    email_token_lifetime_seconds: int = 7200
    password_token_lifetime_seconds: int = 600


class SMTPEmail(BaseModel):
    server: str
    port: int
    user: EmailStr
    password: str


class Sentry(BaseModel):
    dsn: str


class Redis(BaseModel):
    port: int
    url: str
    password: str = None
    use_ssl: bool = False
    socket_timeout: int = 2

    limiter_enabled: bool = True
    limiter_strategy: Literal["fixed-window", "moving-window"] = "moving-window"
    limiter_default: str = "10/minute"

    @property
    def full_url(self):
        scheme = "rediss" if self.use_ssl else "redis"
        return f"{scheme}://{self.url}:{self.port}/0"

    @property
    def safe_storage_options(self) -> dict:
        return {
            "socket_timeout": self.socket_timeout,
            "ssl": self.use_ssl,
            "ssl_cert_reqs": None,
            "health_check_interval": 30,
            "retry_on_timeout": True,
            "socket_keepalive": True,
        }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_files,
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig
    smtp_email: SMTPEmail
    db: DbConfig
    redis: Redis
    sentry: Sentry
    gunicorn_run: GunicornConfig = GunicornConfig()
    api: ApiPrefix = ApiPrefix()
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
