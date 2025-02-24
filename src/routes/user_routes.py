from fastapi import APIRouter, HTTPException
from ..schemas.user_schema import UserCreate, UserResponse
from ..services.user_service import UserService

router = APIRouter()

@router.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate):
    return await UserService.create_user(user)

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    user = await UserService.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user 