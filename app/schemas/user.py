from __future__ import annotations

from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)


class UserBase(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_-]+$",
    )
    email: EmailStr

    @field_validator("username")
    @classmethod
    def sanitize_and_validate_username(cls, value: str) -> str:
        trimmed_value = value.strip()
        reserved_usernames = {"admin", "root", "system", "superuser", "administrator"}
        if trimmed_value.lower() in reserved_usernames:
            raise ValueError(f"The username '{trimmed_value}' is reserved and cannot be used.")
        return trimmed_value


class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )


class UserUpdate(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_-]+$",
    )

    @field_validator("username")
    @classmethod
    def sanitize_and_validate_username(cls, value: str) -> str:
        trimmed_value = value.strip()
        reserved_usernames = {"admin", "root", "system", "superuser", "administrator"}
        if trimmed_value.lower() in reserved_usernames:
            raise ValueError(f"The username '{trimmed_value}' is reserved and cannot be used.")
        return trimmed_value


class ChangePasswordRequest(BaseModel):
    old_password: str = Field(..., min_length=8, max_length=128)
    new_password: str = Field(..., min_length=8, max_length=128)

    @model_validator(mode="after")
    def validate_passwords_differ(self) -> ChangePasswordRequest:
        if self.old_password == self.new_password:
            raise ValueError("New password must be different from the old password.")
        return self


class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)