from typing import Any

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from utils import get_current_utc
from utils.schemas import (
    Pagination,
    SuccessListResponse,
    SuccessListResponseWithoutPagination,
    Meta,
    SuccessResponse,
)


def pagination_build(
    total: int,
    page: int,
    per_page: int,
    base_url: str,
    include: list[str] | None = None,
) -> Pagination:
    inc = "".join([f"include={i}&" for i in include])[:-1] if include else ""
    total_pages = (total + per_page - 1) // per_page
    base_url = base_url + "?" if base_url[-1] == "/" else base_url + "&"
    next_url = (
        f"{base_url}page={page + 1}&per_page={per_page}&{inc}"
        if page < total_pages and inc
        else (
            f"{base_url}page={page + 1}&per_page={per_page}"
            if page < total_pages
            else None
        )
    )
    prev_url = (
        f"{base_url}page={page - 1}&per_page={per_page}&{inc}"
        if page < total_pages and inc
        else (
            f"{base_url}page={page - 1}&per_page={per_page}"
            if page < total_pages
            else None
        )
    )
    return Pagination(
        current_page=page,
        per_page=per_page,
        total=total,
        total_pages=total_pages,
        next=next_url,
        previous=prev_url,
    )


def create_list_response(
    data: list[Any],
    page: int | None,
    per_page: int | None,
    base_url: str,
    include: list[str] | None = None,
) -> dict:
    if data and page and per_page:
        pagination = pagination_build(
            total=len(data),
            page=page,
            per_page=per_page,
            base_url=base_url,
            include=include,
        )
        offset = (page - 1) * per_page
        response_content = jsonable_encoder(
            SuccessListResponse(
                data=data[offset : offset + per_page],
                meta=Meta(version="v1", timestamp=str(get_current_utc())),
                pagination=pagination,
            )
        )
    else:
        response_content = jsonable_encoder(
            SuccessListResponseWithoutPagination(
                data=data, meta=Meta(version="v1", timestamp=str(get_current_utc()))
            )
        )
    return response_content


def create_json_response(
    data: list | Any,
    page: int | None = None,
    per_page: int | None = None,
    base_url: str | None = None,
    include: list[str] | None = None,
):
    if isinstance(data, list):
        response_content = create_list_response(
            data=data,
            page=page,
            per_page=per_page,
            base_url=base_url,
            include=include,
        )
    else:
        response_content = jsonable_encoder(
            SuccessResponse(
                data=data, meta=Meta(version="v1", timestamp=str(get_current_utc()))
            )
        )
    return JSONResponse(content=response_content, status_code=201)


"""
Response должен содержать проработанный Header, включающий
Помимо обычных:
- content-length: 1060
- content-type: application/json
- date: Sat,21 Jun 2025 12:15:24 GMT
- server: uvicorn (или кастомный)

Ещё и:
- X-Request-ID: UUID
- X-RateLimit-Limit: 100 (Ели у ендпоинта есть лимиты по срабатыванию)
- X-RateLimit-Remaining: 97 (Сколько осталось срабатываний)
- X-RateLimit-Reset: 2025-06-21T12:30:30Z (Когда обновится)
- Cache-Control: no-cache (Кеш)

Для Post/Patch/Put:
- Location: /api/v1/queue/jobs/abc123 (URI созданного объекта)
"""
