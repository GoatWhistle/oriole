from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import IdIntPkMixin
from database.base import Base
from shared.enums import SpaceTypeEnum

if TYPE_CHECKING:
    from features.modules.models import Module
    from features.groups.models import Account, GroupInvite


class Space(Base, IdIntPkMixin):
    space_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    __mapper_args__ = {
        "polymorphic_identity": SpaceTypeEnum.BASE,
        "polymorphic_on": space_type,
        "with_polymorphic": "*",
    }

    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(200))

    accounts: Mapped[list["Account"]] = relationship(back_populates="group")
    modules: Mapped[list["Module"]] = relationship(back_populates="group")
    invites: Mapped[list["GroupInvite"]] = relationship(back_populates="group")
