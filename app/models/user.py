import enum
from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String

from app.core.database import Base
from app.utils.helper import get_current_time


class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.user)
    created_at = Column(DateTime, default=get_current_time)
