from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.hospital import Hospital
from app.schemas.hospital import HospitalCreate, HospitalUpdate, HospitalResponse
from app.core.dependencies import get_db, get_current_user

router = APIRouter()

# 病院情報の登録
@router.post("/hospitals", response_model=HospitalResponse)
def create_hospital(
    hospital_in: HospitalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_hospital = Hospital(
        user_id = current_user.id,
        name = hospital_in.name,
        address = hospital_in.address,
        tel = hospital_in.tel,
        memo = hospital_in.memo,
    )
    db.add(new_hospital)
    db.commit()
    db.refresh(new_hospital)

    return new_hospital

# 病院情報の表示
@router.get("/hospitals/{id}", response_model=HospitalResponse)
def get_hospital(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    hospital = db.query(Hospital).filter(Hospital.id == id, Hospital.user_id == current_user.id).first()

    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")

    return hospital

# 病院情報の更新
@router.put("/hospitals/{id}", response_model=HospitalResponse)
def update_hospital(
    id: int,
    hospital_in: HospitalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    hospital = db.query(Hospital).filter(Hospital.id == id, Hospital.user_id == current_user.id).first()

    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")

    update_data = hospital_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(hospital, key, value)

    db.commit()
    db.refresh(hospital)

    return hospital

# 病院情報の削除
@router.delete("/hospitals/{id}")
def delete_hospital(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    hospital = db.query(Hospital).filter(Hospital.id == id, Hospital.user_id == current_user.id).first()

    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")

    db.delete(hospital)
    db.commit()
    # 削除が実行されるとdbからデータが消えるためdb.refresh(hospital)は不要
    return {"message": "Hospital deleted successfully!"}