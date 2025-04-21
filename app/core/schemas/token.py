from typing import Annotated

from pydantic import BaseModel, Field


class AccessToken(BaseModel):
    user_id: int
    token: str
    created_at: int
