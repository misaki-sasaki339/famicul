from pydantic import BaseModel, EmailStr, ConfigDict

# 共通属性
class UserBase(BaseModel):
    name: str
    email: EmailStr

# ユーザ登録時のスキーマ
class UserCreate(UserBase):
    password: str

# レスポンス用スキーマ
class UserResponse(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# トークンレスポンス用スキーマ
class TokenResponse(BaseModel):
    access_token: str
    token_type: str