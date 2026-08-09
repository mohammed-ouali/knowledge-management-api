from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Comment


class CommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_by_note(self, note_id: int) -> list[Comment]:
        statement = select(Comment).where(Comment.note_id == note_id)
        result = await self.db.execute(statement)
        return list(result.scalars().all())

    async def get_all_by_author(self, author_id: int) -> list[Comment]:
        statement = select(Comment).where(Comment.author_id == author_id)
        result = await self.db.execute(statement)
        return list(result.scalars().all())

    async def get_by_id(self, comment_id: int) -> Comment | None:
        statement = select(Comment).where(Comment.id == comment_id)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()

    async def create(self, comment: Comment) -> Comment:
        self.db.add(comment)
        await self.db.commit()
        await self.db.refresh(comment)
        return comment

    async def update(self, comment: Comment) -> Comment:
        await self.db.commit()
        await self.db.refresh(comment)
        return comment

    async def delete(self, comment: Comment) -> None:
        await self.db.delete(comment)
        await self.db.commit()