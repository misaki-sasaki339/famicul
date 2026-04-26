from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.crud import child as child_crud
from app.schemas.child import ChildCreate, ChildUpdate

def _get_child_or_404(
    db: Session,
    child_id: int,
    user_id: int
):
    # DBから対象のユーザーのこどもを取得する
    child = child_crud.get_child_by_id_and_user_id(db, child_id, user_id)

    # 見つからない場合は404を返す
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")

    #見つかったこども情報を返す
    return child


def get_child_service(
    db: Session,
    child_id: int,
    user_id: int
):
    # 共通関数を使って取得
    return _get_child_or_404(db, child_id, user_id)

# こども作成処理
def create_child_service(
    db: Session,
    child_in: ChildCreate,
    user_id: int
):
    # DB保存処理をcrudへ委譲
    return child_crud.create_child(db, child_in, user_id)

# こども情報更新処理
def update_child_service(
    db: Session,
    child_id: int,
    child_in: ChildUpdate, 
    user_id: int
):
    # DBから対象のユーザーのこどもを探す
    child = _get_child_or_404(db, child_id, user_id)

    # DB保存処理をcrudへ委譲
    return child_crud.update_child(db, child, child_in)

# こども情報削除処理
def delete_child_service(
    db: Session,
    child_id: int,
    user_id: int
):
    # DBから対象のユーザーのこどもを探す
    child = _get_child_or_404(db, child_id, user_id)
    
    # DB削除処理をcrudに委譲
    child_crud.delete_child(db, child)
    return {"message": "Child deleted successfully!"}