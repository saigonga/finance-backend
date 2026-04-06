from sqlalchemy import Column,Integer, String, Numeric,Boolean, Enum, DateTime, Date, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

class TransactionType(str, enum.Enum):
    income = 'income'
    expense = 'expense'

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Numeric(12, 2), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    category = Column(String(100), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(Text, nullable=True)
    is_deleted = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    creator = relationship("User", backref="transactions")

