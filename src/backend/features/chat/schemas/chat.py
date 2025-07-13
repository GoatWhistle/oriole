from pydantic import BaseModel


class ChatResponse(BaseModel):
    chat_id: int
    group_id: int
    creator_id: int


class ChatCreateRequest(BaseModel):
    group_id: int
