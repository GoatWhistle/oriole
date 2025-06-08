from fastapi import APIRouter, status

from features.modules.services import deadline as service

router = APIRouter()


@router.get(
    "/check-deadlines/",
    status_code=status.HTTP_200_OK,
)
async def check_modules_deadlines():
    return await service.check_modules_deadlines()