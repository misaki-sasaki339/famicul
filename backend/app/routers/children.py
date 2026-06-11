from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.child import ChildCreate, ChildUpdate, ChildResponse
from app.core.dependencies import get_db, get_current_user
from app.services import child_service

router = APIRouter()

# 子ども情報の登録
@router.post(
    "/children",
    response_model=ChildResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_child(
    child_in: ChildCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # serviceに処理を委譲して結果だけ返す
    return child_service.create_child_service(db, child_in, current_user.id)

# こども情報の全件表示
@router.get(
    "/children",
    response_model=list[ChildResponse],
    status_code=status.HTTP_200_OK,
)
def get_children(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    #serviceに処理を委譲して結果だけ返す
    return child_service.get_children_service(db, current_user.id)

# こども情報の表示
@router.get(
    "/children/{child_id}",
    response_model=ChildResponse,
    status_code=status.HTTP_200_OK,
)
def get_child(
    child_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # serviceに処理を委譲して結果だけ返す
    return child_service.get_child_service(db, child_id, current_user.id)

# こども情報の更新
@router.patch(
    "/children/{child_id}",
    response_model=ChildResponse,
    status_code=status.HTTP_200_OK,
)
def update_child(
    child_id: int,
    child_in: ChildUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # serviceに処理を委譲して結果を返す
    return child_service.update_child_service(db, child_id, child_in, current_user.id)

# こども情報の削除
@router.delete(
    "/children/{child_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_child(
    child_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 削除処理だけ実行し何も返さない
    child_service.delete_child_service(db, child_id, current_user.id)
