from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CommentCreate(BaseModel):
    content: str
    not_id: int
    author_id: int


class CommentUpdate(BaseModel):
    content: str | None = None


class CommentResponse(BaseModel):
    id: int
    content: str
    note_id: int
    author_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )