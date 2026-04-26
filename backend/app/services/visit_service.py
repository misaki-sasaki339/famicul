from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.crud import visit as visit_crud
from app.schemas.visit import VisitCreate, VisitKey, VisitUpdate


def _get_visit_or_404(
    db: Session,
    key: VisitKey
):
    # DBから対象のこどもの受診記録を取得する
    visit = visit_crud.get_visit_by_id_and_child_id(db, key.child_id, key.visit_id)

    # 見つからない場合は404を返す
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")

    # 見つかった受診記録を返す
    return visit

# 受診記録の取得処理
def get_visit_service(
    db: Session,
    key: VisitKey
):
    # 共通関数を使って取得
    return _get_visit_or_404(db, key)

# 受診記録作成処理
def create_visit_service(
    db: Session,
    child_id: int,
    visit_in: VisitCreate
):
    # DB保存処理をcrudへ委譲
    return visit_crud.create_visit(db, child_id, visit_in)

# 受診記録更新処理
def update_visit_service(
    db: Session,
    key: VisitKey,
    visit_in: VisitUpdate
):
    # DBから対象のこどもの受診記録を探す
    visit = _get_visit_or_404(db, key)

    # DB保存処理をcrudへ委譲
    return visit_crud.update_visit(db, visit, visit_in)

# 情報削除処理
def delete_visit_service(
    db: Session,
    key: VisitKey
):
    # DBから対象のこどもの受診記録を探す
    visit = _get_visit_or_404(db, key)
    
    # DB削除処理をcrudに委譲
    visit_crud.delete_visit(db, visit)
    return {"message": "Visit deleted successfully!"}