from fastapi import Depends, status, APIRouter

from app.api.dependencies import get_db

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import LoginRequest, RefreshTokenRequest, Token
from app.schemas.user import UserCreate
from app.services.user import UserService
from app.services.auth import AuthService
from app.repositories.user import UserRepository

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

def get_auth_service(
    db: AsyncSession = Depends(get_db),
) -> AuthService:
    user_repository = UserRepository(db)
    user_service = UserService(repository=user_repository)
    return AuthService(user_service=user_service)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=Token,
)
async def register(
    user_data: UserCreate,
    service: AuthService = Depends(get_auth_service),
):
    return await service.register_user(user_data)


@router.post(
    "/login",
    response_model=Token,
)
async def login(
    credentials: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    return await service.login_user(
        email=credentials.email,
        password=credentials.password,
    )


@router.post(
    "/refresh",
    response_model=Token,
)
async def refresh_token(
    body: RefreshTokenRequest,
    service: AuthService = Depends(get_auth_service),
):
    return await service.refresh_tokens(body.refresh_token)