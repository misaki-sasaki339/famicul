from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.visit import VisitCreate, VisitImageCreate, VisitResponse, VisitUpdate
from app.core.dependencies import get_db
from app.models import Visit

router = APIRouter()

# 受診記録の登録
@router.post("/visits", response_model=VisitResponse)
def create_visit(
    visit_in: VisitCreate,
    db: Session = Depends(get_db),
):
    new_visit = Visit(
        child_id = visit_in.child_id,
        hospital_id = visit_in.hospital_id,
        department_id = visit_in.department_id,
        visit_date = visit_in.visit_date,
        symptom = visit_in.symptom,
        advice = visit_in.advice,
        next_visit_at = visit_in.next_visit_at,
        is_emergency = visit_in.is_emergency,
    )
    db.add(new_visit)
    db.commit()
    db.refresh(new_visit)

    # disease_namesは後で処理

    return new_visit

# 受診記録の表示
@router.get("/children/{child_id}/visits/{id}", response_model=VisitResponse)
def get_visit(
    child_id: int,
    id: int,
    db: Session = Depends(get_db),
):
    visit = db.query(Visit).filter(Visit.id == id, Visit.child_id == child_id).first()

    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")

    return visit

# 受診記録の更新
@router.put("/children/{child_id}/visits/{id}", response_model=VisitResponse)
def update_visit(
    child_id: int,
    id: int,
    visit_in: VisitUpdate,
    db: Session = Depends(get_db),
):
    visit = db.query(Visit).filter(Visit.id == id, Visit.child_id == child_id).first()

    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")

    update_data = visit_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if key == "disease_names":
            continue
        setattr(visit, key, value)

    db.commit()
    db.refresh(visit)

    return visit

# 受診記録の削除
@router.delete("/children/{child_id}/visits/{id}")
def delete_visit(
    child_id: int,
    id: int,
    db: Session = Depends(get_db),
):
    visit = db.query(Visit).filter(Visit.id == id, Visit.child_id == child_id).first()

    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")

    db.delete(visit)
    db.commit()
    # 削除が実行されるとdbからデータが消えるためdb.refresh(visit)は不要
    return {"message": "Visit deleted successfully!"}