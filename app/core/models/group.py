from typing import TYPE_CHECKING, Optional

from .base import Base
from .mixins.id_int_pk import IdIntPkMixin

from .user_group_association import user_group_association_table

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

if TYPE_CHECKING:
    from .user_profile import UserProfile
    from .assignment import Assignment


class Group(Base, IdIntPkMixin):
    title: Mapped[str] = mapped_column(String(64))
    description: Mapped[str] = mapped_column(String(200))

    admin_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.user_id"))
    admin: Mapped["UserProfile"] = relationship(back_populates="admin_groups")

    users: Mapped[list["UserProfile"]] = relationship(
        secondary=user_group_association_table,
        back_populates="groups",
    )

    assignments: Mapped[list[Optional["Assignment"]]] = relationship(
        back_populates="group"
    )
    # tasks: Mapped[list[Optional["Task"]]] = relationship(back_populates="group")
