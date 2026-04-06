from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.transaction import Transaction, TransactionType


def get_summary(db:Session):
    rows = db.query(Transaction).filter(Transaction.is_deleted == False).all()
    total_income = sum(float(r.amount)for r in rows if r.type == TransactionType.income)
    total_expense = sum(float(r.amount) for r in rows if r.type == TransactionType.expense)

    category_map ={}

    for r in rows: 
        category_map[r.category] = category_map.get(r.category,0 )+ float(r.amount)

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": total_income - total_expense,
        "category_totals": [{"category":k, "total":v}for k, v in category_map.items()]

        
    }