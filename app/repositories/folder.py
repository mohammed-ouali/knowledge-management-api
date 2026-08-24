from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Folder, Note


class FolderRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(
        self,
        offset: int,
        limit: int,
        q: str | None = None,
        sort_by: str = "created_at",
        order: str = "asc",
        user_id: int | None = None,
    ) -> tuple[list[Folder], int]:

        query = select(Folder)

        if user_id is not None:
            query = query.where(Folder.user_id == user_id)

        if q:
            query = query.where(
                Folder.name.ilike(f"%{q}%")
            )

        count_query = select(func.count()).select_from(
            query.subquery()
        )

        total_result = await self.db.execute(count_query)
        total = total_result.scalar_one()

        sort_column = getattr(
            Folder,
            sort_by,
            Folder.created_at,
        )

        if order.lower() == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

        query = query.offset(offset).limit(limit)

        result = await self.db.execute(query)
        folders = list(result.scalars().all())

        return folders, total

    async def get_by_id(
        self,
        folder_id: int,
    ) -> Folder | None:

        statement = select(Folder).where(
            Folder.id == folder_id
        )

        result = await self.db.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_name_and_parent(
        self,
        user_id: int,
        name: str,
        parent_id: int | None,
    ) -> Folder | None:

        statement = (
            select(Folder)
            .where(Folder.user_id == user_id)
            .where(Folder.name == name)
            .where(Folder.parent_id == parent_id)
        )

        result = await self.db.execute(statement)

        return result.scalar_one_or_none()

    async def get_children(
        self,
        parent_id: int,
        user_id: int,
    ) -> list[Folder]:

        statement = (
            select(Folder)
            .where(Folder.parent_id == parent_id)
            .where(Folder.user_id == user_id)
            .order_by(Folder.name.asc())
        )

        result = await self.db.execute(statement)

        return list(result.scalars().all())

    async def get_notes(
        self,
        folder_id: int,
        user_id: int,
        offset: int,
        limit: int,
    ) -> tuple[list[Note], int]:

        query = (
            select(Note)
            .where(Note.folder_id == folder_id)
            .where(Note.user_id == user_id)
        )

        count_query = select(func.count()).select_from(
            query.subquery()
        )

        total_result = await self.db.execute(count_query)
        total = total_result.scalar_one()

        query = (
            query
            .order_by(Note.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        result = await self.db.execute(query)
        notes = list(result.scalars().all())

        return notes, total

    async def create(
        self,
        folder: Folder,
    ) -> Folder:

        self.db.add(folder)

        await self.db.commit()
        await self.db.refresh(folder)

        return folder

    async def update(
        self,
        folder: Folder,
    ) -> Folder:

        await self.db.commit()
        await self.db.refresh(folder)

        return folder

    async def delete(
        self,
        folder: Folder,
    ) -> None:

        await self.db.delete(folder)

        await self.db.commit()