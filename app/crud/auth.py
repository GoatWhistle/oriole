from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from fastapi import (
    HTTPException,
    status,
    Depends,
    Response,
    Request,
)

from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from sqlalchemy.orm import Mapped

from utils.JWT import (
    validate_password,
    decode_jwt,
    create_access_token,
    create_refresh_token,
)
from jwt.exceptions import InvalidTokenError


from core.schemas.token import TokenResponseForOAuth2
from core.models import User, UserProfile, db_helper
from core.config import settings

from .email_access import send_confirmation_email

from utils.JWT import hash_password, encode_jwt

from core.schemas.user import (
    UserAuth,
    RegisterUser,
    UserAuthRead,
    UserLogin,
)
from datetime import datetime
from pytz import utc


class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> str | None:
        token = request.cookies.get("access_token")
        if token:
            return token

        auth_header = await super().__call__(request)
        if auth_header:
            return auth_header

        return None


OAuth2_scheme = OAuth2PasswordBearerWithCookie(
    tokenUrl="/api/v1/auth/token",
    auto_error=False,
)


async def register_user(
    request: Request,
    session: AsyncSession,
    user_data: RegisterUser,
) -> UserAuth:
    access_token_cookie = request.cookies.get("access_token")
    refresh_token_cookie = request.cookies.get("refresh_token")

    auth_header = request.headers.get("Authorization")

    if auth_header or access_token_cookie or refresh_token_cookie:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authenticated users cannot register new accounts. Please logout first.",
        )

    try:
        user_data.is_active = True
        user_data.is_verified = False

        user = User(
            email=user_data.email,
            hashed_password=hash_password(user_data.hashed_password),
            is_active=True,
            is_verified=True,
        )
        session.add(user)
        await session.flush()

        profile = UserProfile(
            user_id=user.id,
            name=user_data.name,
            surname=user_data.surname,
            patronymic=user_data.patronymic,
        )
        session.add(profile)
        await session.commit()

        jwt_payload = {
            "sub": str(user.id),
            "email": user_data.email,
        }

        token = encode_jwt(jwt_payload)

        await send_confirmation_email(email=user_data.email, token=token)

        return UserAuthRead.model_validate(user)

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{user_data.email}' is already registered",
        )
    except Exception as e:
        raise e


async def validate_registered_user(
    user_data: UserLogin,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
):
    email = user_data.email
    password = user_data.password

    statement = select(User).filter_by(email=email)
    user_from_db = await session.scalars(statement)
    user_from_db = user_from_db.first()

    await validate_activity_and_verification(user_from_db=user_from_db)

    if not validate_password(
        password=password, hashed_password=str(user_from_db.hashed_password)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login or password",
        )

    return UserLogin.model_validate(user_data)


async def validate_activity_and_verification(
    user_from_db: UserAuthRead,
):
    if not user_from_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login or password",
        )

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


async def refresh_if_needed(
    request: Request,
    response: Response,
    session: AsyncSession,
    token: str | None,
) -> str | None:
    try:
        if token.startswith("Bearer "):
            token = token[7:]

        payload = decode_jwt(token=token)
        current_time_utc = datetime.now(utc)
        if int(current_time_utc) < int(payload.get("exp", 0)):
            return None

        return await refresh_tokens(
            request=request,
            response=response,
            session=session,
        )
    except HTTPException:
        return None


def get_current_token_payload(
    token: str,
) -> dict:
    try:
        if token.startswith("Bearer "):
            token = token[7:]

        payload = decode_jwt(token=token)
        return payload

    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token error: {e}",
        )


async def get_non_expire_payload_token(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    token: str | None = Depends(OAuth2_scheme),
) -> str:
    if token:
        new_token = await refresh_if_needed(
            request=request,
            response=response,
            session=session,
            token=token,
        )
        if new_token:
            token = new_token
        return get_current_token_payload(token)

    new_token = await refresh_tokens(request, response, session)
    return get_current_token_payload(new_token)


async def get_current_auth_user(
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    payload: dict = Depends(get_non_expire_payload_token),
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

    await validate_activity_and_verification(user_from_db=user_from_db)

    return UserAuthRead.model_validate(user_from_db)


def get_current_active_auth_user_id(
    user_from_db: UserAuthRead = Depends(get_current_auth_user),
) -> int | Mapped[int]:
    return user_from_db.id


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

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  # TODO: потом поставить на True!!!
        samesite="lax",  # strict
        path="/",  # auth/refresh
        max_age=settings.auth_jwt.refresh_token_lifetime_seconds,
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


async def refresh_tokens(
    request: Request,
    response: Response,
    session: AsyncSession,
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is missing, sign in again",
        )

    try:
        payload = decode_jwt(refresh_token)
        user_email = payload.get("email")
        user_id = payload.get("sub")

        if not user_email or not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        statement = select(User).filter_by(email=user_email)
        user_from_db = await session.scalars(statement)
        user_from_db = user_from_db.first()

        await validate_activity_and_verification(user_from_db=user_from_db)

        access_token = create_access_token(user_id, user_email)
        refresh_token = create_refresh_token(user_id, user_email)

        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            secure=False,  # TODO: потом поставить на True!!!
            samesite="lax",
            max_age=settings.auth_jwt.access_token_lifetime_seconds,
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,  # TODO: потом поставить на True!!!
            samesite="lax",
            path="/",
            max_age=settings.auth_jwt.refresh_token_lifetime_seconds,
        )

        return f"Bearer {access_token}"

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )


async def logout(
    request: Request,
    response: Response,
):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    if "authorization" in request.headers:
        response.headers["Authorization"] = ""

    return {"logout": "Logout done!"}
