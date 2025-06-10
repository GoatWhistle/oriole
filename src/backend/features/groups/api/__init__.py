from fastapi import APIRouter

from core.config import settings
from .account import router as account_router
from .group import router as group_router
from .invite import router as invite_router
from .module import router as module_router

router = APIRouter(prefix=settings.api.groups)

router.include_router(router=group_router)
router.include_router(router=module_router)
router.include_router(router=invite_router)
router.include_router(router=account_router)
