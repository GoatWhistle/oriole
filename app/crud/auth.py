from os import access

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import (
    HTTPException,
    status,
    Form,
    Depends,
)

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from utils.JWT import (
    encode_jwt,
    validate_password,
    decode_jwt,
)
from jwt.exceptions import InvalidTokenError

from datetime import datetime
from pytz import utc

from core.schemas.token import AccessToken
from core.models import User, UserProfile

from utils.JWT import hash_password

from core.schemas.user import (
    UserAuth,
    RegisterUser,
    UserAuthRead,
    UserLogin,
)

http_bearer = HTTPBearer(auto_error=False)


async def register_user(
    session: AsyncSession,
    user_data: RegisterUser,
) -> UserAuth:

    try:
        user = User(
            email=user_data.email,
            hashed_password=hash_password(user_data.hashed_password),
        )

        session.add(user)
        await session.flush()

        statement = select(User).filter_by(email=user_data.email)

        user_by_email = await session.scalars(statement)
        user_by_email = user_by_email.all()
        profile = UserProfile(
            user_id=user_by_email[0].id,
            name=user_data.name,
            surname=user_data.surname,
            patronymic=user_data.patronymic,
        )
        session.add(profile)

        await session.commit()

        return UserAuthRead.model_validate(user)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with '{user_data.email}' email has already registered",
        )


async def validate_registered_user(
    session: AsyncSession,
    email: str = Form(),
    password: str = Form(),
):
    unauthed_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid login or password",
    )

    if not (user_by_email := await session.get(User, email)):
        raise unauthed_exception

    if not validate_password(
        password=password, hashed_password=user_by_email.hashed_password
    ):
        raise unauthed_exception
    if not user_by_email.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )

    if not user_by_email.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is unverified",
        )

    return user_by_email


def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> UserLogin:
    token = credentials.credentials
    try:
        payload = decode_jwt(
            token=token,
        )
        return payload

    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )


async def get_current_auth_user(
    session: AsyncSession,
    payload: dict = Depends(get_current_token_payload),
) -> UserLogin:
    email: str | None = payload.get("email")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid (email not found in payload)",
        )

    user_by_email = await session.get(User, email)
    if not user_by_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid (user not found)",
        )
    return user_by_email


def get_current_active_auth_user(
    user_data: UserLogin = Depends(get_current_auth_user),
):
    if user_data.is_active:
        return user_data
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User inactive",
    )


async def login_user(
    session: AsyncSession,
    user_data: UserLogin,
) -> AccessToken:
    statement = select(User).filter_by(email=user_data.email)

    user_by_email = await session.scalars(statement)
    user_by_email = user_by_email.all()[0]

    jwt_payload = {
        "id": user_by_email.id,
        "email": user_data.email,
    }
    token = encode_jwt(jwt_payload)

    access_token = AccessToken(
        user_id=user_by_email.id,
        access_token=token,
        created_at=int(datetime.now(utc).timestamp()),
    )
    session.add(access_token)
    await session.commit()

    return AccessToken.model_validate(access_token)
