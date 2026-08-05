from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.department import DepartmentResponse
from app.core.dependencies import get_db, get_current_user
from app.services import department_service

router = APIRouter()

# 診療科の全件表示
@router.get(
    "/departments",
    response_model=list[DepartmentResponse],
    status_code=status.HTTP_200_OK,
)
def get_departments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # serviceに処理を委譲して結果だけ返す
    return department_service.get_departments_service(db)
    