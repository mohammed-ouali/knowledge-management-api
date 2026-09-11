from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.exceptions import (
    InvalidTokenException, 
    UserInactiveException,
)
from app.api.dependencies.services import get_user_service
from app.core.security import decode_token
from app.models import User
from app.services.user import UserService

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_service: UserService = Depends(get_user_service), 
) -> User:
    
    payload = decode_token(token=credentials.credentials, expected_type="access")
    
    user_id = payload.get("sub")
    if not user_id:
        raise InvalidTokenException("Token subject is missing")

    user = await user_service.get_user_by_id(int(user_id))
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise UserInactiveException("User account is inactive or disabled")
    return current_user