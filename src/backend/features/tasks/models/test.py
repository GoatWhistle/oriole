from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import IdIntPkMixin, Base

if TYPE_CHECKING:
    from features.tasks.models import CodeTask


class Test(Base, IdIntPkMixin):
    task_id: Mapped[int] = mapped_column(ForeignKey("code_tasks.id"))
    correct_output: Mapped[str] = mapped_column(nullable=False)
    input_data: Mapped[str] = mapped_column(nullable=True)
    is_public: Mapped[bool] = mapped_column(default=True)

    task: Mapped["CodeTask"] = relationship(back_populates="tests")
