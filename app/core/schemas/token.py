from pydantic import BaseModel

class AccessToken(BaseModel):
    user_id: int
    access_token: str
    created_at: int
