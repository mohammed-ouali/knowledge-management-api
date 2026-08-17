from __future__ import annotations

from datetime import datetime
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


class CommentBase(BaseModel):
    content: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Comment content must be between 1 and 1000 characters long.",
    )

    @field_validator("content")
    @classmethod
    def validate_and_sanitize_content(cls, value: str) -> str:
        trimmed_value = value.strip()
        if not trimmed_value:
            raise ValueError("Comment content cannot consist solely of whitespace.")
        return trimmed_value


class CommentCreate(CommentBase):
    note_id: int = Field(
        ...,
        gt=0,
        description="ID of the note being commented on. Must be a positive integer.",
    )
    user_id: int = Field(
        ...,
        gt=0,
        description="ID of the user creating the comment. Must be a positive integer.",
    )


class CommentUpdate(BaseModel):
    content: str | None = Field(
        None,
        min_length=1,
        max_length=1000,
        description="Updated comment content must be between 1 and 1000 characters long.",
    )

    @field_validator("content")
    @classmethod
    def validate_and_sanitize_content(cls, value: str | None) -> str | None:
        if value is None:
            return None
        trimmed_value = value.strip()
        if not trimmed_value:
            raise ValueError("Comment content cannot consist solely of whitespace.")
        return trimmed_value

    @model_validator(mode="after")
    def validate_at_least_one_field(self) -> CommentUpdate:
        if self.content is None:
            raise ValueError("Update payload cannot be empty. Updated content must be provided.")
        return self


class CommentResponse(CommentBase):
    id: int
    note_id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)