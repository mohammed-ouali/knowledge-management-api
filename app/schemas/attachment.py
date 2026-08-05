from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CommentCreate(BaseModel):
    note_id: int
    filename: str
    file_path: str


class CommentUpdate(BaseModel):
    filename: str | None = None
    file_path: str | None = None


class CommentResponse(BaseModel):
    id: int
    note_id: int
    filename: str
    file_path: str
    uploaded_at: datetime

    model_config = ConfigDict(
        from_attributes=True
        )