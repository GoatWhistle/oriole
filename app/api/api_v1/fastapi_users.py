from fastapi_users import FastAPIUsers

from core.models import User
from core.types.user_id import UserIdType

from api.api_v1.dependencies.authentication.user_manager import get_user_manager
from api.api_v1.dependencies.authentication.backend import authentication_backend

fastapi_users = FastAPIUsers[User, UserIdType](
    get_user_manager,
    [authentication_backend],
)
current_active_user = fastapi_users.current_user(active=True)
