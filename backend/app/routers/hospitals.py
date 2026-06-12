from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.hospital import HospitalCreate, HospitalUpdate, HospitalResponse
from app.core.dependencies import get_db, get_current_user
from app.services import hospital_service

router = APIRouter()

# 病院情報の登録
@router.post(
    "/hospitals",
    response_model=HospitalResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_hospital(
    hospital_in: HospitalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # serviceに処理を委譲して結果だけを返す
    return hospital_service.create_hospital_service(db, hospital_in, current_user.id)

# 病院情報の全件表示
@router.get(
    "/hospitals",
    response_model=list[HospitalResponse],
    status_code=status.HTTP_200_OK,
)
def get_hospitals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # serviceに処理を委譲して結果だけを返す
    return hospital_service.get_hospitals_service(db, current_user.id)

# 病院情報の表示
@router.get(
    "/hospitals/{hospital_id}",
    response_model=HospitalResponse,
    status_code=status.HTTP_200_OK,
)
def get_hospital(
    hospital_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # serviceに処理を委譲して結果だけを返す
    return hospital_service.get_hospital_service(db, hospital_id, current_user.id)

# 病院情報の更新
@router.patch(
    "/hospitals/{hospital_id}",
    response_model=HospitalResponse,
    status_code=status.HTTP_200_OK,
)
def update_hospital(
    hospital_id: int,
    hospital_in: HospitalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # serviceに処理を委譲して結果だけを返す
    return hospital_service.update_hospital_service(db, hospital_id, hospital_in, current_user.id)

# 病院情報の削除
@router.delete(
    "/hospitals/{hospital_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_hospital(
    hospital_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    hospital_service.delete_hospital_service(db, hospital_id, current_user.id)
