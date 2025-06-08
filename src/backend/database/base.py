from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

from core.config import settings
from utils.case_converter import pluralize_snake_case


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    @declared_attr
    def __tablename__(self):
        return f"{pluralize_snake_case(self.__name__)}"
