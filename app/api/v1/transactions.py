from fastapi import APIRouter, Depends , Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.core.database import get_db
from app.core.dependencies import get_current_user, require_roles
from app.models.user import UserRole, User
from app.models.transaction import TransactionType
from app.schemas.transaction import TransactionCreate, TransactionResponse, TransactionUpdate
from app.services import transaction_service


router = APIRouter()

@router.get("/", response_model=List[TransactionResponse])
def get_transactions(
    type :Optional[TransactionType] = Query(None),
    category : Optional[str] = Query(None),
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.viewer,UserRole.analyst,UserRole.admin))
    
):
    return transaction_service.get_all(db, type, category, from_date, to_date)

@router.post("/", response_model=TransactionResponse)
def create_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin))
):
    return transaction_service.create(db, data, current_user.id)

@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.viewer,UserRole.analyst,UserRole.admin))):
    return transaction_service.get_one(db, transaction_id)


@router.patch("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: int, 
    data: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin))
):
    return transaction_service.update(db, transaction_id, data)

@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin))
):
    transaction_service.delete(db, transaction_id)
    return {"message": "Transaction Deleted"}

