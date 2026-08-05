from datetime import datetime

from pydantic import BaseModel, ConfigDict

class FolderCreate(BaseModel):
    name: str
    user_id: int


class FolderUpdate(BaseModel):
    name: str | None = None


class FolderResponse(BaseModel):
    id: int
    name: str
    user_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )