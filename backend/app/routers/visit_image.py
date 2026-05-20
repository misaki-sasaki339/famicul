from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.visit import VisitImageCreate, VisitKey, VisitImageResponse
from app.core.dependencies import get_db, get_current_user
from app.services import visit_image_service
from app.models.user import User

router = APIRouter()

# 画像の登録
@router.post("/children/{child_id}/visits/{id}/images", response_model=VisitImageResponse)
def create_visit_image(
    child_id: int,
    id: int,
    visit_image_in: VisitImageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # pathのchild_idとvisit_idをVisitKeyにまとめる
    key = VisitKey(child_id=child_id, visit_id=id)
    # serviceの処理を委譲し結果だけを返す
    return visit_image_service.create_visit_image_service(db, key, visit_image_in, current_user.id)

# 画像の一覧取得
@router.get("/children/{child_id}/visits/{id}/images", response_model=list[VisitImageResponse])
def get_visit_images(
    child_id: int,
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # pathのchild_idとvisit_idをVisitKeyにまとめる
    key = VisitKey(child_id=child_id, visit_id=id)

    return visit_image_service.get_visit_images_service(db, key, current_user.id)

# 画像の削除
@router.delete("/children/{child_id}/visits/{id}/images/{image_id}")
def delete_visit_image(
    child_id: int,
    id: int,
    image_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # pathのchild_idとvisit_idをVisitKeyにまとめる
    key = VisitKey(child_id=child_id, visit_id=id)
    # serviceに処理を委譲して結果だけを返す
    return visit_image_service.delete_visit_image_service(db, key, image_id, current_user.id)