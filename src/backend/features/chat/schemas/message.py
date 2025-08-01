from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MessageOut(BaseModel):
    message_id: int
    account_id: int
    message: str
    timestamp: datetime
    reply_to: int | None = None
    reply_to_text: str | None = None
    is_edited: bool = False

    class Config:
        orm_mode = True
