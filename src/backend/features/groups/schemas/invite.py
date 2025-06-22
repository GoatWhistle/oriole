from pydantic import BaseModel


class LinkRead(BaseModel):
    link: str


class LinkJoinRead(BaseModel):
    group_id: str
