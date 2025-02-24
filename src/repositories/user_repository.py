from typing import Optional
from ..database import DatabasePool
from ..schemas.user_schema import UserCreate, UserResponse

class UserRepository:
    @staticmethod
    async def create(user: UserCreate) -> UserResponse:
        with DatabasePool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (email, name) VALUES (%s, %s) RETURNING id, email, name",
                (user.email, user.name)
            )
            result = cursor.fetchone()
            return UserResponse(id=result[0], email=result[1], name=result[2])

    @staticmethod
    async def get_by_id(user_id: int) -> Optional[UserResponse]:
        with DatabasePool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, email, name FROM users WHERE id = %s",
                (user_id,)
            )
            result = cursor.fetchone()
            return UserResponse(id=result[0], email=result[1], name=result[2]) if result else None 