from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from features.spaces.models.space import Space
from shared.enums import SpaceTypeEnum


class Course(Space):
    __mapper_args__ = {"polymorphic_identity": SpaceTypeEnum.COURSE.value}
    id: Mapped[int] = mapped_column(ForeignKey("spaces.id"), primary_key=True)
