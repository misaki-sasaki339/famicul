from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.crud import hospital as hospital_crud
from app.schemas.hospital import HospitalCreate, HospitalUpdate
from app.crud import visit as visit_crud

def _get_hospital_or_404(
    db: Session,
    hospital_id: int,
    user_id: int
):
    # DBから対象のユーザーの病院を取得する
    hospital = hospital_crud.get_hospital_by_id_and_user_id(db, hospital_id, user_id)

    # 見つからない場合は404を返す
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")

    # 見つかった病院情報を返す
    return hospital

# 病院情報の取得処理
def get_hospital_service(
    db: Session,
    hospital_id: int,
    user_id: int
):
    # 共通関数を使って取得
    return _get_hospital_or_404(db, hospital_id, user_id)

# 病院情報の全件取得処理
def get_hospitals_service(
    db: Session,
    user_id: int
):
    return hospital_crud.get_hospitals_by_user_id(db, user_id)

# 病院作成処理
def create_hospital_service(
    db: Session,
    hospital_in: HospitalCreate,
    user_id: int
):
    # DB保存処理をcrudへ委譲
    return hospital_crud.create_hospital(db, hospital_in, user_id)

# 病院情報更新処理
def update_hospital_service(
    db: Session,
    hospital_id: int,
    hospital_in: HospitalUpdate, 
    user_id: int
):
    # DBから対象のユーザーの病院を探す
    hospital = _get_hospital_or_404(db, hospital_id, user_id)

    # DB保存処理をcrudへ委譲
    return hospital_crud.update_hospital(db, hospital, hospital_in)

# 病院情報削除処理
def delete_hospital_service(
    db: Session,
    hospital_id: int,
    user_id: int
):
    # DBから対象のユーザーの病院を探す
    hospital = _get_hospital_or_404(db, hospital_id, user_id)

    # 受診記録の件数を調べる
    visit_count = visit_crud.count_visits_by_hospital_id(db, hospital_id)

    # 1件以上あれば削除不可
    if visit_count > 0:
        raise HTTPException(status_code=409, detail="Cannot delete hospital with existing visit records")
    
    # DB削除処理をcrudに委譲
    hospital_crud.delete_hospital(db, hospital)
    return {"message": "Hospital deleted successfully!"}