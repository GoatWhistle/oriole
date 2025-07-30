from abc import abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, IdIntPkMixin
from features.solutions.schemas import SolutionFeedbackRead

if TYPE_CHECKING:
    from features.accounts.models import Account
    from features.solutions.models import BaseSolution


class SolutionFeedback(Base, IdIntPkMixin):
    solution_id: Mapped[int] = mapped_column(ForeignKey("solutions.id"))
    creator_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))

    content: Mapped[str] = mapped_column(String(1000))
    is_anonymous: Mapped[bool] = mapped_column(Boolean, default=False)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.timezone("UTC", func.now())
    )
    is_updated: Mapped[bool] = mapped_column(Boolean, default=False)

    @abstractmethod
    def get_validation_schema(self) -> SolutionFeedbackRead:
        return SolutionFeedbackRead.model_validate(self)

    solution: Mapped["BaseSolution"] = relationship(back_populates="feedbacks")
    creator: Mapped["Account"] = relationship(back_populates="created_feedbacks")
