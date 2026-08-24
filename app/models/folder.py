from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Folder(Base):
    __tablename__ = "folders"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )

    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("folders.id", ondelete="CASCADE"),
        index=True,
    )

    name: Mapped[str] = mapped_column(String(100))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    user: Mapped["User"] = relationship(
        back_populates="folders",
    )

    parent_folder: Mapped[Optional["Folder"]] = relationship(
        back_populates="subfolders",
        remote_side="Folder.id",
    )

    subfolders: Mapped[list["Folder"]] = relationship(
        back_populates="parent_folder",
        cascade="all, delete-orphan",
    )

    notes: Mapped[list["Note"]] = relationship(
        back_populates="folder",
        cascade="all, delete-orphan",
    )