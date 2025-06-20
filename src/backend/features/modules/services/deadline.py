import features.modules.crud.module as module_crud
from core.config import settings
from database import DbHelper
from utils import get_current_utc


async def check_modules_deadlines():
    local_db_helper = DbHelper(url=str(settings.db.url))

    async with local_db_helper.session_factory() as session:
        modules = await module_crud.get_modules(session)

        updated = False
        for module in modules:
            new_status = (
                module.start_datetime <= get_current_utc() <= module.end_datetime
            )
            if module.is_active != new_status:
                module.is_active = new_status
                updated = True

        if updated:
            await session.commit()

        await local_db_helper.dispose()
