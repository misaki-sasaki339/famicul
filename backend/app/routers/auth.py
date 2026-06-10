from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.dependencies import get_db, get_current_user
from app.services import user_service
from app.schemas.user import TokenResponse, UserCreate, UserResponse

router = APIRouter()

# 会員登録API
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    return user_service.register_user_service(db, user_in)

# ログインAPI
@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    email = form_data.username
    return user_service.login_service(db, email, form_data.password)

# ログインユーザAPI
@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def me(current_user: User = Depends(get_current_user)):
    return current_user