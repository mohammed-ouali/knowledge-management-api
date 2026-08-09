from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Note


class NoteRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_by_folder(self, folder_id: int) -> list[Note]:
        statement = select(Note).where(Note.folder_id == folder_id)
        result = await self.db.execute(statement)
        return list(result.scalars().all())

    async def get_all_by_author(self, author_id: int) -> list[Note]:
        statement = select(Note).where(Note.author_id == author_id)
        result = await self.db.execute(statement)
        return list(result.scalars().all())

    async def get_by_id(self, note_id: int) -> Note | None:
        statement = select(Note).where(Note.id == note_id)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()

    async def create(self, note: Note) -> Note:
        self.db.add(note)
        await self.db.commit()
        await self.db.refresh(note)
        return note

    async def update(self, note: Note) -> Note:
        await self.db.commit()
        await self.db.refresh(note)
        return note

    async def delete(self, note: Note) -> None:
        await self.db.delete(note)
        await self.db.commit()