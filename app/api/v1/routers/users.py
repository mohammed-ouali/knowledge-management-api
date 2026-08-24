from typing import Literal

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.user import UserRepository
from app.schemas.pagination import PaginatedResponse
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


def get_user_service(
    db: AsyncSession = Depends(get_db),
) -> UserService:

    repository = UserRepository(db)

    return UserService(repository)


@router.get(
    "",
    response_model=PaginatedResponse[UserResponse],
)
async def get_users(
    page: int = Query(
        default=1,
        ge=1,
        description="Page number",
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Items per page",
    ),
    q: str | None = Query(
        default=None,
        description="Search by username",
    ),
    sort_by: Literal["username", "created_at"] = Query(
        default="username",
        description="Field to sort by",
    ),
    order: Literal["asc", "desc"] = Query(
        default="asc",
        description="Sorting direction",
    ),
    service: UserService = Depends(get_user_service),
):
    return await service.get_all_users(
        page=page,
        limit=limit,
        q=q,
        sort_by=sort_by,
        order=order,
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    return await service.get_user_by_id(user_id)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service),
):
    return await service.create_user(user_data)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    service: UserService = Depends(get_user_service),
):
    return await service.update_user(
        user_id,
        user_data,
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    await service.delete_user(user_id)