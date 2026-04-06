from pydantic import BaseModel
from typing import List


class CategorySummary(BaseModel):
    category: str
    total: float

class DashboardSummary(BaseModel):
    total_income: float
    total_expenses:float
    net_balance: float
    category_totals: List[CategorySummary]