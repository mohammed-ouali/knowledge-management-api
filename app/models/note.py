from datetime import datetime, timezone

from sqlalchemy import String, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    folder_id: Mapped[int] = mapped_column(
        ForeignKey("folders.id"),
        nullable=False,
        index=True
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    folder: Mapped["Folder"] = relationship(
        back_populates="notes"
    )

    author: Mapped["User"] = relationship(
        back_populates="notes"
    )

    attachments: Mapped[list["Attachment"]] = relationship(
        back_populates="note"
    )

    comments: Mapped[list["Comment"]] = relationship(
        back_populates="note"
    )

    tags: Mapped[list["Tag"]] = relationship(
        secondary="note_tag",
        back_populates="notes"
    )