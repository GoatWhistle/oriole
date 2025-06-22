from fastapi.encoders import jsonable_encoder

from utils import get_current_utc
from utils.schemas import (
    Pagination,
    SuccessListResponse,
    SuccessListResponseWithoutPagination,
    Meta,
)


def pagination_build(total, page, per_page, base_url):
    total_pages = (total + per_page - 1) // per_page
    next_url = (
        f"{base_url}?page={page + 1}&per_page={per_page}"
        if page < total_pages
        else None
    )
    prev_url = f"{base_url}?page={page - 1}&per_page={per_page}" if page > 1 else None
    return Pagination(
        current_page=page,
        per_page=per_page,
        total=total,
        total_pages=total_pages,
        next=next_url,
        previous=prev_url,
    )


def create_list_response(data, page, per_page, base_url):
    if data and page and per_page:
        pagination = pagination_build(
            total=len(data),
            page=page,
            per_page=per_page,
            base_url=base_url,
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
