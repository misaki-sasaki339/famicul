from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.crud import visit_image as visit_image_crud
from app.schemas.visit import VisitImageCreate, VisitKey
from app.services.visit_service import _get_visit_or_404

# 画像１件を取得し、なければ404を返す
def _get_visit_image_or_404(
    db: Session,
    key: VisitKey,
    image_id: int,
    user_id: int
):
    _get_visit_or_404(db, key, user_id)
    # DBから対象画像を取得する
    visit_image = visit_image_crud.get_visit_image_by_id_and_visit_id(
        db, key.visit_id, image_id
    )

    # 見つからない場合は404を返す
    if not visit_image:
        raise HTTPException(status_code=404, detail="VisitImage not found")

    # 見つかった画像を返す
    return visit_image

# 画像作成処理
def create_visit_image_service(
    db: Session,
    key: VisitKey,
    visit_image_in: VisitImageCreate,
    user_id: int
):
    _get_visit_or_404(db, key, user_id)
    # pathのvisit_idとbodyのvisit_idがずれていないか確認
    if visit_image_in.visit_id != key.visit_id:
        raise HTTPException(status_code=400, detail="visit_id mismatch")

    # CRUDへ保存処理を委譲する
    return visit_image_crud.create_visit_image(db, visit_image_in)

# 画像一覧取得処理
def get_visit_images_service(
    db: Session,
    key: VisitKey,
    user_id: int
):
    _get_visit_or_404(db, key, user_id)
    # CRUDヘ取得処理を委譲する
    return visit_image_crud.get_visit_images_by_visit_id(db, key.visit_id)

# 画像削除処理
def delete_visit_image_service(
    db: Session,
    key: VisitKey,
    image_id: int,
    user_id: int
):
    # 対象画像を取得する（なければ404）
    visit_image = _get_visit_image_or_404(db, key, image_id, user_id)

    # CRUDへ処理を委譲する
    visit_image_crud.delete_visit_image(db, visit_image)

    return {"message": "VisitImage deleted successfully!"}