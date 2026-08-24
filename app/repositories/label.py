from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Label


class LabelRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_by_note(self, note_id: int) -> list[Label]:
        statement = select(Label).where(
            Label.note_id == note_id
        )

        result = await self.db.execute(statement)

        return list(result.scalars().all())

    async def get_by_name_and_note(
        self,
        name: str,
        note_id: int,
    ) -> Label | None:
        statement = select(Label).where(
            Label.name == name,
            Label.note_id == note_id,
        )

        result = await self.db.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_id_and_note(
    self,
    label_id: int,
    note_id: int,
) -> Label | None:
        statement = select(Label).where(
            Label.id == label_id,
            Label.note_id == note_id,
        )
    
        result = await self.db.execute(statement)
    
        return result.scalar_one_or_none()

    async def create(self, label: Label) -> Label:
        self.db.add(label)
        await self.db.commit()
        await self.db.refresh(label)
        return label

    async def update(self, label: Label) -> Label:
        await self.db.commit()
        await self.db.refresh(label)
        return label

    async def delete(self, label: Label) -> None:
        await self.db.delete(label)
        await self.db.commit()