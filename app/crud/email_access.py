from pydantic import EmailStr

from aiosmtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from core.config import settings


async def send_confirmation_email(
    email: EmailStr,
    token: str,
):
    msg = MIMEMultipart()
    msg["From"] = settings.smtp_email.user
    msg["To"] = email
    msg["Subject"] = "Подтверждение электронной почты"

    body = f"Пожалуйста, подтвердите вашу электронную почту, перейдя по следующей ссылке: http://localhost:8000/confirm_email?token={token}"
    msg.attach(MIMEText(body, "plain"))

    async with SMTP(
        hostname=settings.smtp_email.server, port=settings.smtp_email.port
    ) as server:
        await server.starttls()
        await server.login(settings.smtp_email.user, settings.smtp_email.password)
        await server.send_message(msg)
