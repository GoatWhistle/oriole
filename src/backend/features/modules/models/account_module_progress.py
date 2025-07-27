from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base, IdIntPkMixin

if TYPE_CHECKING:
    from features.accounts.models import Account
    from features.modules.models import Module


class AccountModuleProgress(Base, IdIntPkMixin):
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id"))

    user_completed_tasks_count: Mapped[int] = mapped_column(Integer, default=0)

    account: Mapped["Account"] = relationship(back_populates="module_progresses")
    module: Mapped["Module"] = relationship(back_populates="account_progresses")
