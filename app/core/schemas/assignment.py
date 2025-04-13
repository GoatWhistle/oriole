from pydantic import BaseModel, Field, ConfigDict

from typing import Annotated, Optional, Sequence

from utils.number_optimizer import get_number_one_bit_less as num_opt


class AssignmentBase(BaseModel):
    title: Annotated[str, Field(max_length=num_opt(100))]
    description: Annotated[str, Field(max_length=num_opt(200))]

    is_contest: bool

    admin_id: int
    group_id: int

    tasks: Sequence[int]


class AssignmentRead(AssignmentBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class AssignmentCreate(AssignmentBase):
    pass


class AssignmentUpdate(AssignmentCreate):
    pass


class AssignmentUpdatePartial(AssignmentCreate):
    title: Annotated[Optional[str], Field(max_length=num_opt(100))] = None
    description: Annotated[Optional[str], Field(max_length=num_opt(200))] = None

    is_contest: bool = None

    admin_id: Optional[int] = None
    group_id: Optional[int] = None

    tasks: Optional[Sequence[int]] = None
