from __future__ import annotations

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


class TagBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Tag name must be between 1 and 50 characters long.",
    )

    @field_validator("name")
    @classmethod
    def validate_and_sanitize_name(cls, value: str) -> str:
        # Strip spaces and convert to lowercase for uniform tag indexing
        trimmed_value = value.strip().lower()
        if not trimmed_value:
            raise ValueError("Tag name cannot consist solely of whitespace.")
        return trimmed_value


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: str | None = Field(
        None,
        min_length=1,
        max_length=50,
        description="Updated tag name must be between 1 and 50 characters long.",
    )

    @field_validator("name")
    @classmethod
    def validate_and_sanitize_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        trimmed_value = value.strip().lower()
        if not trimmed_value:
            raise ValueError("Tag name cannot consist solely of whitespace.")
        return trimmed_value

    @model_validator(mode="after")
    def validate_at_least_one_field(self) -> TagUpdate:
        if self.name is None:
            raise ValueError("Update payload cannot be empty. A new tag name must be provided.")
        return self


class TagResponse(TagBase):
    id: int

    model_config = ConfigDict(from_attributes=True)