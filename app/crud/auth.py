from fastapi import Depends

from typing import Sequence, Annotated
from sqlalchemy import select, and_
from sqlalchemy.engine import Result

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, Group, Task, Account, Assignment
from core.schemas.group import GroupRead
from core.schemas.task import TaskRead
from core.schemas.assignment import AssignmentRead

from utils.JWT import hash_password

from core.exceptions.user import (
    get_user_or_404_with_return,
    check_teacher_or_403,
    if_already_registered,
)
from core.schemas.user import (
    UserCreate,
    UserRead,
    UserUpdate,
    UserProfile,
    UserAuth,
    RegisterUser,
)


async def register_user(
    session: AsyncSession,
    user_data: RegisterUser,
) -> RegisterUser:

    if not await if_already_registered(session, user_data):
        user = User(
            email=user_data.email,
            hashed_password=hash_password(user_data.hashed_password),
            is_active=True,
            is_superuser=False,
            is_verified=False,
        )

        session.add(user)
        await session.flush()

        user_by_email = await session.get(User, user_data.email)
        profile = UserProfile(
            user_id=user_by_email.id,
            name=user_data.name,
            surname=user_data.surname,
            patronymic=user_data.patronymic,
        )
        session.add(profile)

        await session.commit()
        await session.refresh(user)

        return RegisterUser.model_validate(user)
