from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.crud import user as user_crud
from app.core.security import get_password_hash, verify_password
from app.core.auth import create_token

# 会員登録処理
def register_user_service(
    db: Session,
    user_in: UserCreate
):
    # メールの重複チェック
    existing_user = user_crud.get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # パスワードのハッシュ化
    hashed_pw = get_password_hash(user_in.password)

    # crudで保存
    return user_crud.create_user(db, user_in.name, user_in.email, hashed_pw)

# ログイン処理
def login_service(
    db: Session,
    email: str,
    password: str
):
    # メールアドレスからユーザーを探す
    user = user_crud.get_user_by_email(db, email)

    # 見つからなければ401エラー/セキュリティの観点からdetailは書かない
    if not user:
        raise HTTPException(status_code=401)
    
    # パスワードチェック/セキュリティの観点からdetailは書かない
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401)
    
    token = create_token(user.id)
    return {"access_token": token, "token_type": "bearer"}