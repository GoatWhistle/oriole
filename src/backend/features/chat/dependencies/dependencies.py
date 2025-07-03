from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.chat.exeptions import AccountNotFoundError
from features.users.services.auth import get_current_active_auth_user_id
from features import Account


async def get_current_account_id(
    user_id: int = Depends(get_current_active_auth_user_id),
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
) -> int:
    result = await session.execute(select(Account).where(Account.user_id == user_id))
    account = result.scalars().first()
    if not account:
        raise AccountNotFoundError()
    return account.id
