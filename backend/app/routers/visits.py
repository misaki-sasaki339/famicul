from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.visit import VisitCreate, VisitImageCreate, VisitResponse, VisitUpdate, VisitKey
from app.core.dependencies import get_db
from app.services import visit_service

router = APIRouter()

# 受診記録の登録
@router.post("/children/{child_id}/visits", response_model=VisitResponse)
def create_visit(
    child_id: int,
    visit_in: VisitCreate,
    db: Session = Depends(get_db),
):
    # serviceの処理を委譲し結果だけを返す
    return visit_service.create_visit_service(db, child_id, visit_in)

# 受診記録の表示
@router.get("/children/{child_id}/visits/{id}", response_model=VisitResponse)
def get_visit(
    child_id: int,
    id: int,
    db: Session = Depends(get_db),
):
    # pathのchild_idとvisit_idをVisitKeyにまとめる
    key = VisitKey(child_id=child_id, visit_id=id)

    # serviceに処理を委縮して結果だけを返す
    return visit_service.get_visit_service(db, key)

# 受診記録の更新
@router.put("/children/{child_id}/visits/{id}", response_model=VisitResponse)
def update_visit(
    child_id: int,
    id: int,
    visit_in: VisitUpdate,
    db: Session = Depends(get_db),
):
    # pathのchild_idとvisit_idをVisitKeyにまとめる
    key = VisitKey(child_id=child_id, visit_id=id)

    # serviceに処理を委譲して結果だけを返す
    return visit_service.update_visit_service(db, key, visit_in)

# 受診記録の削除
@router.delete("/children/{child_id}/visits/{id}")
def delete_visit(
    child_id: int,
    id: int,
    db: Session = Depends(get_db),
):
    # pathのchild_idとvisit_idをVisitKeyにまとめる
    key = VisitKey(child_id=child_id, visit_id=id)

    # serviceに処理を委譲して結果だけを返す
    return visit_service.delete_visit_service(db, key)