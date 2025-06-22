from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.users.schemas.token import SuccessVerify
from features.users.services import email_access as service
from utils import get_current_utc
from utils.schemas import SuccessResponse, Meta

router = APIRouter()


@router.get("/{token}", response_model=SuccessResponse[SuccessVerify])
async def verify(
    token: str,
    session: Annotated[AsyncSession, Depends(db_helper.dependency_session_getter)],
):
    data = await service.verify(token=token, session=session)
    response_content = jsonable_encoder(
        SuccessResponse[SuccessVerify](
            data=data, meta=Meta(version="v1", timestamp=str(get_current_utc()))
        )
    )
    return JSONResponse(content=response_content, status_code=200)


@router.get(
    "/reset_password_redirect/{token}", response_model=SuccessResponse[SuccessVerify]
)
async def reset_password_redirect(
    token: str,
    new_password: str,
    session: Annotated[AsyncSession, Depends(db_helper.dependency_session_getter)],
):
    data = await service.reset_password_redirect(
        token=token,
        new_password=new_password,
        session=session,
    )
    response_content = jsonable_encoder(
        SuccessResponse[SuccessVerify](
            data=data, meta=Meta(version="v1", timestamp=str(get_current_utc()))
        )
    )
    return JSONResponse(content=response_content, status_code=200)


@router.get(
    "/forgot_password_redirect/{token}", response_model=SuccessResponse[SuccessVerify]
)
async def forgot_password_redirect(
    token: str,
    new_password: str,
    session: Annotated[AsyncSession, Depends(db_helper.dependency_session_getter)],
):
    data = await service.forgot_password_redirect(
        token=token,
        new_password=new_password,
        session=session,
    )
    response_content = jsonable_encoder(
        SuccessResponse[SuccessVerify](
            data=data, meta=Meta(version="v1", timestamp=str(get_current_utc()))
        )
    )
    return JSONResponse(content=response_content, status_code=200)
