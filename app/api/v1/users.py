from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import require_roles
from app.models.user import UserRole
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services import user_service
from typing import List


router = APIRouter()
admin_only = Depends(require_roles(UserRole.admin))

@router.get("/", response_model=List[UserResponse], dependencies=[admin_only])
def get_users(db:Session = Depends(get_db)):
    return user_service.get_all_users(db)

@router.post("/",response_model=UserResponse, dependencies=[admin_only])
def create_user(data:UserCreate, db:Session = Depends(get_db)):
    return user_service.create_user(db,data)

@router.get("/{user_id}", response_model=UserResponse, dependencies=[admin_only])
def get_user(user_id:int, db:Session = Depends(get_db)):
    return user_service.get_user(db, user_id)

@router.patch("/{user_id}", response_model=UserResponse, dependencies=[admin_only])
def update_user(user_id:int, data:UserUpdate, db:Session = Depends(get_db)):
    return user_service.update_user(db, user_id, data)


@router.delete("/{user_id}", status_code=204, dependencies=[admin_only])
def delete_user(user_id:int, db:Session = Depends(get_db)):
    user_service.delete_user(db, user_id)
    return {"message": "User Deleted"}


