from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserBase, UserOut

router = APIRouter()


@router.get("/", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()


# Update user endpoint (partial update)
@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: str, user_in: UserBase, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.hashed_password = (get_password_hash(user_in.password),)
    user.email = user_in.email
    user.name = user_in.name
    user.role = user_in.role
    user.is_active = user_in.is_active
    db.commit()
    db.refresh(user)
    return user
