from datetime import datetime

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
from jwt.exceptions import InvalidTokenError
from pydantic.v1 import EmailStr
from pytz import utc
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from core.config import settings
from database import db_helper
from features.users.models import User, UserProfile
from features.users.schemas import (
    UserAuth,
    RegisterUserInput,
    RegisterUserInternal,
    UserAuthRead,
    UserLogin,
    UserRead,
    UserProfileRead,
    TokenResponseForOAuth2,
)
from features.users.services.email_access import send_confirmation_email
from features.users.validators import validate_activity_and_verification
from utils.JWT import (
    validate_password,
    create_access_token,
    create_refresh_token,
    create_email_confirmation_token,
    create_password_confirmation_token,
    decode_jwt,
    hash_password,
)


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
    tokenUrl="/api/auth/token",
    auto_error=False,
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
        current_time_utc = datetime.now(utc).timestamp()
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
            value=access_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=settings.auth_jwt.access_token_lifetime_seconds,
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="strict",
            path="/",
            max_age=settings.auth_jwt.refresh_token_lifetime_seconds,
        )

        return f"Bearer {access_token}"

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )


async def register_user(
    request: Request,
    session: AsyncSession,
    user_data: RegisterUserInput,
) -> UserAuth:
    access_token_cookie = request.cookies.get("access_token")
    refresh_token_cookie = request.cookies.get("refresh_token")

    auth_header = request.headers.get("Authorization")

    if auth_header or access_token_cookie or refresh_token_cookie:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authenticated users cannot register new accounts",
        )

    try:
        internal_data = RegisterUserInternal(**user_data.model_dump())
        internal_data.is_active = True
        internal_data.is_verified = False

        user = User(
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
            is_active=internal_data.is_active,
            is_verified=internal_data.is_verified,
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

        token = create_email_confirmation_token(
            user_id=user.id,
            user_email=user_data.email,
        )

        await send_confirmation_email(
            request=request,
            email=user_data.email,
            token=token,
            html_file="verified_email.html",
        )

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


async def login_user(
    session: AsyncSession,
    user_data: UserLogin,
    response: Response,
) -> TokenResponseForOAuth2:

    statement = select(User).filter_by(email=user_data.email)
    user_by_email = await session.scalars(statement)
    user_by_email = user_by_email.first()

    await validate_activity_and_verification(user_from_db=user_by_email)

    access_token = create_access_token(user_by_email.id, user_by_email.email)
    refresh_token = create_refresh_token(user_by_email.id, user_by_email.email)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.auth_jwt.access_token_lifetime_seconds,
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="strict",
        path="/",
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


async def logout(
    request: Request,
    response: Response,
):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    if "authorization" in request.headers:
        response.headers["Authorization"] = ""

    return {"message": "Logout done!"}


async def check_auth(
    session: AsyncSession,
    payload: dict,
) -> UserRead:
    email = payload.get("email")
    user_id = int(payload.get("sub"))

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid (email not found in payload)",
        )

    statement = select(User).filter_by(email=email)
    user_from_db = await session.scalars(statement)
    user_from_db = user_from_db.first()

    await validate_activity_and_verification(user_from_db=user_from_db)

    statement = select(UserProfile).filter_by(user_id=user_id)
    profile_from_db = await session.scalars(statement)
    profile_from_db = profile_from_db.first()

    if not profile_from_db:
        raise HTTPException(
            status_code=404,
            detail="Profile not found",
        )

    profile_and_email = UserRead(
        email=email,
        profile=UserProfileRead(
            user_id=profile_from_db.user_id,
            name=profile_from_db.name,
            surname=profile_from_db.surname,
            patronymic=profile_from_db.patronymic,
        ),
    )

    return UserRead.model_validate(profile_and_email)


async def reset_password(
    request: Request,
    user_from_db: UserAuthRead,
):
    token = create_password_confirmation_token(
        user_email=user_from_db.email,
        user_id=user_from_db.id,
    )

    await send_confirmation_email(
        request=request,
        email=user_from_db.email,
        token=token,
        html_file="password_reset_warning.html",
        address_type="reset_password",
    )

    return {"message": "Password reset link has been sent to your email"}


async def forgot_password(
    request: Request,
    email: EmailStr,
    session: AsyncSession,
):
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Please enter an email",
        )

    statement = select(User).filter_by(email=email)
    user_from_db = await session.scalars(statement)
    user_from_db = user_from_db.first()

    if not user_from_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found",
        )

    token = create_password_confirmation_token(
        user_email=user_from_db.email,
        user_id=user_from_db.id,
    )

    await send_confirmation_email(
        request=request,
        email=user_from_db.email,
        token=token,
        html_file="forgot_password_warning.html",
        address_type="forgot_password",
    )

    return {"message": "Password reset link has been sent to your email"}


async def send_confirmation_email_again(
    request: Request,
    user_data: UserAuthRead,
):

    token = create_password_confirmation_token(
        user_email=user_data.email,
        user_id=user_data.id,
    )

    await send_confirmation_email(
        request=request,
        email=user_data.email,
        token=token,
        html_file="verified_email.html",
    )
