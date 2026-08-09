from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.comment import CommentRepository
from app.schemas.comment import CommentCreate, CommentResponse, CommentUpdate
from app.services.comment import CommentService

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


def get_comment_service(db: AsyncSession = Depends(get_db)) -> CommentService:
    repository = CommentRepository(db)
    return CommentService(repository)


@router.get("/", response_model=list[CommentResponse])
async def get_comments(
    note_id: int | None = None,
    author_id: int | None = None,
    service: CommentService = Depends(get_comment_service)
):
    if note_id is not None:
        return await service.get_all_comments_by_note(note_id)
    if author_id is not None:
        return await service.get_all_comments_by_author(author_id)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Must provide either note_id or author_id as a query parameter"
    )


@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment(
    comment_id: int,
    service: CommentService = Depends(get_comment_service)
):
    return await service.get_comment_by_id(comment_id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CommentResponse
)
async def create_comment(
    comment_data: CommentCreate,
    service: CommentService = Depends(get_comment_service)
):
    return await service.create_comment(comment_data)


@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    service: CommentService = Depends(get_comment_service)
):
    return await service.update_comment(comment_id, comment_data)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    service: CommentService = Depends(get_comment_service)
):
    await service.delete_comment(comment_id)