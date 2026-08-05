from datetime import datetime

from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    username: str
    email: str 
    password: str 


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)