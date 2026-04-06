from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password


def get_user_by_email(db:Session, email:str) ->User:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db:Session, user_id:int) ->User:
    return db.query(User).filter(User.id == user_id ).first()

def get_all_users(db:Session)-> list[User]:
    return db.query(User).all()

def create_user(db:Session, data: UserCreate)-> User:
    user = User(
        email= data.email,
        full_name= data.full_name,
        hashed_password = hash_password(data.password),
        role= data.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db:Session, user: User, data: UserUpdate)-> User:
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(user,field,value)
    db.commit()
    db.refresh(user)
    return user 

def delete_user(db:Session, user: User):
    db.delete(user)
    db.commit()

