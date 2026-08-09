from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Folder

class FolderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_by_user(self, user_id: int) -> list[Folder]:
        statement = select(Folder).where(Folder.user_id == user_id)
        result = await self.db.execute(statement)
        return list(result.scalars().all())

    async def get_by_id(self, folder_id: int) -> Folder | None:
        statement = select(Folder).where(Folder.id == folder_id)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_name_and_user(self, user_id: int, folder_name: str) -> Folder | None:
        statement = (select(Folder).where(Folder.user_id == user_id).where(Folder.name == folder_name))
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()

    async def create(self, folder: Folder) -> Folder:
        self.db.add(folder)
        await self.db.commit()
        await self.db.refresh(folder)
        return folder

    async def update(self, folder: Folder) -> Folder:
        await self.db.commit()
        await self.db.refresh(folder)
        return folder

    async def delete(self, folder: Folder) -> None:
            await self.db.delete(folder)
            await self.db.commit()