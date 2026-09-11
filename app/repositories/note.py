from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Note


class NoteRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(
        self,
        offset: int,
        limit: int,
        q: str | None = None,
        sort_by: str = "created_at",
        order: str = "asc",
        folder_id: int | None = None,
        user_id: int | None = None,
    ) -> tuple[list[Note], int]:

        query = select(Note)

        if folder_id is not None:
            query = query.where(Note.folder_id == folder_id)

        if user_id is not None:
            query = query.where(Note.user_id == user_id)

        if q:
            query = query.where(
                or_(
                    Note.title.ilike(f"%{q}%"),
                    Note.content.ilike(f"%{q}%"),
                )
            )

        count_query = select(func.count()).select_from(query.subquery())

        total_result = await self.db.execute(count_query)
        total = total_result.scalar_one()

        sort_column = getattr(
            Note,
            sort_by,
            Note.created_at,
        )

        if order.lower() == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

        query = query.offset(offset).limit(limit)

        result = await self.db.execute(query)
        items = list(result.scalars().all())

        return items, total

    async def get_by_id(
        self,
        note_id: int,
        user_id: int | None = None,
    ) -> Note | None:

        statement = select(Note).where(Note.id == note_id)

        if user_id is not None:
            statement = statement.where(Note.user_id == user_id)

        result = await self.db.execute(statement)

        return result.scalar_one_or_none()

    async def create(
        self,
        note: Note,
    ) -> Note:

        self.db.add(note)

        await self.db.commit()
        await self.db.refresh(note)

        return note

    async def update(
        self,
        note: Note,
    ) -> Note:

        await self.db.commit()
        await self.db.refresh(note)

        return note

    async def delete(
        self,
        note: Note,
    ) -> None:

        await self.db.delete(note)

        await self.db.commit()