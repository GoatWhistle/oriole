from core.config import settings

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)


class DbHelper:
    def __init__(
        self,
        db_url: str,
        db_echo: bool = settings.db.db_echo,
        db_echo_pool: bool = settings.db.db_echo_pool,
        db_max_overflow: int = settings.db.db_max_overflow,
        db_pool_size: int = settings.db.db_pool_size,
    ):
        self.engine: AsyncEngine = create_async_engine(
            url=db_url,
            echo=db_echo,
            echo_pool=db_echo_pool,
            max_overflow=db_max_overflow,
            pool_size=db_pool_size,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self):
        await self.engine.dispose()

    async def dependency_session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


db_helper = DbHelper(
    db_url=str(settings.db.db_url),
)
