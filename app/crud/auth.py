from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from fastapi import (
    HTTPException,
    status,
    Depends,
    Response,
)

from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from sqlalchemy.orm import Mapped

from utils.JWT import (
    encode_jwt,
    validate_password,
    decode_jwt,
    create_access_token,
    create_refresh_token,
)
from jwt.exceptions import InvalidTokenError

from datetime import datetime
from pytz import utc

from core.schemas.token import TokenResponseForOAuth2
from core.models import User, UserProfile, db_helper
from core.config import settings

from .email_access import send_confirmation_email

from utils.JWT import hash_password

from core.schemas.user import (
    UserAuth,
    RegisterUser,
    UserAuthRead,
    UserLogin,
)

OAuth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


async def register_user(
    session: AsyncSession,
    user_data: RegisterUser,
) -> UserAuth:

    try:
        user_data.is_active = True
        user_data.is_verified = False

        user = User(
            email=user_data.email,
            hashed_password=hash_password(user_data.hashed_password),
            is_active=user_data.is_active,
            is_verified=user_data.is_verified,
        )

        session.add(user)
        await session.flush()

        statement = select(User).filter_by(email=user_data.email)

        user_by_email = await session.scalars(statement)
        user_by_email = user_by_email.first()
        profile = UserProfile(
            user_id=user_by_email.id,
            name=user_data.name,
            surname=user_data.surname,
            patronymic=user_data.patronymic,
        )
        session.add(profile)
        await session.commit()

        jwt_payload = {
            "sub": str(user_by_email.id),
            "email": user_data.email,
        }

        token = encode_jwt(jwt_payload)

        await send_confirmation_email(email=user_data.email, token=token)

        return UserAuthRead.model_validate(user)

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with '{user_data.email}' email has already registered",
        )
    except Exception as e:
        raise e


def get_current_token_payload(
    token: str = Depends(OAuth2_scheme),
) -> dict:
    if token is None or token == "undefined":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated (missing or invalid token)",
        )
    try:
        if token.startswith("Bearer "):
            token = token[7:]

        payload = decode_jwt(token=token)

        if payload.get("iat", 0) > payload.get("exp", 0):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
            )

        return payload

    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token error: {e}",
        )


async def get_current_auth_user(
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    payload: dict = Depends(get_current_token_payload),
) -> UserAuth:
    email = payload.get("email")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid (email not found in payload)",
        )

    statement = select(User).filter_by(email=email)
    user_from_db = await session.scalars(statement)
    user_from_db = user_from_db.first()

    if not user_from_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid (user not found)",
        )
    return UserAuthRead.model_validate(user_from_db)


def get_current_active_auth_user_id(
    user_data: UserAuthRead = Depends(get_current_auth_user),
) -> int | Mapped[int]:
    if user_data.is_active:
        return user_data.id

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User inactive",
    )


async def validate_registered_user(
    user_data: UserLogin,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
):
    email = user_data.email
    password = user_data.password

    statement = select(User).filter_by(email=email)
    user_from_db = await session.scalars(statement)
    user_from_db = user_from_db.first()

    unauthed_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid login or password",
    )

    if not user_from_db:
        raise unauthed_exception

    if not validate_password(
        password=password, hashed_password=str(user_from_db.hashed_password)
    ):
        raise unauthed_exception

    if not user_from_db.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )

    if not user_from_db.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is unverified",
        )

    return UserLogin.model_validate(user_data)


async def login_user(
    session: AsyncSession,
    user_data: UserLogin,
    response: Response,
) -> TokenResponseForOAuth2:

    statement = select(User).filter_by(email=user_data.email)
    user_by_email = await session.scalars(statement)
    user_by_email = user_by_email.first()

    access_token = create_access_token(user_by_email.id, user_by_email.email)
    refresh_token = create_refresh_token(user_by_email.id, user_by_email.email)

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=False,  # TODO: потом поставить на True!!!
        samesite="lax",
        max_age=settings.auth_jwt.access_token_lifetime_seconds,
    )

    return TokenResponseForOAuth2(
        access_token=access_token,
        token_type="bearer",
    )


async def login_for_token(
    response: Response,
    session: AsyncSession,
    form_data: OAuth2PasswordRequestForm,
) -> TokenResponseForOAuth2:
    user_data = UserLogin(
        email=form_data.username,
        password=form_data.password,
    )
    await validate_registered_user(user_data, session)

    return await login_user(session, user_data, response)
