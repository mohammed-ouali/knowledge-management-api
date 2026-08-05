from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Comment
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


@router.get("/", response_model=list[CommentResponse])
async def get_comments(db: AsyncSession = Depends(get_db)):
    statement = select(Comment)
    result = await db.execute(statement)

    return result.scalars().all()


@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    statement = select(Comment).where(Comment.id == comment_id)
    result = await db.execute(statement)
    comment = result.scalar_one_or_none()

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    return comment


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CommentResponse)
async def create_comment(data: CommentCreate, db: AsyncSession = Depends(get_db)):
    comment = Comment(
        note_id=data.note_id,
        author_id=data.author_id,
        content=data.content
    )

    db.add(comment)

    await db.commit()
    await db.refresh(comment)

    return comment


@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(comment_id: int, data: CommentUpdate, db: AsyncSession = Depends(get_db)):
    statement = select(Comment).where(Comment.id == comment_id)
    result = await db.execute(statement)
    comment = result.scalar_one_or_none()

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    if data.content is not None:
        comment.content = data.content

    await db.commit()
    await db.refresh(comment)

    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    statement = select(Comment).where(Comment.id == comment_id)
    result = await db.execute(statement)
    comment = result.scalar_one_or_none()

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    await db.delete(comment)
    await db.commit()