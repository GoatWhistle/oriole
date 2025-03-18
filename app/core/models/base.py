from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    declared_attr,
)
from sqlalchemy import MetaData

from utils import camel_case_to_snake_case

from core.config import settings


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr
    def __tablename__(self):
        return f"{camel_case_to_snake_case(self.__name__)}s"
