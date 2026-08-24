from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Label(Base):
    __tablename__ = "labels"

    __table_args__ = (
        UniqueConstraint(
            "note_id",
            "name",
            name="uq_note_label_name",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    note_id: Mapped[int] = mapped_column(
        ForeignKey("notes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    note: Mapped["Note"] = relationship(
        back_populates="labels",
    )