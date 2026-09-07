from app.models import User
from app.core.security import get_password_hash
from app.repositories.user import UserRepository
from app.schemas.pagination import PaginatedResponse
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.core.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
)


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_all_users(
        self,
        page: int = 1,
        limit: int = 10,
        q: str | None = None,
        sort_by: str = "username",
        order: str = "asc",
    ) -> PaginatedResponse[UserResponse]:

        offset = (page - 1) * limit

        items, total = await self.repository.get_all(
            offset=offset,
            limit=limit,
            q=q,
            sort_by=sort_by,
            order=order,
        )

        return PaginatedResponse[UserResponse](
            items=items,
            total=total,
            page=page,
            limit=limit,
        )

    async def get_user_by_id(
        self,
        user_id: int,
    ) -> User:

        user = await self.repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundException(
                f"User with ID {user_id} not found"
            )

        return user

    async def create_user(
        self,
        user_data: UserCreate,
    ) -> User:

        if await self.repository.get_by_email(user_data.email):
            raise UserAlreadyExistsException(
                "Email is already registered"
            )

        if await self.repository.get_by_username(user_data.username):
            raise UserAlreadyExistsException(
                "Username is already taken"
            )

        user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=get_password_hash(user_data.password),
            is_active=True
        )

        return await self.repository.create(user)

    async def update_user(
        self,
        user_id: int,
        user_data: UserUpdate,
    ) -> User:

        user = await self.get_user_by_id(user_id)

        if (
            user_data.username is not None
            and user_data.username != user.username
        ):
            if await self.repository.get_by_username(
                user_data.username
            ):
                raise UserAlreadyExistsException(
                    "Username is already taken"
                )

            user.username = user_data.username

        if (
            user_data.email is not None
            and user_data.email != user.email
        ):
            if await self.repository.get_by_email(
                user_data.email
            ):
                raise UserAlreadyExistsException(
                    "Email is already registered"
                )

            user.email = user_data.email

        if user_data.password is not None:
            user.password_hash = user_data.password

        return await self.repository.update(user)

    async def delete_user(
        self,
        user_id: int,
    ) -> None:

        user = await self.get_user_by_id(user_id)

        await self.repository.delete(user)