from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.crud import child as child_crud
from app.crud import visit as visit_crud
from app.schemas.child import ChildCreate, ChildUpdate
from app.core.local_storage import delete_storage_file, delete_visit_upload_dir

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

    # 見つかったこども情報を返す
    return child

# こども情報の取得処理
def get_child_service(
    db: Session,
    child_id: int,
    user_id: int
):
    # 共通関数を使って取得
    return _get_child_or_404(db, child_id, user_id)

# こども情報の全件取得処理
def get_children_service(
    db: Session,
    user_id: int
):
    return child_crud.get_children_by_user_id(db, user_id)
    
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
    # ①DBから対象のユーザーのこどもを探す
    child = _get_child_or_404(db, child_id, user_id)

    # ②紐づく受診・画像レコードを削除（commitはしない）
    storage_keys, visit_ids = visit_crud.delete_all_for_child(
        db,
        child.id
    )
    
    # ③こども本体を削除（commitはしない）
    child_crud.delete_child(db, child, commit=False)

    # ④DBを確定
    db.commit()

    # ⑤ローカルのファイルを削除
    for storage_key in storage_keys:
        delete_storage_file(storage_key)

    # ⑥受診ごとの保存フォルダを削除
    for visit_id in visit_ids:
        delete_visit_upload_dir(visit_id)

    return {"message": "Child and related records deleted successfully!"}