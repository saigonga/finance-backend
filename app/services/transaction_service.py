from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date
from typing import Optional
from app.repositories import transaction_repository
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.models.transaction import TransactionType

def get_all(db:Session, type:Optional[TransactionType]= None,
            category:Optional[str]= None,
            from_date: Optional[date] =None,
            to_date: Optional[date] = None):
    return transaction_repository.get_all(db, type, category, from_date, to_date)

def get_one(db:Session, transaction_id: int):
    t= transaction_repository.get_by_id(db, transaction_id)
    if not t:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return t

def create(db:Session, data:TransactionCreate, user_id:int):
    return transaction_repository.create(db, data, user_id)

def update(db:Session, transaction_id:int, data: TransactionUpdate):
    t= get_one(db, transaction_id)
    return transaction_repository.update(db,t,data)

def delete(db:Session, transaction_id:int):
    t= get_one(db, transaction_id)
    transaction_repository.soft_delete(db,t)