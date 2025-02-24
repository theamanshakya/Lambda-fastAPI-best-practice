from src.database import DatabasePool
from .schema import UserCreate, UserResponse
from .queries import USER_QUERIES
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class UserRepository:
    async def create(self, user: UserCreate) -> UserResponse:
        with DatabasePool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                USER_QUERIES["create_user"],
                (user.email, user.name)
            )
            result = cursor.fetchone()
            return UserResponse(**result)

    async def get_by_id(self, user_id: int) -> Optional[UserResponse]:
        with DatabasePool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(USER_QUERIES["get_user_by_id"], (user_id,))
            result = cursor.fetchone()
            return UserResponse(**result) if result else None

    async def list(self, skip: int = 0, limit: int = 10) -> List[UserResponse]:
        with DatabasePool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(USER_QUERIES["list_users"], (limit, skip))
            results = cursor.fetchall()
            return [UserResponse(**row) for row in results] 