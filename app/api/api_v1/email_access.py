from fastapi import (
    APIRouter,
    Depends,
    status,
)

router = APIRouter()


@router.get("/verify/{token}")
async def confirm_email(token: str):
    pass
