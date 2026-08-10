from app.core.exceptions import CommentNotFoundException
from app.models import Comment
from app.repositories.comment import CommentRepository
from app.schemas.comment import CommentCreate, CommentUpdate


class CommentService:
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    async def get_all_comments_by_note(self, note_id: int) -> list[Comment]:
        return await self.repository.get_all_by_note(note_id)

    async def get_all_comments_by_author(self, author_id: int) -> list[Comment]:
        return await self.repository.get_all_by_author(author_id)

    async def get_comment_by_id(self, comment_id: int) -> Comment:
        comment = await self.repository.get_by_id(comment_id)
        if comment is None:
            raise CommentNotFoundException(f"Comment with ID {comment_id} not found")
        return comment

    async def create_comment(self, comment_data: CommentCreate) -> Comment:
        comment = Comment(
            content=comment_data.content,
            note_id=comment_data.note_id,
            author_id=comment_data.author_id,
        )
        return await self.repository.create(comment)

    async def update_comment(self, comment_id: int, comment_data: CommentUpdate) -> Comment:
        comment = await self.get_comment_by_id(comment_id)

        if comment_data.content is not None:
            comment.content = comment_data.content

        return await self.repository.update(comment)

    async def delete_comment(self, comment_id: int) -> None:
        comment = await self.get_comment_by_id(comment_id)
        await self.repository.delete(comment)