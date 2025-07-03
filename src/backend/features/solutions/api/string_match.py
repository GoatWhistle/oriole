# from fastapi import APIRouter, Depends, status
# from sqlalchemy.ext.asyncio import AsyncSession
#
# import features.tasks.services.string_match as service
# from database import db_helper
# from features.users.services.auth import get_current_active_auth_user_id
# from utils.response_func import create_json_response
#
# router = APIRouter()
#
#
# @router.patch(
#     "/{task_id}/complete/",
#     response_model=TaskRead,
#     status_code=status.HTTP_200_OK,
# )
# async def try_to_complete_task(
#     task_id: int,
#     user_answer: str,
#     session: AsyncSession = Depends(db_helper.dependency_session_getter),
#     user_id: int = Depends(get_current_active_auth_user_id),
# ):
#     data = await service.try_to_complete_task(session, user_id, task_id, user_answer)
#     return create_json_response(data=data)
