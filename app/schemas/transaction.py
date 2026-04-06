from pydantic import BaseModel, condecimal
from datetime import date
from typing import Optional
from decimal import Decimal
from app.models.transaction import TransactionType


class TransactionCreate(BaseModel):
    amount: condecimal(gt=0, max_digits=12, decimal_places=2)
    type: TransactionType
    category: str
    date: date
    description: Optional[str] = None

class TransactionUpdate(BaseModel):
    amount: condecimal(gt=0, max_digits=12, decimal_places=2) | None = None
    category: str | None = None
    date: date | None = None
    description: str | None = None

class TransactionResponse(BaseModel):
    id:int
    amount: Decimal
    type: TransactionType
    category: str
    date: date
    description: Optional[str] 
    created_by: int
    model_config = {"from_attributes": True}


