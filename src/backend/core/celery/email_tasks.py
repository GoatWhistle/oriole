import asyncio

from pydantic import EmailStr
from fastapi import Request

from core.celery.app import app
from features.users.services.email_access import send_confirmation_email_base


@app.task
def _send_confirmation_email_task(
    base_url: str,
    email: str,
    token: str,
    html_file: str,
    address_type: str = "",
):
    asyncio.run(
        send_confirmation_email_base(
            base_url=base_url,
            email=email,
            token=token,
            html_file=html_file,
            address_type=address_type,
        )
    )


async def send_confirmation_email(
    request: Request,
    email: EmailStr,
    token: str,
    html_file: str,
    address_type: str = "",
):
    base_url = str(request.base_url)
    _send_confirmation_email_task.delay(
        base_url=base_url,
        email=str(email),
        token=token,
        html_file=html_file,
        address_type=address_type,
    )
