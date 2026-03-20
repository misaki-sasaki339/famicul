from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import verify_password
from app.core.auth import create_token
from app.core.dependencies import get_db, get_current_user

router = APIRouter()

# ログインAPI
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # usernameにemailが入ってくる
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user:
        raise HTTPException(status_code=401)

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401)
    
    token = create_token(user.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# ログインユーザAPI
@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return current_user