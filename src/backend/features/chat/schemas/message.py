from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MessageOut(BaseModel):
    message_id: int
    account_id: int
    message: str
    timestamp: datetime
    reply_to: Optional[int] = None
    reply_to_text: Optional[str] = None

    class Config:
        orm_mode = True
