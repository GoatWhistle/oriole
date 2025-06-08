from fastapi import APIRouter, status

from features.tasks.services import deadline as service

router = APIRouter()


@router.get(
    "/check-deadlines/",
    status_code=status.HTTP_200_OK,
)
async def check_tasks_deadlines():
    return await service.check_tasks_deadlines()