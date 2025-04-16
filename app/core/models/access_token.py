from sqlalchemy import (
    String,
    Integer,
)

from sqlalchemy.orm import (
    Mapped,
    relationship,
    mapped_column,
)
from datetime import datetime
from pytz import utc

from .base import Base
from .mixins.id_int_pk import IdIntPkMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class AccessToken(Base, IdIntPkMixin):
    token: Mapped[str] = mapped_column(String(length=511), nullable=False)
    created_at: Mapped[int] = mapped_column(
        String(length=15), default=str(datetime.now(utc)), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="tokens")
