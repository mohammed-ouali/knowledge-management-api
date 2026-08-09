from sqlalchemy import Table, Column, ForeignKey

from app.core.database import Base

note_tag = Table(
    "note_tag",
    Base.metadata,

    Column(
        "note_id",
        ForeignKey("notes.id"),
        primary_key=True
    ),

    Column(
        "tag_id",
        ForeignKey("tags.id"),
        primary_key=True
    ),
)