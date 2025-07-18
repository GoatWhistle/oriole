from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, IdIntPkMixin
from features.modules.schemas import ModuleRead

if TYPE_CHECKING:
    from features.tasks.models import BaseTask
    from features.spaces.models import Space
    from features.accounts.models import Account


class Module(Base, IdIntPkMixin):
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(200))

    creator_id: Mapped[int] = mapped_column(ForeignKey("accounts.user_id"))
    space_id: Mapped[int] = mapped_column(ForeignKey("spaces.id", ondelete="CASCADE"))

    creator: Mapped["Account"] = relationship(back_populates="created_modules")
    space: Mapped["Space"] = relationship(back_populates="modules")

    tasks: Mapped[list["BaseTask"]] = relationship(
        back_populates="module", cascade="all, delete-orphan"
    )
    tasks_count: Mapped[int] = mapped_column(Integer, default=0)

    start_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.timezone("UTC", func.now())
    )
    end_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.timezone("UTC", func.now())
    )
    is_active: Mapped[bool] = mapped_column(default=False)

    def get_validation_schema(self) -> ModuleRead:
        return ModuleRead.model_validate(self)
