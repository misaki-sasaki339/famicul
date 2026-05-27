from sqlalchemy.orm import Session

from app.models import User

# メールアドレスからユーザーを取得
def get_user_by_email(
    db: Session,
    email: str
) -> User | None:
    return db.query(User).filter(User.email == email).first

# ユーザー情報の新規作成
def create_user(
    db: Session,
    name: str,
    email: str,
    hashed_password: str
) -> User:
    # 入力データからユーザーモデルを作成して保存する
    new_user = User(
        name = name,
        email = email,
        hashed_password = hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# ユーザーIDからユーザーを取得
def get_user_by_id(
    db: Session,
    user_id: int
) -> User | None:
    return db.query(User).filter(User.id == user_id).first()