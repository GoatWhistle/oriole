from pydantic import BaseModel


class TokenResponseForOAuth2(BaseModel):
    access_token: str
    token_type: str = "bearer"


class SuccessVerify(BaseModel):
    user_id: int
    message: str
    status: str


class SuccessAuthAction(BaseModel):
    message: str
