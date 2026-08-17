from __future__ import annotations

from datetime import datetime

from pydantic import ( 
    BaseModel, 
    ConfigDict, 
    Field,
    field_validator,
    model_validator
    )


class NoteBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Note title must be between 1 and 255 characters long."
    )

    content: str | None = Field(
        None, 
        description="Optional detailed content or body of the note."
    )

    @field_validator("title")
    @classmethod
    def validate_and_sanitize_title(cls, value : str) -> str:
        trimmed_value = value.strip()
        if not trimmed_value:
            raise ValueError("Note title can not consist only of whitespaces")
        return trimmed_value

    @field_validator("content")
    @classmethod
    def sanitize_content(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip()



class NoteCreate(NoteBase):
    folder_id: int | None = Field(
        None,
        gt=0,
        description="Optional folder ID to organize the note. Must be a positive integer if provided.",
    )
    user_id: int = Field(
        ...,
        gt=0,
        description="ID of the user who owns this note. Must be a positive integer.",
    )


class NoteUpdate(BaseModel):
    title: str | None = Field(
        None,
        min_length=1,
        max_length=255,
        description="Updated note title must be between 1 and 255 characters long.",
    )
    content: str | None = Field(
        None,
        description="Updated content or body of the note.",
    )
    folder_id: int | None = Field(
        None,
        gt=0,
        description="Updated folder ID or None to remove the note from a folder.",
    )

    @field_validator("title")
    @classmethod
    def validate_and_sanitize_title(cls, value: str | None) -> str | None:
        if value is None:
            return None
        trimmed_value = value.strip()
        if not trimmed_value:
            raise ValueError("Note title cannot consist only of whitespace.")
        return trimmed_value

    @field_validator("content")
    @classmethod
    def sanitize_content(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip()

    @model_validator(mode="after")
    def validate_at_least_one_field(self) -> "NoteUpdate":
        if not any([
            self.title is not None,
            self.content is not None,
            self.folder_id is not None
        ]):
            raise ValueError("Update payload cannot be empty. At least one field must be provided.")
        return self


class NoteResponse(NoteBase):
    id: int
    user_id: int
    folder_id: int | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)