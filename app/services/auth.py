from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)
from app.core.exceptions import(
    UserInactiveException,
    InvalidCredentialsException,
    InvalidTokenException
)
from app.schemas.auth import Token
from app.schemas.user import UserCreate
from app.services.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.service = user_service

    @staticmethod
    def _generate_tokens(user_id: str) -> Token: #private method
        return Token(
            access_token=create_access_token(subject=user_id),
            refresh_token=create_refresh_token(subject=user_id),
            type="bearer"
        )

    async def register_user(self, user_data: UserCreate) -> Token:
        user = await self.service.create_user(user_data=user_data)
        return self._generate_tokens(user_id=str(user.id))

    async def authenticate_user(self, email: str, password: str):
        user = await self.service.repository.get_by_email(email=email)
        if not user or not verify_password(plain_password=password, hashed_password=user.password_hash):
            raise InvalidCredentialsException("Invalid email or password")
        if not user.is_active:
            raise UserInactiveException("User account is inactive or disabled")
        return user

    async def login_user(self, email: str, password: str):
        user = await self.authenticate_user(email=email, password=password)
        return self._generate_tokens(user_id=str(user.id))

    async def refresh_tokens(self, refresh_token: str) -> Token:
        payload = decode_token(token=refresh_token, expected_type="refresh")
        user_id = payload.get("sub")
        if not user_id:
            raise InvalidTokenException("Invalid refresh token payload")

        user = await self.service.get_user_by_id(user_id=int(user_id))
        if not user.is_active:
            raise UserInactiveException("User account is inactive or disabled")

        return self._generate_tokens(user_id=str(user.id))