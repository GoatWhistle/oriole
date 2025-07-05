from fastapi import APIRouter

from .group import router as group_router
from .invite import router as invite_router

router = APIRouter()

router.include_router(router=group_router)
router.include_router(router=invite_router)
