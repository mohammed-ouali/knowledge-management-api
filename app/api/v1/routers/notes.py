from typing import Literal

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.repositories.folder import FolderRepository
from app.repositories.label import LabelRepository
from app.repositories.note import NoteRepository

from app.schemas.label import (
    LabelCreate,
    LabelResponse,
    LabelUpdate,
)
from app.schemas.note import (
    NoteCreate,
    NoteResponse,
    NoteUpdate,
)
from app.schemas.pagination import PaginatedResponse

from app.services.label import LabelService
from app.services.note import NoteService


router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


def get_note_service(
    db: AsyncSession = Depends(get_db),
) -> NoteService:
    repository = NoteRepository(db)
    folder_repository = FolderRepository(db)

    return NoteService(
        repository=repository,
        folder_repository=folder_repository,
    )


def get_label_service(
    db: AsyncSession = Depends(get_db),
) -> LabelService:
    repository = LabelRepository(db)

    return LabelService(repository)


@router.get(
    "",
    response_model=PaginatedResponse[NoteResponse],
)
async def get_notes(
    page: int = Query(
        default=1,
        ge=1,
        description="Page number",
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Items per page",
    ),
    q: str | None = Query(
        default=None,
        description="Search by title or content",
    ),
    sort_by: Literal["created_at", "updated_at"] = Query(
        default="created_at",
        description="Field to sort by",
    ),
    order: Literal["asc", "desc"] = Query(
        default="asc",
        description="Sorting direction",
    ),
    folder_id: int | None = Query(
        default=None,
        description="Filter by folder ID",
    ),
    user_id: int | None = Query(
        default=None,
        description="Filter by user ID",
    ),
    service: NoteService = Depends(get_note_service),
):
    return await service.get_all_notes(
        page=page,
        limit=limit,
        q=q,
        sort_by=sort_by,
        order=order,
        folder_id=folder_id,
        user_id=user_id,
    )


@router.get(
    "/{note_id}",
    response_model=NoteResponse,
)
async def get_note(
    note_id: int,
    service: NoteService = Depends(get_note_service),
):
    return await service.get_note_by_id(note_id)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=NoteResponse,
)
async def create_note(
    note_data: NoteCreate,
    service: NoteService = Depends(get_note_service),
):
    return await service.create_note(note_data)


@router.put(
    "/{note_id}",
    response_model=NoteResponse,
)
async def update_note(
    note_id: int,
    note_data: NoteUpdate,
    service: NoteService = Depends(get_note_service),
):
    return await service.update_note(
        note_id,
        note_data,
    )


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_note(
    note_id: int,
    service: NoteService = Depends(get_note_service),
):
    await service.delete_note(note_id)


@router.get(
    "/{note_id}/labels",
    response_model=list[LabelResponse],
)
async def get_labels(
    note_id: int,
    service: LabelService = Depends(get_label_service),
):
    return await service.get_all_labels(note_id)


@router.post(
    "/{note_id}/labels",
    status_code=status.HTTP_201_CREATED,
    response_model=LabelResponse,
)
async def create_label(
    note_id: int,
    label_data: LabelCreate,
    service: LabelService = Depends(get_label_service),
):
    return await service.create_label(
        note_id,
        label_data,
    )


@router.put(
    "/{note_id}/labels/{label_id}",
    response_model=LabelResponse,
)
async def update_label(
    note_id: int,
    label_id: int,
    label_data: LabelUpdate,
    service: LabelService = Depends(get_label_service),
):
    return await service.update_label(
        note_id,
        label_id,
        label_data,
    )


@router.delete(
    "/{note_id}/labels/{label_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_label(
    note_id: int,
    label_id: int,
    service: LabelService = Depends(get_label_service),
):
    await service.delete_label(
        note_id,
        label_id,
    )