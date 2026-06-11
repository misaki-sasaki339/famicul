from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.visit import VisitCreate, VisitResponse, VisitUpdate, VisitKey
from app.core.dependencies import get_db, get_current_user
from app.services import visit_service
from app.models.user import User

router = APIRouter()

# 受診記録の登録
@router.post(
    "/children/{child_id}/visits",
    response_model=VisitResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_visit(
    child_id: int,
    visit_in: VisitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # serviceの処理を委譲し結果だけを返す
    return visit_service.create_visit_service(db, child_id, visit_in, current_user.id)

# こどもごとの受診記録の全件表示
@router.get(
    "/children/{child_id}/visits",
    response_model=list[VisitResponse],
    status_code=status.HTTP_200_OK,
)
def list_visits(
    child_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # serviceに処理を委譲して結果だけ返す
    return visit_service.list_visits_service(db, child_id, current_user.id)

# 受診記録の表示
@router.get(
    "/children/{child_id}/visits/{visit_id}",
    response_model=VisitResponse,
    status_code=status.HTTP_200_OK,
)
def get_visit(
    child_id: int,
    visit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # pathのchild_idとvisit_idをVisitKeyにまとめる
    key = VisitKey(child_id=child_id, visit_id=visit_id)

    # serviceに処理を委譲して結果だけを返す
    return visit_service.get_visit_service(db, key, current_user.id)

# 受診記録の更新
@router.patch(
    "/children/{child_id}/visits/{visit_id}",
    response_model=VisitResponse,
    status_code=status.HTTP_200_OK,
)
def update_visit(
    child_id: int,
    visit_id: int,
    visit_in: VisitUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # pathのchild_idとvisit_idをVisitKeyにまとめる
    key = VisitKey(child_id=child_id, visit_id=visit_id)

    # serviceに処理を委譲して結果だけを返す
    return visit_service.update_visit_service(db, key, visit_in, current_user.id)

# 受診記録の削除
@router.delete(
    "/children/{child_id}/visits/{visit_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_visit(
    child_id: int,
    visit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # pathのchild_idとvisit_idをVisitKeyにまとめる
    key = VisitKey(child_id=child_id, visit_id=visit_id)

    visit_service.delete_visit_service(db, key, current_user.id)
