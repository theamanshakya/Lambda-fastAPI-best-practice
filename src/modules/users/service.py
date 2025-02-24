from .repository import UserRepository
from .schema import UserCreate, UserResponse
from src.core.exceptions import CustomHTTPException
from typing import List

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    async def create_user(self, user: UserCreate) -> UserResponse:
        try:
            return await self.repository.create(user)
        except Exception as e:
            raise CustomHTTPException(
                status_code=500,
                detail="Failed to create user",
                error_code="USER_CREATE_ERROR",
                extra={"original_error": str(e)}
            )

    async def get_user(self, user_id: int) -> UserResponse:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise CustomHTTPException(
                status_code=404,
                detail="User not found",
                error_code="USER_NOT_FOUND"
            )
        return user

    async def list_users(self, skip: int = 0, limit: int = 10) -> List[UserResponse]:
        return await self.repository.list(skip, limit) 