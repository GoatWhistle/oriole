from pydantic import BaseModel


class TokenResponseForOAuth2(BaseModel):
    access_token: str
    token_type: str = "bearer"
