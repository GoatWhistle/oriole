from fastapi import (
    Response,
    Request,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession
from features.users.validators.email import (
    validate_user_email_match,
    validate_email_change_token,
)
from features.users.validators.existence import validate_token_presence


async def change_email_with_token(
    token: str,
    session: AsyncSession,
    request: Request,
    response: Response | None = None,
) -> dict:
    try:
        user_id, old_email, new_email = await validate_email_change_token(
            token=token,
            session=session,
        )

        user = await validate_user_email_match(
            session=session,
            user_id=user_id,
            expected_email=old_email,
        )

        user.email = new_email

        if response:
            has_cookies, has_header = validate_token_presence(
                request,
                mode="require",
                raise_exception=False,
            )

            if has_cookies:
                response.delete_cookie("access_token")
                response.delete_cookie("refresh_token")

            if has_header:
                response.headers["Authorization"] = ""

        await session.commit()

        return {
            "status": "success",
            "message": "Email changed successfully",
            "new_email": new_email,
        }

    except HTTPException:
        raise
    except Exception:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to change email"
        )
