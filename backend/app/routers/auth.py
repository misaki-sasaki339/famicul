from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.core.security import verify_password
from app.core.auth import create_token
from app.core.dependencies import get_current_user

router = APIRouter()

# ログインAPI
@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):

    # 入力されたemailと合致するユーザをDBから検索
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=401)

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401)
    
    token = create_token(user.id)

    return {"access_token": token}

# ログインユーザAPI
@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return current_user