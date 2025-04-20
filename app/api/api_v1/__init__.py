from fastapi import (
    APIRouter,
)

from core.config import settings

from .groups import router as groups_router
from .assignments import router as assignments_router
from .tasks import router as tasks_router
from .users import router as users_router
from .auth import router as auth_router


router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(
    groups_router,
    prefix=settings.api.v1.learn + settings.api.v1.groups,
)

router.include_router(
    assignments_router,
    prefix=settings.api.v1.assignments,
)
router.include_router(
    tasks_router,
    prefix=settings.api.v1.tasks,
)

router.include_router(
    users_router,
    prefix=settings.api.v1.users,
)

router.include_router(
    auth_router,
    prefix=settings.api.v1.auth,
)
