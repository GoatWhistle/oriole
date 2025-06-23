import pytest
from fastapi.responses import JSONResponse

from src.backend.utils.case_converter import (
    camel_case_to_snake_case,
    pluralize_snake_case,
)
from src.backend.utils.response_func import pagination_build, create_list_response
from src.backend.utils.schemas import Pagination, Meta


def test_pagination_build():
    total = 10
    page = 2
    per_page = 2
    base_url = "http://127.0.0.1:8000/api/groups/"
    result = pagination_build(
        total=total, page=page, per_page=per_page, base_url=base_url
    )
    assert hasattr(result, "current_page")
    assert result.next is not None
    assert result.previous == base_url + f"?page={page - 1}&per_page={per_page}"
    assert (
        result.model_dump()
        == Pagination(
            total=total,
            current_page=page,
            per_page=per_page,
            total_pages=5,
            next=(base_url + f"?page={page + 1}&per_page={per_page}"),
            previous=(base_url + f"?page={page - 1}&per_page={per_page}"),
        ).model_dump()
    )


def test_create_list_response():
    data = [Meta(version="v1", timestamp="ok")]
    page = None
    per_page = 4
    base_url = "http://127.0.0.1:8000/api/groups/"
    result = create_list_response(
        data=data, page=page, per_page=per_page, base_url=base_url
    )
    assert result["data"] is not None
    assert result["meta"] is not None
    assert "pagination" not in result
    try:
        JSONResponse(content=result)
    except Exception as e:
        pytest.fail(e)


def test_camel_case_to_snake_case():
    assert camel_case_to_snake_case("JSONResponse") == "json_response"
    assert camel_case_to_snake_case("parseXMLFile") == "parse_xml_file"
    assert camel_case_to_snake_case("already_snake") == "already_snake"


def test_pluralize_snake_case():
    assert pluralize_snake_case("UserProfile") == "user_profiles"
    assert pluralize_snake_case("DataPerson") == "data_people"
