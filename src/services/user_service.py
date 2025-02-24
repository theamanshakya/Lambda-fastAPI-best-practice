from ..repositories.user_repository import UserRepository
from ..schemas.user_schema import UserCreate, UserResponse
from ..core.exceptions import CustomHTTPException

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