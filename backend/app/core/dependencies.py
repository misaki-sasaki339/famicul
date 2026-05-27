from app.database import SessionLocal
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt
from app.core.auth import SECRET_KEY, ALGORITHM
from app.crud import user as user_crud

# DBセッションを取得する依存関数
# リクエストごとにセッションを作成し、処理終了後にクローズする
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login")

# ログインユーザーの取得
def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_schema)
):
    # トークンを受け取りuser_idを取り出す
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload["sub"])
    except:
        raise HTTPException(status_code=401)

    user = user_crud.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=401)

    return user