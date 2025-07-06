from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, IdIntPkMixin

if TYPE_CHECKING:
    from features.spaces.models import Space


class GroupInvite(Base, IdIntPkMixin):
    space_id: Mapped[int] = mapped_column(ForeignKey("spaces.id", ondelete="CASCADE"))
    space: Mapped["Space"] = relationship(back_populates="invites")

    code: Mapped[str] = mapped_column(String(8), unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.timezone("UTC", func.now())
    )
    is_active: Mapped[bool] = mapped_column(default=True)
