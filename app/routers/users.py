from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    repository = UserRepository(db)
    return UserService(repository)


@router.get("/", response_model=list[UserResponse])
async def get_users(service: UserService = Depends(get_user_service)):
    return await service.get_all_users()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int, 
    service: UserService = Depends(get_user_service)
):
    return await service.get_user_by_id(user_id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)
async def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service)
):
    return await service.create_user(user_data)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    service: UserService = Depends(get_user_service)
):
    return await service.update_user(user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    await service.delete_user(user_id)