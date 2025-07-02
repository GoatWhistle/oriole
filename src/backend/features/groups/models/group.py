from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from features.spaces.models.space import Space
from shared.enums import SpaceTypeEnum

if TYPE_CHECKING:
    from features import Chat

class Group(Space):
    __mapper_args__ = {"polymorphic_identity": SpaceTypeEnum.GROUP.value}
    id: Mapped[int] = mapped_column(ForeignKey("spaces.id"), primary_key=True)


    chat: Mapped["Chat"] = relationship(
        "Chat", back_populates="group", uselist=False, cascade="all, delete-orphan"
    )
