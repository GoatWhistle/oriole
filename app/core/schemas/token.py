from pydantic import BaseModel


class AccessToken(BaseModel):
    user_id: str
    access_token: str
    created_at: str
    token_type: str
