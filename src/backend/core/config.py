from pathlib import Path
from typing import Literal, Protocol

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

    def get_storage_uri(self):
        scheme = "rediss" if self.use_ssl else "redis"
        credentials = f":{self.password}@" if self.password else ""
        return f"{scheme}://{credentials}{self.url}:{self.port}/0"

    def get_storage_options(self) -> dict:
        return {
            "socket_timeout": self.socket_timeout,
            "ssl": self.use_ssl,
            "ssl_cert_reqs": None,
            "health_check_interval": 30,
            "retry_on_timeout": True,
            "socket_keepalive": True,
        }


class MemcachedConfig(BaseModel):
    url: str
    port: int = 11211
    timeout: int = 2

    def get_storage_uri(self) -> str:
        return f"memcached://{self.url}:{self.port}"

    def get_storage_options(self) -> dict:
        return {"timeout": self.timeout}


class RateLimiterStorageConfig(Protocol):
    def get_storage_uri(self) -> str: ...
    def get_storage_options(self) -> dict: ...


class RateLimiterSettings(BaseModel):
    enabled: bool = True
    storage_type: Literal["redis", "memcached"] = "redis"
    strategy: Literal["fixed-window", "moving-window"] = "moving-window"
    default: str = "10/minute"
    redis: Redis | None = None
    memcached: MemcachedConfig | None = None

    def get_storage_config(self) -> RateLimiterStorageConfig:
        if self.storage_type == "redis" and self.redis:
            return self.redis
        elif self.storage_type == "memcached" and self.memcached:
            return self.memcached
        raise ValueError("Storage configuration not found")


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
    memcached: MemcachedConfig = MemcachedConfig(url="localhost")
    sentry: Sentry
    gunicorn_run: GunicornConfig = GunicornConfig()
    api: ApiPrefix = ApiPrefix()
    auth_jwt: AuthJWT = AuthJWT()

    @property
    def rate_limiter(self) -> RateLimiterSettings:
        return RateLimiterSettings(
            enabled=self.redis.limiter_enabled,
            storage_type="redis",
            strategy=self.redis.limiter_strategy,
            default=self.redis.limiter_default,
            redis=self.redis,
            memcached=self.memcached,
        )


settings = Settings()
