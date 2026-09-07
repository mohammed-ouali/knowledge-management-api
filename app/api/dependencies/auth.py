from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.repositories.user import UserRepository
from app.core.exceptions import (
    InvalidTokenException, 
    UserNotFoundException, 
    UserInactiveException,
)
from app.core.security import decode_token
from app.models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), repository: UserRepository = Depends()) -> User:
    payload = decode_token(token=token, expected_type="access")
    user_id = payload.get("sub")
    if not user_id:
        raise InvalidTokenException("Token subject is missing")

    user = await repository.get_by_id(user_id)
    if not user:
        raise UserNotFoundException(f"User with ID {user_id} not found")
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise UserInactiveException("User account is inactive or disabled")
    return current_user