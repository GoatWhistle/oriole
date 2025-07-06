from fastapi import Response, Depends, APIRouter

from database import db_helper

from sqlalchemy.ext.asyncio import AsyncSession
from features.users.schemas.token import TokenResponseForOAuth2
from features.users.services import telegram_auth as service


router = APIRouter()


@router.post("/telegram", response_model=TokenResponseForOAuth2)
async def login_via_telegram(
    raw_data: dict,
    response: Response,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
):
    return await service.login_via_telegram(
        raw_data=raw_data,
        response=response,
        session=session,
    )
