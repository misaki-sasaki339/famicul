from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.child import ChildCreate, ChildUpdate, ChildResponse
from app.core.dependencies import get_db, get_current_user
from app.services import child_service

router = APIRouter()

# 子ども情報の登録
@router.post("/children", response_model=ChildResponse)
def create_child(
    child_in: ChildCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # serviceに処理を委譲して結果だけ返す
    return child_service.create_child_service(db, child_in, current_user.id)

# こども情報の表示
@router.get("/children/{id}", response_model=ChildResponse)
def get_child(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # serviceに処理を委譲して結果だけ返す
    return child_service.get_child_service(db, id, current_user.id)

# こども情報の更新
@router.put("/children/{id}", response_model=ChildResponse)
def update_child(
    id: int,
    child_in: ChildUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    #serviceに処理を委譲して結果を返す
    return child_service.update_child_service(db, id, child_in, current_user.id)

# こども情報の削除
@router.delete("/children/{id}")
def delete_child(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # serviceに処理を委譲して結果を返す
    return child_service.delete_child_service(db, id, current_user.id)