from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api.dependencies import get_db, get_current_user
from app.schemas.user import UserResponse
from app.models.user import User

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
async def read_users(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get all users. In a real scenario, protect this with an Admin role check."""
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users
