from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from features.users.validators.password import validate_password_not_equal
from features.users.validators.timing import validate_token_expiration
from utils.JWT import decode_jwt
from features.users.crud.user import get_user_by_id, update_user_password


async def change_password_with_token(
    token: str,
    new_password: str,
    session: AsyncSession,
) -> dict:
    try:
        payload = decode_jwt(token)
        validate_token_expiration(payload)

        user_id = int(payload["sub"])
        user = await get_user_by_id(session=session, user_id=user_id)

        validate_password_not_equal(
            plain_password=new_password,
            hashed_password=str(user.hashed_password),
        )

        await update_user_password(
            session=session,
            user=user,
            new_password=new_password,
        )

        return {"status": "success", "message": "You changed password"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
