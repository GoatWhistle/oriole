from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, BigInteger
from sqlalchemy.orm import Mapped, relationship, mapped_column

from database import IdIntPkMixin
from database.base import Base
from utils import get_number_one_bit_less as get_num_opt

if TYPE_CHECKING:
    from features import UserProfile


class User(Base, IdIntPkMixin):
    email: Mapped[str] = mapped_column(
        String(length=127), unique=True, index=True, nullable=True
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=get_num_opt(1000)), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        index=True,
        nullable=True,
        default=0,
    )

    profile: Mapped["UserProfile"] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
