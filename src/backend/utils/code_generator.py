from secrets import choice
from string import ascii_uppercase, digits

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from groups.models.group_invite import GroupInvite


def generate_random_code(length: int = 7) -> str:
    alphabet = ascii_uppercase + digits
    return "".join(choice(alphabet) for _ in range(length))


async def generate_unique_group_invite_code(
    session: AsyncSession,
    length: int = 7,
) -> str:
    while True:
        code = generate_random_code(length)
        result = await session.execute(
            select(GroupInvite).where(GroupInvite.code == code)
        )
        if not result.scalar_one_or_none():
            return code
