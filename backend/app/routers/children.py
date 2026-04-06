from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.child import Child
from app.schemas.child import ChildCreate, ChildUpdate, ChildResponse
from app.core.dependencies import get_db, get_current_user

router = APIRouter()

# 子ども情報の登録
@router.post("/children", response_model=ChildResponse)
def create_child(
    child_in: ChildCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_child = Child(
        name = child_in.name,
        gender = child_in.gender,
        birthday = child_in.birthday,
        weight = child_in.weight,
        chronic_disease = child_in.chronic_disease,
        allergy = child_in.allergy,
        # memo = child_in.memo,
        user_id = current_user.id
    )
    db.add(new_child)
    db.commit()
    db.refresh(new_child)

    return new_child


# こども情報の表示
@router.get("/children/{id}", response_model=ChildResponse)
def get_child(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    child = db.query(Child).filter(Child.id == id, Child.user_id == current_user.id).first()

    if not child:
        raise HTTPException(status_code=404, detail="Child not found")

    return child


# こども情報の更新
@router.put("/children/{id}", response_model=ChildResponse)
def update_child(
    id: int,
    child_in: ChildUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    child = db.query(Child).filter(Child.id == id, Child.user_id == current_user.id).first()

    if not child:
        raise HTTPException(status_code=404, detail="Child not found")

    update_data = child_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(child, key, value)
    db.commit()
    db.refresh(child)

    return child

# こども情報の削除
@router.delete("/children/{id}")
def delete_child(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    child = db.query(Child).filter(Child.id == id, Child.user_id == current_user.id).first()

    if not child:
        raise HTTPException(status_code=404, detail="Child not found")

    db.delete(child)
    db.commit()
    # 削除が実行されるとdbからデータが消えるためdb.refresh(child)は不要
    return {"message": "Child deleted successfully!"}