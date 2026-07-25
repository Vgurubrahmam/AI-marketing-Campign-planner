from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, UnauthorizedError
from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repo import UserRepository
from app.schemas.auth import AuthResponse, RegisterRequest, UserResponse


class AuthService:
    """Handles authentication business logic."""

    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def register(self, data: RegisterRequest) -> AuthResponse:
        # Check if email already exists
        existing = await self.user_repo.get_by_email(data.email)
        if existing:
            raise ConflictError("An account with this email already exists")

        # Create user with hashed password
        hashed = hash_password(data.password)
        user = await self.user_repo.create(
            email=data.email,
            password_hash=hashed,
            full_name=data.full_name,
        )

        # Generate JWT
        token = create_access_token(str(user.id), user.email)

        return AuthResponse(
            user=UserResponse.model_validate(user),
            token=token,
        )

    async def login(self, email: str, password: str) -> AuthResponse:
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise UnauthorizedError("Invalid email or password")

        if not verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid email or password")

        token = create_access_token(str(user.id), user.email)

        return AuthResponse(
            user=UserResponse.model_validate(user),
            token=token,
        )
