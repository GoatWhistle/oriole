from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import (
    HTTPException,
    status,
    Depends,
)

from fastapi.security import (
    OAuth2PasswordBearer,
)
from sqlalchemy.orm import Mapped

from utils.JWT import (
    encode_jwt,
    validate_password,
    decode_jwt,
)
from jwt.exceptions import InvalidTokenError

from datetime import datetime
from pytz import utc

from core.schemas.token import AccessToken as AccessTokenSchema
from core.models import User, UserProfile, AccessToken, db_helper

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
        user_data.is_verified = True

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

        return UserAuthRead.model_validate(user)

    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with '{user_data.email}' email has already registered",
        )


def get_current_token_payload(
    token: str = Depends(OAuth2_scheme),
) -> dict:
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated (missing or invalid token)",
        )
    try:
        payload = decode_jwt(token=token)
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
    email: str | None = payload.get("email")
    if email is None:
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


async def get_current_active_auth_user_id(
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_data: UserAuthRead = Depends(get_current_auth_user),
) -> int | Mapped[int]:
    if user_data.is_active:
        statement = select(User).filter_by(email=user_data.email)
        user_from_db = await session.scalars(statement)
        user_from_db = user_from_db.first()
        return user_from_db.id

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
) -> AccessTokenSchema:
    statement = select(User).filter_by(email=user_data.email)

    user_by_email = await session.scalars(statement)
    user_by_email = user_by_email.first()

    jwt_payload = {
        "sub": str(user_by_email.id),
        "email": user_data.email,
    }
    token = encode_jwt(jwt_payload)

    access_token = AccessToken(
        user_id=user_by_email.id,
        token=token,
        created_at=int(datetime.now(utc).timestamp()),
    )
    session.add(access_token)
    await session.commit()

    return AccessTokenSchema.model_validate(access_token.__dict__)
