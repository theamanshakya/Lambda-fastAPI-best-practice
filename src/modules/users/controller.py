from fastapi import APIRouter, Depends, HTTPException
from .schema import UserCreate, UserResponse
from .service import UserService
from typing import List

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, service: UserService = Depends()):
    return await service.create_user(user)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, service: UserService = Depends()):
    return await service.get_user(user_id)

@router.get("/", response_model=List[UserResponse])
async def list_users(skip: int = 0, limit: int = 10, service: UserService = Depends()):
    return await service.list_users(skip, limit) 