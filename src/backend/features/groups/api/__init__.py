from fastapi import APIRouter

from .group import router as group_router
from .group_invite import router as group_invite_router

router = APIRouter()

router.include_router(router=group_router)
router.include_router(router=group_invite_router)
