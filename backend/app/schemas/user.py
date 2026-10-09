from typing import Optional, List
from pydantic import BaseModel, EmailStr
from app.models.user import RoleEnum

class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: RoleEnum = RoleEnum.analista
    manager_id: Optional[int] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[RoleEnum] = None
    manager_id: Optional[int] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleEnum
    manager_id: Optional[int] = None
    manager_name: Optional[str] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None
