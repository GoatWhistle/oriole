from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from core.config import settings
from core.models import db_helper
from core.models.user import User

from core.exceptions.user import (
    get_user_or_404_with_return,
)

from core.schemas.assignment import AssignmentRead
from core.schemas.group import GroupRead
from core.schemas.task import TaskRead

from crud import users as crud

router = APIRouter(
    prefix=settings.api.v1.users,
)
