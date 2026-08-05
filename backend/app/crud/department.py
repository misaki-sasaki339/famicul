from sqlalchemy.orm import Session
from app.models import Department

# 診療科を全件取得する
def get_departments(
    db: Session
) -> list[Department]:
    return (
        db.query(Department)
        .order_by(Department.id.asc())
        .all()
    )

# 診療科を1件取得する(存在チェックで使用)
def get_department_by_id(
    db: Session, department_id: int
):
    return (
        db.query(Department)
        .filter(Department.id == department_id)
        .first()
    )