from fastapi import (
    Depends,
    Response,
    Request,
)
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from pydantic.v1 import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from core.config import settings
from database import db_helper
from features.users.schemas import (
    UserAuth,
    RegisterUserInput,
    UserAuthRead,
    UserLogin,
    UserRead,
    UserProfileRead,
    TokenResponseForOAuth2,
)

from features.users.crud.user import (
    get_user_by_email,
    create_user,
)
from features.users.crud.user_profile import (
    create_user_profile,
)

from features.users.services.token_operations import (
    get_valid_payload,
    clear_auth_tokens,
)

from core.celery.email_tasks import send_confirmation_email
from features.users.validators.rules import validate_activity_and_verification
from utils.JWT import (
    create_access_token,
    create_refresh_token,
    create_email_confirmation_token,
    create_password_confirmation_token,
)
from features.users.validators.existence import (
    ensure_user_not_exists_by_email,
    get_user_profile_if_exists,
    validate_token_has_email,
    validate_token_has_user_id,
    is_email_entered,
    ensure_no_tokens,
    ensure_user_exists_by_email,
    has_any_token,
)
from features.users.validators.password import validate_password_matching
from features.users.services.token_operations import _set_auth_cookies


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


async def get_non_expire_payload_token(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    token: str | None = Depends(OAuth2_scheme),
) -> dict:
    return await get_valid_payload(request, response, session, token)


async def get_current_auth_user(
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    payload: dict = Depends(get_non_expire_payload_token),
) -> UserAuth:
    email = payload.get("email")

    user_from_db = await get_user_by_email(session=session, email=email)
    await validate_activity_and_verification(user_from_db=user_from_db)

    return UserAuthRead.model_validate(user_from_db)


def get_current_active_auth_user_id(
    user_from_db: UserAuthRead = Depends(get_current_auth_user),
) -> int | Mapped[int]:
    return user_from_db.id


async def register_user(
    request: Request,
    session: AsyncSession,
    user_data: RegisterUserInput,
) -> UserAuth:
    ensure_no_tokens(request)
    await ensure_user_not_exists_by_email(session, user_data.email)

    try:
        user = await create_user(
            session=session,
            user_data=user_data,
        )

        await create_user_profile(
            session=session,
            user_id=user.id,
            profile_data=user_data,
        )

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

    except Exception as e:
        raise e


async def validate_registered_user(
    user_data: UserLogin,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
):
    email = user_data.email
    password = user_data.password

    user_from_db = await get_user_by_email(session=session, email=email)

    await validate_activity_and_verification(user_from_db=user_from_db)

    validate_password_matching(
        password=password,
        hashed_password=user_from_db.hashed_password,
    )

    return UserLogin.model_validate(user_data)


async def login_user(
    session: AsyncSession,
    user_data: UserLogin,
    response: Response,
) -> TokenResponseForOAuth2:

    user_by_email = await get_user_by_email(session=session, email=user_data.email)
    await validate_activity_and_verification(user_from_db=user_by_email)

    access_token = create_access_token(user_by_email.id, user_by_email.email)
    refresh_token = create_refresh_token(user_by_email.id, user_by_email.email)

    _set_auth_cookies(
        response=response,
        access_token=access_token,
        refresh_token=refresh_token,
        access_expires=settings.auth_jwt.access_token_lifetime_seconds,
        refresh_expires=settings.auth_jwt.refresh_token_lifetime_seconds,
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
) -> dict:
    if has_any_token(request):
        clear_auth_tokens(request, response)

    return {"message": "Logout done!"}


async def check_auth(
    session: AsyncSession,
    payload: dict,
) -> UserRead:
    email = validate_token_has_email(payload)
    user_id = validate_token_has_user_id(payload)

    user_from_db = await get_user_by_email(session=session, email=email)

    await validate_activity_and_verification(user_from_db=user_from_db)

    profile_from_db = await get_user_profile_if_exists(session, user_id)

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
    await is_email_entered(email)

    user_from_db = await ensure_user_exists_by_email(session=session, email=email)

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

    token = create_email_confirmation_token(
        user_email=user_data.email,
        user_id=user_data.id,
    )

    await send_confirmation_email(
        request=request,
        email=user_data.email,
        token=token,
        html_file="verified_email.html",
    )
