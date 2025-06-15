from fastapi import HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from features.users.models import User
from features.users.validators import check_expiration_after_redirect
from utils.JWT import decode_jwt, validate_password, hash_password
from urllib.parse import urljoin


templates = Jinja2Templates(directory="templates/email")


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

        user = await session.get(User, int(dict_token["sub"]))
        user.is_verified = True

        await session.commit()
        await session.refresh(user)

        return {"status": "success", "message": "You are verified"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")


async def reset_password_redirect(
    token: str,
    new_password: str,
    session: AsyncSession,
):
    try:
        dict_token = decode_jwt(token)
        check_expiration_after_redirect(payload=dict_token)

        user_from_db = await session.get(User, int(dict_token["sub"]))

        if validate_password(
            password=new_password, hashed_password=str(user_from_db.hashed_password)
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The new password must be different from the previous one.",
            )
        user_from_db.hashed_password = hash_password(new_password)
        await session.commit()
        await session.refresh(user_from_db)

        return {"status": "success", "message": "You changed password"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")


async def forgot_password_redirect(
    token: str,
    new_password: str,
    session: AsyncSession,
):
    try:
        dict_token = decode_jwt(token)
        check_expiration_after_redirect(payload=dict_token)

        user_from_db = await session.get(User, int(dict_token["sub"]))

        if validate_password(
            password=new_password, hashed_password=str(user_from_db.hashed_password)
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The new password must be different from the previous one.",
            )
        user_from_db.hashed_password = hash_password(new_password)
        await session.commit()
        await session.refresh(user_from_db)

        return {"status": "success", "message": "You changed password"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
