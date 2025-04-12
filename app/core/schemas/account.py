from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel
from sqlalchemy.sql.annotation import Annotated

if TYPE_CHECKING:
    from .group import Group
    from .task import TaskRead


class Account(BaseModel):
    user_id: Annotated[int]

    role: Annotated[int]

    group_id: Annotated[int]

    done_tasks: Annotated[list[Optional[int]]]
