from fastapi import (
    APIRouter,
)

from core.config import settings

from .groups import router as groups_router
from .assignments import router as assignments_router
from .tasks import router as tasks_router
from .users import router as users_router
from .auth import router as auth_router
from .email_access import router as email_access_router


router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(
    router=groups_router,
    tags=[settings.api.v1.groups[1:].capitalize()],
    prefix=settings.api.v1.learn + settings.api.v1.groups,
)

router.include_router(
    router=assignments_router,
    tags=[settings.api.v1.assignments[1:].capitalize()],
    prefix=settings.api.v1.assignments,
)
router.include_router(
    router=tasks_router,
    tags=[settings.api.v1.tasks[1:].capitalize()],
    prefix=settings.api.v1.tasks,
)

router.include_router(
    router=users_router,
    tags=[settings.api.v1.users[1:].capitalize()],
    prefix=settings.api.v1.users,
)

router.include_router(
    router=auth_router,
    tags=[settings.api.v1.auth[1:].capitalize()],
)

router.include_router(
    router=email_access_router,
    tags=[settings.api.v1.email_verify[1:].capitalize()],
    prefix=settings.api.v1.email_verify,
)
