from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import require_roles
from app.models.user import UserRole
from app.services import dashboard_service


router = APIRouter()

@router.get("/summary")
def get_summary(
    db:Session = Depends(get_db),
    current_user = Depends(require_roles(UserRole.analyst, UserRole.admin))
    ):
    return  dashboard_service.get_summary(db)