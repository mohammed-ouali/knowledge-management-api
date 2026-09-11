from typing import Literal

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies.services import get_note_service
from app.api.dependencies.services import get_label_service
from app.api.dependencies.auth import get_current_active_user
from app.models import User
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
    current_user: User = Depends(get_current_active_user),
    service: NoteService = Depends(get_note_service),
):
    return await service.get_all_notes(
        page=page,
        limit=limit,
        q=q,
        sort_by=sort_by,
        order=order,
        folder_id=folder_id,
        user_id=current_user.id,
    )


@router.get(
    "/{note_id}",
    response_model=NoteResponse,
)
async def get_note(
    note_id: int,
    current_user: User = Depends(get_current_active_user),
    service: NoteService = Depends(get_note_service),
):
    return await service.get_note_by_id(note_id=note_id, user_id=current_user.id)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=NoteResponse,
)
async def create_note(
    note_data: NoteCreate,
    current_user: User = Depends(get_current_active_user),
    service: NoteService = Depends(get_note_service),
):
    return await service.create_note(note_data=note_data, user_id=current_user.id)


@router.put(
    "/{note_id}",
    response_model=NoteResponse,
)
async def update_note(
    note_id: int,
    note_data: NoteUpdate,
    current_user: User = Depends(get_current_active_user),
    service: NoteService = Depends(get_note_service),
):
    return await service.update_note(
        note_id=note_id,
        note_data=note_data,
        user_id=current_user.id,
    )


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_active_user),
    service: NoteService = Depends(get_note_service),
):
    await service.delete_note(note_id=note_id, user_id=current_user.id)


@router.get(
    "/{note_id}/labels",
    response_model=list[LabelResponse],
)
async def get_labels(
    note_id: int,
    current_user: User = Depends(get_current_active_user),
    service: LabelService = Depends(get_label_service),
):
    return await service.get_all_labels(note_id=note_id, user_id=current_user.id)


@router.post(
    "/{note_id}/labels",
    status_code=status.HTTP_201_CREATED,
    response_model=LabelResponse,
)
async def create_label(
    note_id: int,
    label_data: LabelCreate,
    current_user: User = Depends(get_current_active_user),
    service: LabelService = Depends(get_label_service),
):
    return await service.create_label(
        note_id=note_id,
        label_data=label_data,
        user_id=current_user.id,
    )


@router.put(
    "/{note_id}/labels/{label_id}",
    response_model=LabelResponse,
)
async def update_label(
    note_id: int,
    label_id: int,
    label_data: LabelUpdate,
    current_user: User = Depends(get_current_active_user),
    service: LabelService = Depends(get_label_service),
):
    return await service.update_label(
        note_id=note_id,
        label_id=label_id,
        label_data=label_data,
        user_id=current_user.id,
    )


@router.delete(
    "/{note_id}/labels/{label_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_label(
    note_id: int,
    label_id: int,
    current_user: User = Depends(get_current_active_user),
    service: LabelService = Depends(get_label_service),
):
    await service.delete_label(
        note_id=note_id,
        label_id=label_id,
        user_id=current_user.id,
    )