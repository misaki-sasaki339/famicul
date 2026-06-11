from fastapi import APIRouter, Depends, UploadFile, File, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.schemas.visit import VisitKey, VisitImageResponse
from app.core.dependencies import get_db, get_current_user
from app.services import visit_image_service
from app.models.user import User

router = APIRouter()

# 画像ファイルそのものを取得する
@router.get(
    "/children/{child_id}/visits/{visit_id}/images/{image_id}/file",
    status_code=status.HTTP_200_OK,
)
def get_visit_image_file(
    child_id: int,
    visit_id: int,
    image_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # pathのchild_idとvisit_idをVisitKeyにまとめる
    key = VisitKey(child_id=child_id, visit_id=visit_id)
    file_path = visit_image_service.get_visit_image_file_service(db, key, image_id, current_user.id)
    return FileResponse(file_path)

# 画像の一覧取得
@router.get(
    "/children/{child_id}/visits/{visit_id}/images",
    response_model=list[VisitImageResponse],
    status_code=status.HTTP_200_OK,
)
def get_visit_images(
    child_id: int,
    visit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # pathのchild_idとvisit_idをVisitKeyにまとめる
    key = VisitKey(child_id=child_id, visit_id=visit_id)

    return visit_image_service.get_visit_images_service(db, key, current_user.id)

# 画像の登録
@router.post(
    "/children/{child_id}/visits/{visit_id}/images",
    response_model=VisitImageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_visit_image(
    child_id: int,
    visit_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # pathのchild_idとvisit_idをVisitKeyにまとめる
    key = VisitKey(child_id=child_id, visit_id=visit_id)
    # serviceの処理を委譲し結果だけを返す
    return visit_image_service.create_visit_image_service(db, key, file, current_user.id)

# 画像の削除
@router.delete(
    "/children/{child_id}/visits/{visit_id}/images/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_visit_image(
    child_id: int,
    visit_id: int,
    image_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # pathのchild_idとvisit_idをVisitKeyにまとめる
    key = VisitKey(child_id=child_id, visit_id=visit_id)

    visit_image_service.delete_visit_image_service(db, key, image_id, current_user.id)