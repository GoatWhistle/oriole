from sqlalchemy import select

from core.config import settings
from database import DbHelper
from features.modules.models import Module
from utils import get_current_utc


async def check_modules_deadlines():
    local_db_helper = DbHelper(
        db_url=str(settings.db.db_url),
    )

    async with local_db_helper.session_factory() as session:
        current_time = get_current_utc()
        result = await session.execute(
            select(Module).where(
                (Module.start_datetime <= current_time)
                | (Module.end_datetime <= current_time)
            )
        )
        modules = result.scalars().all()

        updated_count = 0
        for module in modules:
            new_status = module.start_datetime <= current_time <= module.end_datetime
            if module.is_active != new_status:
                module.is_active = new_status
                updated_count += 1

        if updated_count > 0:
            await session.commit()

        await local_db_helper.dispose()

        return updated_count