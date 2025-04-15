from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, UserProfile

from utils.JWT import hash_password

from core.schemas.user import (
    UserAuth,
    RegisterUser,
    UserAuthRead,
)


async def register_user(
    session: AsyncSession,
    user_data: RegisterUser,
) -> UserAuth:

    if True:  # ot await if_already_registered(session, user_data) or
        user = User(
            email=user_data.email,
            hashed_password=str(hash_password(user_data.hashed_password)),
            is_active=True,
            is_superuser=False,
            is_verified=False,
        )

        session.add(user)
        await session.flush()

        statement = select(User).filter_by(email=user_data.email)

        user_by_email = await session.scalars(statement)
        user_by_email = user_by_email.all()
        profile = UserProfile(
            user_id=user_by_email[0].id,
            name=user_data.name,
            surname=user_data.surname,
            patronymic=user_data.patronymic,
        )
        session.add(profile)

        await session.commit()
        return UserAuthRead.model_validate(user)
