from datetime import datetime, timezone

from sqlalchemy import Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    note_id: Mapped[int] = mapped_column(
        ForeignKey("notes.id"),
        nullable=False,
        index=True
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    note: Mapped["Note"] = relationship(
        back_populates="comments"
    )

    author: Mapped["User"] = relationship(
        back_populates="comments"
    )