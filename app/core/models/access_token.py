from sqlalchemy import String, ForeignKey, TIMESTAMP

from sqlalchemy.orm import (
    Mapped,
    relationship,
    mapped_column,
)
from datetime import datetime
from pytz import utc

from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class AccessToken(Base):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )
    user: Mapped["User"] = relationship(back_populates="access_token")

    token: Mapped[str] = mapped_column(String(length=511), nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP, default=datetime.now(utc).timestamp(), nullable=False
    )
