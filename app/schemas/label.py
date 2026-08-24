from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class LabelBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Label name must be between 1 and 50 characters long.",
    )

    @field_validator("name")
    @classmethod
    def validate_and_sanitize_name(cls, value: str) -> str:
        trimmed_value = value.strip().lower()

        if not trimmed_value:
            raise ValueError("Label name cannot consist solely of whitespace.")

        return trimmed_value


class LabelCreate(LabelBase):
    pass


class LabelUpdate(BaseModel):
    name: str | None = Field(
        None,
        min_length=1,
        max_length=50,
    )

    @field_validator("name")
    @classmethod
    def validate_and_sanitize_name(cls, value: str | None) -> str | None:
        if value is None:
            return None

        trimmed_value = value.strip().lower()

        if not trimmed_value:
            raise ValueError("Label name cannot consist solely of whitespace.")

        return trimmed_value

    @model_validator(mode="after")
    def validate_at_least_one_field(self) -> LabelUpdate:
        if self.name is None:
            raise ValueError("Update payload cannot be empty.")

        return self


class LabelResponse(LabelBase):
    id: int
    note_id: int

    model_config = ConfigDict(from_attributes=True)