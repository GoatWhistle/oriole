from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class Pagination(BaseModel):
    current_page: int
    per_page: int
    total: int
    total_pages: int
    next: str | None
    previous: str | None


class Meta(BaseModel):
    version: str
    timestamp: str


class SuccessResponse(BaseModel, Generic[T]):
    data: T
    meta: Meta


class SuccessListResponse(BaseModel, Generic[T]):
    data: list[T]
    meta: Meta
    pagination: Pagination


class SuccessListResponseWithoutPagination(BaseModel, Generic[T]):
    data: list[T]
    meta: Meta
