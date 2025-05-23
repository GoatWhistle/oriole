from typing import TYPE_CHECKING
from datetime import datetime
from .base import Base
from .mixins.id_int_pk import IdIntPkMixin
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .group import Group


class GroupInvite(Base, IdIntPkMixin):
    code: Mapped[str] = mapped_column(String(6), unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    is_active: Mapped[bool] = mapped_column(default=True)

    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped["Group"] = relationship(back_populates="invites")
