from datetime import datetime

from enum import Enum
from pydantic import BaseModel, EmailStr


class UserRole(str, Enum):
    admin = "admin"
    user = "user"


class UserBase(BaseModel):
    email: EmailStr
    password: str | None = None
    name: str | None = None
    role: UserRole
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    created_at: datetime
