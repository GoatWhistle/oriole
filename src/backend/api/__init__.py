from fastapi import APIRouter

from core.config import settings
from features.chat.api.websocket import router as chat_router
from features.groups.api import router as groups_router
from features.modules.api import router as moduls_router
from features.tasks.api import router as tasks_router
from features.users.api.auth import router as auth_router
from features.users.api.telegram_auth import router as telegram_auth
from features.users.api.email_access import router as email_access_router
from features.users.api.user import router as users_router
from features.chat.api.сhat import router as chats_router


router = APIRouter(prefix=settings.api.prefix)

router.include_router(
    router=groups_router,
    tags=[settings.api.groups[1:].capitalize()],
    prefix=settings.api.groups,
)

router.include_router(
    router=moduls_router,
    tags=[settings.api.modules[1:].capitalize()],
    prefix=settings.api.modules,
)

router.include_router(
    router=tasks_router,
    tags=[settings.api.tasks[1:].capitalize()],
    prefix=settings.api.tasks,
)

router.include_router(
    router=users_router,
    tags=[settings.api.users[1:].capitalize()],
    prefix=settings.api.users,
)

router.include_router(
    router=auth_router,
    tags=[settings.api.auth[1:].capitalize()],
    prefix=settings.api.auth,
)

router.include_router(
    router=telegram_auth,
    tags=[settings.api.auth[1:].capitalize()],
    prefix=settings.api.telegram_auth,
)

router.include_router(
    router=email_access_router,
    tags=[settings.api.email_verify[1:].capitalize()],
    prefix=settings.api.email_verify,
)
router.include_router(
    router=chat_router,
    tags=[settings.api.websocket[1:].capitalize()],
    prefix=settings.api.websocket,
)

router.include_router(
    router=chats_router,
    tags=[settings.api.chat[1:].capitalize()],
    prefix=settings.api.chat,
)
