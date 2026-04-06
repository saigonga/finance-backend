from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date
from typing import Optional
from app.models.transaction import Transaction, TransactionType
from app.schemas.transaction import TransactionCreate, TransactionUpdate


def get_all(db:Session, type:Optional[TransactionType]= None,
            category:Optional[str]= None,
            from_date: Optional[date] =None,
            to_date: Optional[date] = None)-> list[Transaction]:
    
    query = db.query(Transaction).filter(Transaction.is_deleted == False)

    if type:
        query = query.filter(Transaction.type == type)
    if category:
        query = query.filter(Transaction.category == category)
    if from_date:
        query = query.filter(Transaction.date >= from_date)
    if to_date:
        query=  query.filter(Transaction.date <= to_date)

    return query.order_by(Transaction.date.desc()).all()

def get_by_id(db:Session, transaction_id:int)-> Transaction:
    return db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.is_deleted == False
    ).first()

def create(db:Session, data: TransactionCreate, user_id: int)-> Transaction:
    transaction = Transaction(**data.model_dump(), created_by = user_id)
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

def update(db:Session, data: TransactionUpdate, transaction:Transaction) -> Transaction:
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(field,value,transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

def soft_delete(db:Session, transaction:Transaction):
    transaction.is_deleted = True
    db.commit()


