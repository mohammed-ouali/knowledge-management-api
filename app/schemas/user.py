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
        description="Username must be 3-50 characters containing only letters, numbers, underscores, or hyphens.",
    )
    email: EmailStr = Field(..., description="Valid RFC 5322 compliant email address.")

    @field_validator("username")
    @classmethod
    def sanitize_and_validate_username(cls, value: str) -> str:
        trimmed_value = value.strip()
        reserved_usernames = {"admin", "root", "system", "superuser", "administrator"}
        if trimmed_value.lower() in reserved_usernames:
            raise ValueError(f"The username '{trimmed_value}' is reserved and cannot be registered.")
        return trimmed_value


class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Password must be between 8 and 128 characters long.",
    )


class UserUpdate(BaseModel):
    username: str | None = Field(
        None,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_-]+$",
    )
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=8, max_length=128)

    @field_validator("username")
    @classmethod
    def sanitize_and_validate_username(cls, value: str | None) -> str | None:
        if value is None:
            return None
        trimmed_value = value.strip()
        reserved_usernames = {"admin", "root", "system", "superuser", "administrator"}
        if trimmed_value.lower() in reserved_usernames:
            raise ValueError(f"The username '{trimmed_value}' is reserved and cannot be registered.")
        return trimmed_value

    @model_validator(mode="after")
    def validate_at_least_one_field(self) -> "UserUpdate":
        if not any([
            self.username is not None,
            self.email is not None,
            self.password is not None,
        ]):
            raise ValueError("Update payload cannot be empty. At least one field must be provided.")
        return self


class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)