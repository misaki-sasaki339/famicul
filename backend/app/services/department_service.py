from sqlalchemy.orm import Session

from app.crud import department as department_crud

# 受診科一覧取得処理
def get_departments_service(
    db: Session
):
    return department_crud.get_departments(db)
    