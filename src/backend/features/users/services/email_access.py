from urllib.parse import urljoin

from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from features.users.crud.user import (
    get_user_by_id,
    update_user_verification_status,
)
from features.users.services.password_operations import change_password_with_token
from features.users.validators import check_expiration_after_redirect
from utils.JWT import decode_jwt

templates = Jinja2Templates(directory="src/frontend/src/templates/email")


async def send_confirmation_email_base(
    base_url: str,
    email: str,
    token: str,
    html_file: str,
    address_type: str = "",
):

    conf = ConnectionConfig(
        MAIL_USERNAME=settings.smtp_email.user,
        MAIL_PASSWORD=settings.smtp_email.password,
        MAIL_FROM=settings.smtp_email.user,
        MAIL_PORT=settings.smtp_email.port,
        MAIL_SERVER=settings.smtp_email.server,
        MAIL_FROM_NAME=settings.smtp_email.user,
        MAIL_SSL_TLS=False,
        MAIL_STARTTLS=True,
    )

    base_url = base_url.rstrip("/")

    address = getattr(settings.api, address_type, "")
    full_path = f"{settings.api.prefix}{settings.api.email_verify}{address}/{token}"

    link = urljoin(base_url, full_path)
    html_body = templates.get_template(html_file).render(link=link)

    message = MessageSchema(
        subject="Email Confirmation",
        recipients=[email],
        body=html_body,
        subtype="html",
    )
    fm = FastMail(conf)
    await fm.send_message(message)


async def verify(
    token: str,
    session: AsyncSession,
):
    try:
        dict_token = decode_jwt(token)
        check_expiration_after_redirect(payload=dict_token)
        user_id = int(dict_token["sub"])
        user = await get_user_by_id(session=session, user_id=user_id)

        await update_user_verification_status(session, user=user)

        return {"status": "success", "message": "You are verified"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")


async def reset_password_redirect(
    token: str,
    new_password: str,
    session: AsyncSession,
):
    return await change_password_with_token(
        token=token,
        new_password=new_password,
        session=session,
    )


async def forgot_password_redirect(
    token: str,
    new_password: str,
    session: AsyncSession,
):
    return await change_password_with_token(
        token=token,
        new_password=new_password,
        session=session,
    )


# async def change_email_redirect(
#     token: str,
#     new_email: EmailStr,
#     session: AsyncSession,
# ):
#     return await change_email_with_token(
#         token=token,
#         new_email=new_email,
#         session=session,
#     )
