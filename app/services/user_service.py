from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories import user_repository
from app.schemas.user import UserCreate, userUpdate


def get_all_users(db:Session):
    return user_repository.get_all_users(db)

def get_user(db:Session, user_id:int):
    user = user_repository.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found ")
    return user

def create_user(db:Session, data:UserCreate):
    if user_repository.get_user_by_email(db,data.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return user_repository.create_user(db, data)

def update_user(db:Session, user_id:int, data: userUpdate):
    user= get_user(db, user_id)
    return user_repository.update_user(db, user, data)

def delete_user(db:Session, user_id:int):
    user=  get_user(db, user_id)
    user_repository.delete_user(db, user)

