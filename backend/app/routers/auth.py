from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.dependencies import get_db, get_current_user
from app.services import user_service
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()

# 会員登録API
@router.post("/register", response_model=UserResponse)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    return user_service.register_user_service(db, user_in)

# ログインAPI
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    email = form_data.username
    return user_service.login_service(db, email, form_data.password)

# ログインユーザAPI
@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user