from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NoteCreate(BaseModel):
    folder_id: int
    author_id: int
    title: str
    content: str


class NoteUpdate(BaseModel):
    folder_id: int | None = None
    title: str | None = None
    content: str | None = None


class NoteResponse(BaseModel):
    id: int
    folder_id: int
    author_id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)