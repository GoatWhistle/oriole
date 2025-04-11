from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends

from api.api_v1.fastapi_users import (
    current_active_user,
)
from core.config import settings
from core.models import User
from core.schemas.user import UserRead

router = APIRouter(
    prefix=settings.api.v1.messages,
    tags=["Messages"],
)


@router.get("/error")
def view_may_raise_error(
    raise_error: bool = False,
):
    if raise_error:
        # 1 / 0
        UserRead.model_validate(None)
    return {"ok": True}


# TODO: добавить "учетки" учителей учеников кураторов в группах
@router.get("")
def get_messages(
    user: Annotated[User, Depends(current_active_user)],
):
    if user.is_teacher:
        return {"messages": ["Ученик X не сдал работу", "Собрание в 15:00"]}
    else:
        return {"messages": ["ДЗ на завтра", "Тест в пятницу"]}
