from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, Base
from app.core.dependencies import get_db
from app.models import user as user_model
from app.schemas import user as user_schema
from app.models import child as child_model
from app.schemas import child as child_schema
from app.models import department as department_model
from app.schemas import department as department_schema
from app.models import visit as visit_model
from app.schemas import visit as visit_schema
from app.models import disease as disease_model
from app.core.security import get_password_hash
from app.routers import auth
from app.routers import children
from app.routers import hospitals

# appインスタンスを作成（サーバ本体）
app = FastAPI()

# ルートURLにアクセスしたときの処理
@app.get("/")
def read_root():
    return {"message": "Famicul API is running!"}

# ログイン処理の読み込み
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# /childへのアクセスの処理
app.include_router(children.router, tags=["children"])

# /hospitalへのアクセスの処理
app.include_router(hospitals.router, tags=["hospital"])

@app.post("/register")
def register_user(user_in: user_schema.UserCreate, db: Session = Depends(get_db)):
    # 1. すでに同じメールアドレスが登録されていないかチェック
    db_user = db.query(user_model.User).filter(user_model.User.email == user_in.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. パスワードをハッシュ化してモデルを作成
    try:
        hashed_pw = get_password_hash(user_in.password)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error during password processing")
    
    # 3. モデルのインスタンスを作成
    new_user = user_model.User(
        name=user_in.name,
        email=user_in.email,
        hashed_password=hashed_pw
    )

    # 4. DBに保存
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")

    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "message": "User created successfully!"
    }