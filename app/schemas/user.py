from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_verified: bool
    status: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserLogin(UserBase):
    password: str
