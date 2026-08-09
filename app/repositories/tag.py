from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Tag


class TagRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Tag]:
        statement = select(Tag)
        result = await self.db.execute(statement)
        return list(result.scalars().all())

    async def get_by_id(self, tag_id: int) -> Tag | None:
        statement = select(Tag).where(Tag.id == tag_id)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Tag | None:
        statement = select(Tag).where(Tag.name == name)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()

    async def create(self, tag: Tag) -> Tag:
        self.db.add(tag)
        await self.db.commit()
        await self.db.refresh(tag)
        return tag

    async def update(self, tag: Tag) -> Tag:
        await self.db.commit()
        await self.db.refresh(tag)
        return tag

    async def delete(self, tag: Tag) -> None:
        await self.db.delete(tag)
        await self.db.commit()