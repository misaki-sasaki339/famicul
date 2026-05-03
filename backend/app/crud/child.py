from sqlalchemy.orm import Session

from app.models import Child
from app.schemas.child import ChildCreate, ChildUpdate

# こどもIDとユーザーIDからこども情報取得
def get_child_by_id_and_user_id(
    db: Session,
    child_id: int,
    user_id: int
):
    # 指定ユーザーのこども情報を１件取得
    return db.query(Child).filter(Child.id == child_id, Child.user_id == user_id).first()

# こども情報の新規作成
def create_child(
    db: Session,
    child_in: ChildCreate,
    user_id: int
):
    # 入力データからこどもモデルを作成して保存する
    new_child = Child(
        name = child_in.name,
        gender = child_in.gender,
        birthday = child_in.birthday,
        weight = child_in.weight,
        chronic_disease = child_in.chronic_disease,
        allergy = child_in.allergy,
        memo = child_in.memo,
        user_id = user_id
    )
    db.add(new_child)
    db.commit()
    db.refresh(new_child)

    return new_child

# こども情報の更新
def update_child(
    db: Session,
    child: Child,
    child_in: ChildUpdate,
):
    update_data = child_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(child, key, value)

    db.commit()
    db.refresh(child)

    return child

# こども情報の削除
def delete_child(
    db: Session,
    child: Child
) -> None:
    db.delete(child)
    db.commit()
    # 削除が実行されるとdbから削除されるためrefresh(child)は不要