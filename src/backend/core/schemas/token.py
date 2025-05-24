from typing import Annotated

from pydantic import BaseModel, Field

class TokenResponseForOAuth2(BaseModel):
    access_token: str
    token_type: str = "bearer"
